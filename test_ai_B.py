'''
아래 명세를 만족하는 함수의 단위 테스트를 pytest로 작성해 주세요.
정상 · 예외 · 경계값을 모두 포함해 주세요.

함수명: load_scores(path)
  ① 무엇을 받나       : 성적 CSV 파일 경로 (path)
  ② 무엇을 돌려주나   : (kept, skipped) 튜플 (kept는 유효한 (이름, 정수 점수) 목록, skipped는 건너뛴 줄의 (줄번호, 원본줄, 이유) 목록)
  ③ 실패하면 어떻게 하나 : 비정상 데이터(열 개수 오류, 빈 이름/점수, 정수 아님, 0~100 범위 밖)는 프로그램이 멈추지 않고 건너뛴 뒤 skipped에 기록하고, 빈 줄은 기록 없이 건너뜀
  ④ 쓰면 안 되는 것   : 비정상 데이터 발생 시 프로그램 강제 종료 금지, 동명이인 임의 삭제 금지
  ⑤ 예외 상황         : 파일이 없으면 FileNotFoundError를 그대로 발생시키고, 헤더(name,score)만 있는 빈 파일이면 ([], [])를 반환
  ⑥ 조건 · 제약       : 첫 줄은 헤더로 건너뛰며, 점수는 0 이상 100 이하의 정수만 유효한 것으로 인정함
'''
import pytest

from load_scores import load_scores


def test_loads_valid_scores_and_keeps_duplicate_names(tmp_path):
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(
        '\ufeffname,score\n  홍길동  , 88 \n"Kim, Min",0\n홍길동,100\n',
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_file)

    assert kept == [("홍길동", 88), ("Kim, Min", 0), ("홍길동", 100)]
    assert skipped == []


def test_header_only_file_returns_empty_results(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("name,score\n", encoding="utf-8")

    assert load_scores(csv_file) == ([], [])


def test_blank_lines_are_ignored(tmp_path):
    csv_file = tmp_path / "blank.csv"
    csv_file.write_text("name,score\n\n학생,75\n\n", encoding="utf-8")

    kept, skipped = load_scores(csv_file)

    assert kept == [("학생", 75)]
    assert skipped == []


@pytest.mark.parametrize(
    ("score", "expected_kept", "expected_skipped"),
    [
        (-1, [], [(2, "학생,-1", "점수가 0~100 밖")]),
        (0, [("학생", 0)], []),
        (100, [("학생", 100)], []),
        (101, [], [(2, "학생,101", "점수가 0~100 밖")]),
    ],
)
def test_score_boundaries(
    tmp_path, score, expected_kept, expected_skipped
):
    csv_file = tmp_path / "boundary.csv"
    csv_file.write_text(f"name,score\n학생,{score}\n", encoding="utf-8")

    assert load_scores(csv_file) == (expected_kept, expected_skipped)


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("학생", "열 개수가 2가 아님"),
        ("학생,80,추가", "열 개수가 2가 아님"),
        (",80", "이름이 비어 있음"),
        ("   ,80", "이름이 비어 있음"),
        ("학생,", "점수가 비어 있음"),
        ("학생,   ", "점수가 비어 있음"),
        ("학생,팔십", "점수가 정수가 아님"),
        ("학생,80.5", "점수가 정수가 아님"),
    ],
)
def test_invalid_rows_are_skipped_with_details(tmp_path, row, reason):
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(f"name,score\n{row}\n", encoding="utf-8")

    assert load_scores(csv_file) == ([], [(2, row, reason)])


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")