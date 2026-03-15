import asyncio
import os
import json
from dotenv import load_dotenv
from client import NaverCommerceClient

load_dotenv()

async def debug_product():
    async with NaverCommerceClient(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET")
    ) as client:
        p_no = "13195917377"
        print(f"Fetching details for {p_no}...")
        try:
            detail = await client.products.get_origin_product(p_no)
            with open("product_debug.json", "w", encoding="utf-8") as f:
                json.dump(detail, f, indent=2, ensure_ascii=False)
            print("Done. Saved to product_debug.json")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_product())
