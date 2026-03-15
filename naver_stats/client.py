"""네이버 커머스 API 통계(Statistics) 클라이언트."""

from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from client import NaverCommerceClient


class StatisticsClient:
    """비즈니스 통계 관련 API 클라이언트 (API데이터솔루션).
    
    공식 문서: https://apicenter.commerce.naver.com/docs/commerce-api/current/%ED%86%B5%EA%B3%84
    """

    def __init__(self, client: "NaverCommerceClient"):
        self.client = client

    async def get_all_channel_daily_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """전체 채널 일별 리포트 조회.
        GET /v1/bizdata/stats/all-channel-daily-report
        """
        return await self.client.get("/v1/bizdata/stats/all-channel-daily-report", params=params)

    async def get_all_channel_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """전체 채널 리포트 조회.
        GET /v1/bizdata/stats/all-channel-report
        """
        return await self.client.get("/v1/bizdata/stats/all-channel-report", params=params)

    async def get_custom_channel_detail_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """사용자 정의 채널 상세 리포트 조회.
        GET /v1/bizdata/stats/custom-channel-detail-report
        """
        return await self.client.get("/v1/bizdata/stats/custom-channel-detail-report", params=params)

    async def get_custom_channel_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """사용자 정의 채널 리포트 조회.
        GET /v1/bizdata/stats/custom-channel-report
        """
        return await self.client.get("/v1/bizdata/stats/custom-channel-report", params=params)

    async def get_hourly_channel_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """시간대별 채널 리포트 조회.
        GET /v1/bizdata/stats/hourly-channel-report
        """
        return await self.client.get("/v1/bizdata/stats/hourly-channel-report", params=params)
