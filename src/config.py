from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# API 설정
# TODO: 실제 중앙 API 서버 엔드포인트로 변경 필요
API_BASE_URL = os.getenv("API_BASE_URL", "http://bero-dev.netlify.app")
API_ENDPOINT = f"{API_BASE_URL}/api"

# BLE 스캐너 설정
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "1"))  # 초 단위
MAX_RETRY_ATTEMPTS = int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "1"))  # 초 단위
