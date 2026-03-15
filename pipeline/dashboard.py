"""네이버 스마트스토어 분석 대시보드 (FastAPI)."""

import os
import sqlite3
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from pathlib import Path

app = FastAPI(title="Smartstore Analytics Dashboard")

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

    # 3. 최근 상품 목록
    cursor.execute("SELECT name, sale_price, status, representative_image_url FROM products ORDER BY updated_at DESC LIMIT 5")
    recent_products = cursor.fetchall()

    # 4. 최근 문의
    cursor.execute("SELECT inquiry_type, customer_name, content, is_answered FROM inquiries ORDER BY created_at DESC LIMIT 5")
    recent_inquiries = cursor.fetchall()
    
    conn.close()
    return {
        "summary": summary,
        "stats": stats_rows,
        "products": recent_products,
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
        "inquiries": data["inquiries"]
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
