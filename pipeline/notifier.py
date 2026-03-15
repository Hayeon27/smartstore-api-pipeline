"""실시간 알림 전송 모듈."""

import logging
import os
import httpx
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class Notifier:
    """Slack/Discord 웹훅을 통해 알림을 전송하는 클래스."""

    def __init__(self):
        self.webhook_url = os.getenv("WEBHOOK_URL")
        if not self.webhook_url:
            logger.warning("WEBHOOK_URL이 설정되지 않아 알림 기능이 활성화되지 않았습니다.")

    async def send_notification(self, title: str, message: str, color: str = "#36a64f"):
        """Slack/Discord로 메시지를 전송합니다."""
        if not self.webhook_url:
            return

        # Slack 포맷 (Discord도 일부 호환)
        payload = {
            "attachments": [
                {
                    "title": title,
                    "text": message,
                    "color": color
                }
            ]
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.webhook_url, json=payload)
                response.raise_for_status()
                logger.debug(f"알림 전송 성공: {title}")
        except Exception as e:
            logger.error(f"알림 전송 실패: {e}")

    async def notify_new_orders(self, orders: List[Dict[str, Any]]):
        """신규 주문 알림."""
        if not orders: return
        
        count = len(orders)
        msg = f"🎉 신규 주문이 {count}건 발생했습니다!\n"
        for o in orders[:5]: # 최대 5건만 상세 표시
            msg += f"- 주문번호: {o.get('productOrderId')} | 금액: {o.get('totalPaymentAmount', 0):,}원 | 상태: {o.get('orderStatus')}\n"
        
        if count > 5:
            msg += f"...외 {count-5}건 더 있음"
            
        await self.send_notification("🛒 신규 주문 알림", msg, color="#E01E5A")

    async def notify_new_inquiries(self, inquiries: Dict[str, List[Any]]):
        """신규 문의 알림."""
        customers = inquiries.get("customer", [])
        products = inquiries.get("product", [])
        
        if not customers and not products: return
        
        msg = ""
        if customers:
            msg += f"💬 고객 문의: {len(customers)}건\n"
        if products:
            msg += f"📦 상품 Q&A: {len(products)}건\n"
            
        await self.send_notification("💬 신규 문의 알림", msg, color="#2EB67D")

    async def notify_new_products(self, products: List[Dict[str, Any]]):
        """신규 상품 등록 수집 알림."""
        if not products: return
        
        count = len(products)
        msg = f"🆕 신규 상품 {count}건이 파이프라인에 수집되었습니다.\n"
        for p in products[:3]:
            origin_name = p.get('originProduct', {}).get('name', '알 수 없는 상품')
            msg += f"- {origin_name} (ID: {p.get('originProductNo')})\n"
            
        await self.send_notification("📦 신규 상품 수집 알림", msg, color="#4385f4")
