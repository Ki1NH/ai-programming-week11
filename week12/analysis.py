'''
[역할]
너는 파이썬 데이터 처리를 돕는 조교다. 대학교 1학년이 읽을 코드를 쓴다.

[목표]
아래 명세대로 CSV를 정제하는 함수 정제(df) 를 만들어라.

[데이터]
  파일: scores_2026.csv, 114행 5열
  열: 학번(문자), 이름(문자), 반(문자), 과목(문자), 점수(정수)
  점수는 0 이상 100 이하의 정수여야 한다.
  반과 과목 값의 앞뒤에 공백이 섞여 있다.
  점수가 비어 있는 행이 있다.
  모든 열이 완전히 같은 행이 중복으로 들어 있다.

[처리 규칙]
  1) 점수가 비어 있는 행은 삭제한다.
  2) 모든 열이 완전히 같은 행은 하나만 남긴다.
  3) 반과 과목의 앞뒤 공백을 제거한다.
  4) 점수가 0~100 밖인 행은 삭제한다.

[제약]
  - pandas 만 사용한다. 다른 라이브러리를 쓰지 마라.
  - 각 단계가 끝날 때마다 남은 행 수를 print 하라.
  - 원본 df 를 직접 고치지 말고 복사본을 만들어 작업하라.
  - 한 줄짜리 주석으로 각 단계가 무엇을 하는지 적어라.
  '''

import pandas as pd


def 정제(df):
    df = df.copy()

    # 점수가 비어 있는 행을 삭제한다.
    df["점수"] = df["점수"].replace(r"^\s*$", pd.NA, regex=True)
    df = df.dropna(subset=["점수"])
    print("점수 결측치 삭제 후 남은 행 수:", len(df))

    # 모든 열이 완전히 같은 행은 하나만 남긴다.
    df = df.drop_duplicates()
    print("중복 제거 후 남은 행 수:", len(df))

    # 반과 과목의 앞뒤 공백을 제거한다.
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    print("공백 제거 후 남은 행 수:", len(df))

    # 점수가 정수이고 0~100 범위에 있는 행만 남긴다.
    df["점수"] = pd.to_numeric(df["점수"], errors="coerce")
    df = df.dropna(subset=["점수"])
    df = df[df["점수"].mod(1).eq(0)]
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]
    df["점수"] = df["점수"].astype(int)
    print("점수 범위 필터링 후 남은 행 수:", len(df))

    return df.reset_index(drop=True)


def 반별평균(df):
    return df.groupby("반")["점수"].mean().round(2)


if __name__ == "__main__":
    df = pd.read_csv("scores_2026.csv")
    정제된_df = 정제(df)
    print(정제된_df)

    '''
    정제된 df 에서 과목이 '수학'인 행만 남기는 코드를 한 줄로 써라.
    그리고 남은 행 수를 print 하라.

    (응용) 1반이면서 90점 이상인 행만 남기는 코드도 한 줄로 써라.
    '''
    math_rows = 정제된_df[정제된_df["과목"] == "수학"]
    print("수학 과목 행 수:", len(math_rows))

    class1_rows = 정제된_df[
        (정제된_df["반"] == "1반") & (정제된_df["점수"] >= 90)
    ]
    print("1반 90점 이상 행 수:", len(class1_rows))

    '''
    정제된 df 를 '반'으로 묶어 점수 평균을 내는 코드를 써라.
    그다음, '과목'과 '반' 두 기준으로 묶어 평균을 내는 코드도 따로 써라.
    두 결과를 각각 print 하라.
    '''
    class_averages = 정제된_df.groupby("반")["점수"].mean()
    print("반별 점수 평균:")
    print(class_averages)

    subject_class_averages = 정제된_df.groupby(["과목", "반"])["점수"].mean()
    print("과목과 반별 점수 평균:")
    print(subject_class_averages)

    '''
    정제된 df 를 '반'으로 묶어 개수 · 평균 · 중앙값 · 최댓값을
    한 표로 내는 코드를 써라. 소수 둘째 자리까지 반올림하라.
    함수 이름은 반별평균(df) 로 하고, 반 이름을 키로 하는
    평균값 딕셔너리(또는 Series)를 반환하게 하라.
    '''
    print(정제된_df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2))