# BLE Scanner

BLE 장치를 스캔하고 감지된 장치의 정보를 중앙 API 서버로 전송하는 서비스입니다.

## 요구사항

- Python 3.9+
- Bluetooth 어댑터가 있는 리눅스 또는 macOS 시스템
- (리눅스의 경우) `bluez` 패키지

## 설치

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정:
`.env` 파일을 프로젝트 루트 디렉토리에 생성하고 다음 변수들을 설정합니다:

```env
API_BASE_URL=https://api.example.com
SCAN_INTERVAL=1
MAX_RETRY_ATTEMPTS=3
RETRY_DELAY=1
```

## 실행

서비스 시작:
```bash
python src/main.py
```

서비스가 시작되면:
1. BLE 스캐너가 자동으로 시작됩니다
2. 감지된 BLE 장치의 정보가 설정된 API 서버로 전송됩니다
3. 헬스체크 엔드포인트: http://localhost:8000/health

## API 서버로 전송되는 데이터 형식

```json
{
    "device_id": "AA:BB:CC:DD:EE:FF",  // 장치의 MAC 주소
    "rssi": -67,                        // 신호 강도 (dBm)
    "timestamp": "2024-03-14T17:12:54+09:00"  // 감지 시각
}
```

## 참고사항

- 현재 API 엔드포인트와 요청 형식은 임시로 설정되어 있습니다 (TODO 주석 참고)
- 오류 발생 시 자동으로 재시도합니다 (기본값: 최대 3회)
- 로그는 콘솔에 출력됩니다
