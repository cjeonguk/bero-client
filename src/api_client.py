import httpx
import logging
import asyncio
from datetime import datetime
# from typing import Dict, Any

from config import API_ENDPOINT, MAX_RETRY_ATTEMPTS, RETRY_DELAY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def close(self):
        await self.client.aclose()
    
    async def send_device_detection(self, device_id: str, rssi: int, device_name: str) -> bool:
        """감지된 BLE 장치 정보를 API 서버로 전송"""
        data = {
            "device_id": device_id,
            "rssi": rssi,
            "device_name": device_name,
            "timestamp": datetime.now().isoformat()
        }

        # API 서버로의 요청을 임시로 비활성화하고 로그만 출력
        logger.info(f"[임시모드] 장치 감지 데이터: {data}")
        return True
        
        # 아래 코드는 실제 API 서버 연결이 필요할 때 주석 해제
        """
        for attempt in range(MAX_RETRY_ATTEMPTS):
            try:
                # TODO: API 엔드포인트 및 요청 형식은 실제 서버 스펙에 맞게 수정 필요
                response = await self.client.post(API_ENDPOINT, json=data)
                response.raise_for_status()
                logger.info(f"장치 감지 데이터 전송 성공: {device_id}")
                return True
                
            except httpx.ConnectError as e:
                logger.error(f"API 서버 연결 실패 (시도 {attempt + 1}/{MAX_RETRY_ATTEMPTS}): {str(e)}")
                logger.info(f"API_ENDPOINT: {API_ENDPOINT}")
                if attempt < MAX_RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(RETRY_DELAY)
                continue
                
            except httpx.HTTPError as e:
                logger.error(f"API 요청 실패 (시도 {attempt + 1}/{MAX_RETRY_ATTEMPTS}): {str(e)}")
                if attempt < MAX_RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(RETRY_DELAY)
                continue
                
            except Exception as e:
                logger.error(f"예상치 못한 오류 발생: {str(e)}")
                return False
        
        logger.error(f"최대 재시도 횟수 초과: {device_id}")
        return False
        """
