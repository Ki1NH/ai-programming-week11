'''

아래 함수의 단위 테스트를 pytest로 작성해 주세요.

정상 · 예외 · 경계값을 모두 포함해 주세요.



import csv



MIN_SCORE = 0

MAX_SCORE = 100





def load_scores(path):

    """성적 CSV를 읽어 (유효한 목록, 건너뛴 줄 기록) 을 돌려준다."""

    kept = []

    skipped = []



    with open(path, "r", encoding="utf-8-sig", newline="") as f:

        reader = csv.reader(f)

        for line_no, row in enumerate(reader, start=1):

            if line_no == 1:              # 헤더

                continue

            if not row:                   # 빈 줄 — 기록하지 않는다

                continue



            원본 = ",".join(row)



            if len(row) != 2:

                skipped.append((line_no, 원본, "열 개수가 2가 아님"))

                continue



            name = row[0].strip()

            raw = row[1].strip()



            if name == "":

                skipped.append((line_no, 원본, "이름이 비어 있음"))

                continue

            if raw == "":

                skipped.append((line_no, 원본, "점수가 비어 있음"))

                continue



            try:

                score = int(raw)

            except ValueError:

                skipped.append((line_no, 원본, "점수가 정수가 아님"))

                continue



            if score < MIN_SCORE or score > MAX_SCORE:

                skipped.append((line_no, 원본, "점수가 0~100 밖"))

                continue



            kept.append((name, score))



    return kept, skipped





if __name__ == "__main__":

    import sys



    path = sys.argv[1] if len(sys.argv) > 1 else "scores.csv"

    kept, skipped = load_scores(path)

    print(f"읽은 줄 : {len(kept)}개")

    for name, score in kept:

        print(f"  {name} {score}")

    print(f"건너뛴 줄 : {len(skipped)}개")

    for line_no, 원본, 이유 in skipped:

        print(f"  {line_no}행  {원본}   ← {이유}")

'''

import pytest

from load_scores import load_scores


def test_loads_valid_rows_and_preserves_duplicate_names(tmp_path):
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(
        '\ufeffname,score\n  홍길동  , 88 \n"Kim, Min",0\n홍길동,100\n',
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_file)

    assert kept == [("홍길동", 88), ("Kim, Min", 0), ("홍길동", 100)]
    assert skipped == []


def test_header_only_file_returns_empty_results(tmp_path):
    csv_file = tmp_path / "header_only.csv"
    csv_file.write_text("name,score\n", encoding="utf-8")

    assert load_scores(csv_file) == ([], [])


def test_blank_lines_are_ignored_without_being_recorded(tmp_path):
    csv_file = tmp_path / "blank_lines.csv"
    csv_file.write_text("name,score\n\n학생,75\n\n", encoding="utf-8")

    kept, skipped = load_scores(csv_file)

    assert kept == [("학생", 75)]
    assert skipped == []


@pytest.mark.parametrize(
    ("score", "expected_kept", "expected_reason"),
    [
        (-1, [], "점수가 0~100 밖"),
        (0, [("학생", 0)], None),
        (100, [("학생", 100)], None),
        (101, [], "점수가 0~100 밖"),
    ],
)
def test_score_range_boundaries(tmp_path, score, expected_kept, expected_reason):
    csv_file = tmp_path / "boundary.csv"
    csv_file.write_text(f"name,score\n학생,{score}\n", encoding="utf-8")

    kept, skipped = load_scores(csv_file)

    assert kept == expected_kept
    if expected_reason is None:
        assert skipped == []
    else:
        assert skipped == [(2, f"학생,{score}", expected_reason)]


@pytest.mark.parametrize(
    ("row", "expected_reason"),
    [
        ("학생", "열 개수가 2가 아님"),
        ("학생,80,추가", "열 개수가 2가 아님"),
        (",80", "이름이 비어 있음"),
        ("   ,80", "이름이 비어 있음"),
        ("학생,", "점수가 비어 있음"),
        ("학생,   ", "점수가 비어 있음"),
        ("학생,팔십", "점수가 정수가 아님"),
        ("학생,80.5", "점수가 정수가 아님"),
        ("학생,-1", "점수가 0~100 밖"),
        ("학생,101", "점수가 0~100 밖"),
    ],
)
def test_invalid_rows_are_skipped_with_details(tmp_path, row, expected_reason):
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(f"name,score\n{row}\n", encoding="utf-8")

    kept, skipped = load_scores(csv_file)

    assert kept == []
    assert skipped == [(2, row, expected_reason)]


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")
