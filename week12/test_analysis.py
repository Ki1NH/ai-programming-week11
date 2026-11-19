'''
아래 네 가지를 확인하는 pytest 테스트 파일을 만들어라.
파일 이름은 test_analysis.py 로 한다.

  ① scores_2026.csv 를 정제하면 100행이 남는다.
  ② 정제 후 '반' 값의 종류는 '1반'과 '2반' 두 개뿐이다.
  ③ 반으로 묶은 점수 합계의 합이 전체 점수 합계와 같다.
  ④ mini.csv 를 정제한 뒤 1반 평균이 80.0 이다.

[제약]
  - 함수 이름은 test_ 로 시작한다.
  - assert 를 쓴다.
  - 파일을 읽는 코드는 파일 맨 위에서 한 번만 실행한다.
'''

import pandas as pd

from analysis import 정제


점수_df = pd.read_csv("scores_2026.csv")
mini_df = pd.read_csv("mini.csv")
정제된_df = 정제(점수_df)
mini_정제_df = 정제(mini_df)


def test_scores_2026_정제_행수():
    assert len(정제된_df) == 100


def test_반_종류():
    assert set(정제된_df["반"].unique()) == {"1반", "2반"}


def test_반별_합계와_전체_합계():
    반별_점수_합계 = 정제된_df.groupby("반")["점수"].sum().sum()
    전체_점수_합계 = 정제된_df["점수"].sum()
    assert 반별_점수_합계 == 전체_점수_합계


def test_mini_1반_평균():
    평균 = mini_정제_df[mini_정제_df["반"] == "1반"]["점수"].mean()
    assert 평균 == 80.0
import pandas as pd
import pytest

from analysis import 정제

df = pd.read_csv("scores_2026.csv")
정제된_df = 정제(df)
