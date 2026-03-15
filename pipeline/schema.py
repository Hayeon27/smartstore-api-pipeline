"""데이터베이스 스키마 정의 모듈."""

SCHEMA = {
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            origin_product_no TEXT PRIMARY KEY,
            channel_product_no TEXT,
            name TEXT,
            status TEXT,
            sale_price INTEGER,
            stock_quantity INTEGER,
            category_id TEXT,
            representative_image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            product_order_id TEXT PRIMARY KEY,
            order_id TEXT,
            product_no TEXT,
            product_name TEXT,
            quantity INTEGER,
            order_status TEXT,
            payment_date TIMESTAMP,
            delivery_fee INTEGER,
            total_payment_amount INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "inquiries": """
        CREATE TABLE IF NOT EXISTS inquiries (
            inquiry_no INTEGER PRIMARY KEY,
            inquiry_type TEXT,
            customer_name TEXT,
            product_name TEXT,
            content TEXT,
            is_answered BOOLEAN,
            answered_at TIMESTAMP,
            created_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
}
