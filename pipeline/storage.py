"""데이터베이스 저장 및 조회 관리 모듈."""

import sqlite3
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from .schema import SCHEMA

logger = logging.getLogger(__name__)

class StorageManager:
    """SQLite 데이터베이스 연동 및 데이터 저장 관리 클래스."""

    def __init__(self, db_path: str = "data/smartstore.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """스키마를 기반으로 테이블 초기화."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for table_name, create_sql in SCHEMA.items():
                logger.debug(f"Initializing table: {table_name}")
                cursor.execute(create_sql)
            conn.commit()

    def upsert_products(self, products: List[Dict[str, Any]]):
        """상품 정보 저장 또는 업데이트 (Upsert)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            sql = """
                INSERT INTO products (
                    origin_product_no, channel_product_no, name, status,
                    sale_price, stock_quantity, category_id, representative_image_url,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(origin_product_no) DO UPDATE SET
                    name=excluded.name,
                    status=excluded.status,
                    sale_price=excluded.sale_price,
                    stock_quantity=excluded.stock_quantity,
                    category_id=excluded.category_id,
                    representative_image_url=excluded.representative_image_url,
                    updated_at=CURRENT_TIMESTAMP
            """
            
            flat_products = []
            for item in products:
                # v1/products/search 스펙 대응: originProductNo와 channelProducts 리스트가 있음
                origin_no = item.get("originProductNo")
                channels = item.get("channelProducts", [])
                
                if not channels:
                    continue
                
                # 첫 번째 채널 정보를 대표로 저장
                main_ch = channels[0]
                flat_products.append((
                    origin_no,
                    main_ch.get("channelProductNo"),
                    main_ch.get("name"),
                    main_ch.get("statusType"),
                    main_ch.get("salePrice"),
                    main_ch.get("stockQuantity"),
                    main_ch.get("leafCategoryId"),
                    main_ch.get("representativeImage", {}).get("url") if isinstance(main_ch.get("representativeImage"), dict) else None
                ))
            
            if not flat_products:
                logger.warning("No products to upsert after flattening.")
                return

            cursor.executemany(sql, flat_products)
            conn.commit()
            logger.info(f"Upserted {len(flat_products)} products to database.")

    def upsert_orders(self, orders: List[Dict[str, Any]]):
        """주문 정보 저장 또는 업데이트 (Upsert)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            sql = """
                INSERT INTO orders (
                    product_order_id, order_id, product_no, product_name,
                    quantity, order_status, payment_date, delivery_fee,
                    total_payment_amount, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(product_order_id) DO UPDATE SET
                    order_status=excluded.order_status,
                    updated_at=CURRENT_TIMESTAMP
            """
            data = [
                (
                    o.get("productOrderId"),
                    o.get("orderId"),
                    o.get("productNo"),
                    o.get("productName"),
                    o.get("quantity"),
                    o.get("orderStatus"),
                    o.get("paymentDate"),
                    o.get("deliveryFee"),
                    o.get("totalPaymentAmount"),
                ) for o in orders
            ]
            cursor.executemany(sql, data)
            conn.commit()
            logger.info(f"Upserted {len(orders)} orders.")

    def upsert_inquiries(self, inquiries: List[Dict[str, Any]]):
        """문의 정보 저장 또는 업데이트 (Upsert)."""
        # (v1/pay-user/inquiries 기준 예시)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            sql = """
                INSERT INTO inquiries (
                    inquiry_no, inquiry_type, customer_name, product_name,
                    content, is_answered, answered_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(inquiry_no) DO UPDATE SET
                    is_answered=excluded.is_answered,
                    answered_at=excluded.answered_at,
                    updated_at=CURRENT_TIMESTAMP
            """
            data = [
                (
                    i.get("inquiryNo"),
                    i.get("inquiryType"),
                    i.get("customerName"),
                    i.get("productName"),
                    i.get("content"),
                    i.get("answered"),
                    i.get("answeredAt"),
                    i.get("createDate"),
                ) for i in inquiries
            ]
            cursor.executemany(sql, data)
            conn.commit()
            logger.info(f"Upserted {len(inquiries)} inquiries.")
