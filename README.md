# BLE Scanner

[![Build and Release](https://github.com/cjeonguk/bero-client/actions/workflows/build.yml/badge.svg?event=push)](https://github.com/cjeonguk/bero-client/actions/workflows/build.yml)

BLE 장치를 스캔하고 감지된 장치의 정보를 중앙 API 서버로 전송하는 서비스입니다.

## 요구사항

- Python 3.9+
- Bluetooth 모듈이 구성된 시스템

## 설치

1. 의존성 설치:
```bash
uv sync --locked
```

2. 환경 변수 설정:
`.env` 파일을 프로젝트 루트 디렉토리에 생성하고 다음 변수들을 설정합니다:

```env
API_BASE_URL=localhost:5173
SCAN_INTERVAL=1
MAX_RETRY_ATTEMPTS=3
RETRY_DELAY=1
```

## 실행

서비스 시작:
```bash
uv run src/main.py
```

서비스가 시작되면:
1. BLE 스캐너가 자동으로 시작됩니다
2. 감지된 BLE 장치의 정보가 설정된 API 서버로 전송됩니다
3. 헬스체크 엔드포인트: http://localhost:8000/health

## API 서버로 전송되는 데이터 형식

```json
{
    "deviceID": "AA:BB:CC:DD:EE:FF",  // 장치의 MAC 주소
    "rssi": -67,                        // 신호 강도 (dBm)
    "timestamp": "2024-03-14T17:12:54+09:00",  // 감지 시각
    "deviceName": "device1",
    "classroom": "xxx"
}
```
