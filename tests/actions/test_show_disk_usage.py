import pytest
import os
from pro_filer.actions.main_actions import show_disk_usage

@pytest.fixture
def context(tmp_path):
    file1 = tmp_path / "songs.txt"
    file1.write_text("Lista de músicas")

    file2 = tmp_path / "singers.txt"
    file2.write_text("Lista de cantores")

    file3 = tmp_path / "fav_song.txt"
    file3.write_text("Living on a Prayer - Bon Jovi")
    return {"all_files": [str(file1), str(file2), str(file3)]}


def test_show_disk_usage_correct_behavior(context, capsys):
    
    show_disk_usage(context)

    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    assert "fav_song.txt" in output_lines[0]
    assert "songs.txt" in output_lines[1]
    assert "singers.txt" in output_lines[2]
    assert "Total size: 63" in output_lines[3]
    assert len(output_lines) == 4

def test_show_disk_usage_empty(capsys):
    context = {"all_files": []}
    show_disk_usage(context)

    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    assert "Total size:" in output_lines[0]
    assert "0" in output_lines[0]
    assert len(output_lines) == 1


