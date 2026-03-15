"""네이버 스마트스토어 분석 대시보드 (FastAPI)."""

import os
import sqlite3
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import sys
from pathlib import Path

# 루트 디렉토리를 sys.path에 추가하여 상위 모듈(client 등) 참조 허용
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.responses import HTMLResponse, JSONResponse
from client import NaverCommerceClient
import logging
import asyncio

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Smartstore Analytics Dashboard")

# Naver API 클라이언트 초기화
api_client = NaverCommerceClient(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET")
)

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# DB 경로
DB_PATH = "data/smartstore.db"

def get_db_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 1. 요약 정보 (최근 7일 합계)
    cursor.execute("""
        SELECT 
            SUM(payment_amount) as total_sales,
            SUM(payment_count) as total_orders,
            SUM(visitor_count) as total_visitors
        FROM daily_stats
    """)
    summary = cursor.fetchone()
    
    # 2. 일별 데이터 (차트용)
    cursor.execute("SELECT * FROM daily_stats ORDER BY search_date ASC LIMIT 14")
    stats_rows = cursor.fetchall()
    
    # 데이터가 없을 경우 데모용 가상 데이터 생성 (시각화 확인용)
    if not stats_rows:
        import random
        demo_stats = []
        for i in range(7, 0, -1):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            demo_stats.append({
                "search_date": date,
                "payment_amount": random.randint(50000, 200000),
                "payment_count": random.randint(5, 20),
                "visitor_count": random.randint(100, 500)
            })
        stats_rows = demo_stats

    # 3. 최근 상품 및 재고 상태
    cursor.execute("SELECT origin_product_no, name, sale_price, status, stock_quantity, representative_image_url FROM products ORDER BY updated_at DESC LIMIT 10")
    recent_products = cursor.fetchall()

    # 4. 실시간 주문 현황
    cursor.execute("SELECT order_id, product_name, quantity, order_status, total_payment_amount, payment_date FROM orders ORDER BY payment_date DESC LIMIT 10")
    realtime_orders = cursor.fetchall()

    # 5. 최근 문의
    cursor.execute("SELECT inquiry_type, customer_name, content, is_answered FROM inquiries ORDER BY created_at DESC LIMIT 5")
    recent_inquiries = cursor.fetchall()
    
    conn.close()
    return {
        "summary": summary,
        "stats": stats_rows,
        "products": recent_products,
        "orders": realtime_orders,
        "inquiries": recent_inquiries
    }

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    data = get_db_data()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "summary": data["summary"],
        "stats": data["stats"],
        "products": data["products"],
        "orders": data["orders"],
        "inquiries": data["inquiries"]
    })

@app.post("/api/products")
async def create_product(data: dict = Body(...)):
    """새로운 상품 등록 (v2)."""
    try:
        # 데이터 정규화 (샘플 구조 기반)
        # 실제로는 복잡한 JSON 구조가 필요하므로, 간단한 입력 필드에서 확장된 구조 생성
        product_body = {
            "originProduct": {
                "name": data.get("name"),
                "statusType": "SUSPENSION", # 안전을 위해 기본 중지
                "salePrice": int(data.get("salePrice", 0)),
                "stockQuantity": int(data.get("stockQuantity", 0)),
                "leafCategoryId": data.get("categoryId", "50000000"), # 기본 카테고리
                "detailContent": data.get("detailContent", "상품 상세 정보입니다."),
                "images": {
                    "representativeImage": {
                        "url": data.get("imageUrl", "https://via.placeholder.com/500")
                    }
                }
            }
            # ... 기타 필수 필드는 client 내부 default 또는 확장이 필요할 수 있음
        }
        
        # 실제 API 호출 (auth/token 자동 갱신 등은 Client 내부에서 처리됨)
        # register_product_sample.py 의 로직을 간소화하여 반영
        res = await api_client.products.create_product(product_body)
        
        # 등록 성공 시 DB 즉시 수집 유도 (또는 수동 추가)
        return JSONResponse(content={"status": "success", "data": res})
    except Exception as e:
        logger.error(f"Product creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/products/{origin_no}")
async def delete_product(origin_no: str):
    """상품 삭제."""
    try:
        # 1. 실제 네이버 API 호출 (삭제 또는 판매중지 처리)
        # 삭제 API (v2) 호출
        await api_client.products.delete_product(origin_no)
        
        # 2. 로컬 DB 동기화 (삭제)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE origin_product_no = ?", (origin_no,))
            conn.commit()
            
        return {"status": "success", "message": f"Product {origin_no} deleted."}
    except Exception as e:
        logger.error(f"Product deletion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
