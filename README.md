# 🩷 티니핑 도감

아이와 함께 볼 수 있는 귀여운 **티니핑 도감 Streamlit 앱**입니다.  
사진, 이름, 특징, 설명을 카드 형태로 볼 수 있습니다.

## 현재 포함된 파일

- `data/teenieping_data.csv`: 티니핑 데이터 수집용 CSV 템플릿

## CSV 컬럼 설명

- `name`: 티니핑 이름
- `feature`: 한 줄 특징
- `description`: 자세한 설명
- `season`: 시즌 정보
- `category`: 감정 / 행동 / 마법 등 분류
- `image`: 앱에서 사용할 이미지 경로
- `source`: 참고한 출처 메모
- `memo`: 수정 메모
- `status`: `초안`, `검수중`, `완료` 같은 상태 관리

## 사용 방법

1. `data/teenieping_data.csv` 파일을 열어 데이터를 입력합니다.
2. 이미지 파일은 추후 `images/` 폴더에 넣습니다.
3. 이후 Streamlit 앱과 연결해 도감으로 확장할 수 있습니다.

## 권장 저장소 구조

```text
teenieping-book/
├─ data/
│  └─ teenieping_data.csv
├─ images/
└─ app.py
```

## 주의사항

티니핑 캐릭터 이미지와 이름, 설정 등은 저작권 또는 관련 권리가 있을 수 있습니다.  
공개 배포 전에는 이미지 및 콘텐츠 사용 권한을 꼭 확인하세요.
