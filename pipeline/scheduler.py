"""파이프라인 스케줄러 모듈."""

import asyncio
import logging
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pipeline.runner import PipelineRunner
from client import NaverCommerceClient

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

async def run_pipeline_task():
    """주기적으로 실행될 파이프라인 작업."""
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    logger.info("⏰ 정기 파이프라인 실행을 시작합니다...")
    try:
        async with NaverCommerceClient(client_id, client_secret) as client:
            runner = PipelineRunner(client)
            await runner.run()
        logger.info("✅ 정기 파이프라인 실행 완료.")
    except Exception as e:
        logger.error(f"❌ 정기 파이프라인 실행 중 오류 발생: {e}")

async def main():
    scheduler = AsyncIOScheduler()
    
    # 1. 1시간마다 실행 (환경에 따라 조절 가능)
    # 테스트를 위해 5분마다 실행하도록 설정 가능
    scheduler.add_job(
        run_pipeline_task,
        CronTrigger(minute="0"), # 매시 정각
        name="Hourly Pipeline Task"
    )

    # 2. 즉시 1회 실행 후 스케줄 시작
    await run_pipeline_task()
    
    scheduler.start()
    logger.info("🚀 파이프라인 스케줄러가 시작되었습니다. (Ctrl+C로 종료)")

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("👋 스케줄러를 종료합니다.")
        scheduler.shutdown()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
