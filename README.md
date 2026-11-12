# 성적 관리 프로그램

## 무엇을 하나요 (What)
성적 CSV 파일을 읽어 유효한 점수(0~100점)만 골라내고, 비정상 데이터는 프로그램 중단 없이 건너뛰며 사유를 기록하는 프로그램입니다.

## 왜 만들었나요 (Why)
실제 성적 데이터에는 빈 줄, 0~100점 범위를 벗어난 이상치, 열 개수 오류 등이 섞여 있어 예외 처리를 하지 않으면 프로그램이 중단되거나 잘못된 결과를 내기 때문입니다.

## 어떻게 쓰나요 (How)
`python load_scores.py scores.csv`

## 어떻게 테스트하나요 (Test)
`python -m pip install pytest pytest-cov`
`python -m pytest test_load_scores.py`

## 파일 구성
- `load_scores.py`: 성적 CSV 파일을 읽고 유효성을 검증하는 핵심 함수
- `test_load_scores.py`: 정상·예외·경계값 케이스를 검증하는 pytest 테스트 코드
- `test_ai_A.py`, `test_ai_B.py`: AI 테스트 생성 방식 비교 실험용 테스트 파일
- `scores.csv`, `empty.csv`, `weird.csv`: 테스트용 CSV 데이터 파일

## 만든 사람 · AI 활용 내역
- 이름 / 학번: 김나현 / 2026100656
- AI 활용 내역: pytest 단위 테스트 작성 보조, 코드 제공(A) vs 명세 제공(B) 테스트 생성 비교 실험 및 README 작성에 활용함.