import pytest
import os
from pro_filer.actions.main_actions import find_duplicate_files  # NOQA

@pytest.fixture
def context(tmp_path):
    file1 = tmp_path / "my_fav_song.txt"
    file1.write_text("Living on a Prayer")

    file2 = tmp_path / "my_fav_singer.txt"
    file2.write_text("Bon Jovi")

    file3 = tmp_path / "person1_fav_songs.txt"
    file3.write_text("Shelter, The Final Countdown")

    file4 = tmp_path / "person2_fav_songs.txt"
    file4.write_text("Living on a Prayer")

    file5 = tmp_path / "person3_fav_songs.txt"
    file5.write_text("Living on a Prayer")
    return {"all_files": [str(file1), str(file2), str(file3), str(file4), str(file5)]}


def test_find_duplicate_files_correct_behavior(context):
    result = find_duplicate_files(context)

    expected_files = [
        ('my_fav_song.txt', 'person2_fav_songs.txt'),
        ('my_fav_song.txt', 'person3_fav_songs.txt'),
        ('person2_fav_songs.txt', 'person3_fav_songs.txt')
    ]
    
    result_files = [(os.path.basename(file1), os.path.basename(file2)) for file1, file2 in result]

    assert result_files == expected_files


def test_find_duplicate_files_no_existent(context):
    context["all_files"].append("inexistent_file.txt")

    with pytest.raises(ValueError):
        find_duplicate_files(context)