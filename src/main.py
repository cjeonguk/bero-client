import asyncio
import logging
import yaml
from pathlib import Path
from bleak import BleakScanner
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api_client import APIClient
from config import SCAN_INTERVAL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

home_path = Path.home()

config_path = home_path / ".beroconf.yaml"

if config_path.exists():
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    classroom = config["classroom"]

    is_changed = input("교실 정보가 변경되었나요? (Y/n, 기본값: n): ")
    if is_changed.lower() == "y":
        classroom = input("설치된 교실 정보를 입력해주세요: ")
        config = {"classroom": classroom}
        with open(config_path, "w") as config_file:
            yaml.dump(config, config_file, default_flow_style=False)

else:
    classroom = input("설치된 교실 정보를 입력해주세요: ")
    config = {"classroom": classroom}

    with open(config_path, "w") as config_file:
        yaml.dump(config, config_file, default_flow_style=False)


class BLEScanner:
    def __init__(self):
        self.api_client = APIClient()
        self.is_scanning = False

    async def scan_devices(self):
        """BLE 장치 스캔 및 감지된 장치 정보 전송"""
        logger.info("BLE 스캔 시작")
        self.is_scanning = True

        while self.is_scanning:
            try:
                discovered_items = await BleakScanner.discover(
                    timeout=SCAN_INTERVAL, return_adv=True
                )
                for device, adv_data in discovered_items.values():
                    if (
                        device.address
                        and adv_data
                        and adv_data.rssi is not None
                        and device.name is not None
                    ):
                        current_rssi = adv_data.rssi

                        # API 전송 전 로그 (실제 전송되는 값 확인용)
                        logger.info(
                            f"  API 전송 예정: device_name='{device.name}', device_id='{device.address}', rssi={current_rssi}, service_uuids={adv_data.service_uuids}, service_data={adv_data.service_data}"
                        )
                        await self.api_client.send_device_detection(
                            device_name=device.name,
                            device_id=device.address,
                            rssi=current_rssi,
                            classroom=classroom,
                        )
                        # pass
            except Exception as e:
                logger.error(f"스캔 중 오류 발생: {str(e)}")
                await asyncio.sleep(SCAN_INTERVAL)

    def stop_scanning(self):
        """스캔 중지"""
        logger.info("BLE 스캔 중지")
        self.is_scanning = False

    async def cleanup(self):
        """리소스 정리"""
        self.stop_scanning()
        await self.api_client.close()


scanner = BLEScanner()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 스캔 시작
    asyncio.create_task(scanner.scan_devices())
    yield
    # 종료 시 정리
    await scanner.cleanup()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "scanning": scanner.is_scanning}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
