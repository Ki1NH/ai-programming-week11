import pytest
from load_scores import load_scores

# [정상 ①] 평범한 파일 읽기
def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5

# [정상 ②] 빈 줄이 섞인 파일 처리 (임시 파일 생성 후 테스트)
def test_빈_줄은_건너뛴다(tmp_path):
    csv_file = tmp_path / "blank.csv"
    csv_file.write_text("name,score\n김철수,85\n\n이영희,92\n", encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert len(kept) == 2

# [정상 ③] 이름에 쉼표가 포함된 경우 처리
def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    csv_file = tmp_path / "comma.csv"
    csv_file.write_text('name,score\n"Kim, Min",90\n', encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert len(kept) == 1
    assert kept[0][0] == "Kim, Min"

# [예외 ①] 없는 파일 입력 시 오류 발생 확인
def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")

# [예외 ②] 헤더만 있는 빈 파일 처리
def test_헤더만_있으면_빈_결과():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []

# [경계 ①~③] 0점, 100점, 101점 등 경계값 한 번에 검증
@pytest.mark.parametrize("score, is_valid", [
    (-1,  False),
    (0,   True),
    (1,   True),
    (99,  True),
    (100, True),
    (101, False),
])
def test_점수_경계값(tmp_path, score, is_valid):
    csv_file = tmp_path / "boundary.csv"
    csv_file.write_text(f"name,score\n홍길동,{score}\n", encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert (len(kept) == 1) == is_valid

def test_이름이_비어있으면_건너뛴다(tmp_path):
    csv_file = tmp_path / "no_name.csv"
    csv_file.write_text("name,score\n,85\n", encoding="utf-8")
    kept, skipped = load_scores(str(csv_file))
    assert kept == []
    assert skipped[0][2] == "이름이 비어 있음"