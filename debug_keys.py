import asyncio
import os
import json
from dotenv import load_dotenv
from client import NaverCommerceClient

load_dotenv()

async def debug_keys():
    async with NaverCommerceClient(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET")) as client:
        print("Searching products...")
        res = await client.products.search_products({"page": 0, "size": 1})
        contents = res.get("contents", [])
        if contents:
            print("Product Keys:", contents[0].keys())
            print("Sample Product:", json.dumps(contents[0], indent=2, ensure_ascii=False))
        else:
            print("No products found in search.")

if __name__ == "__main__":
    asyncio.run(debug_keys())
