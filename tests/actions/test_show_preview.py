import pytest
from pro_filer.actions.main_actions import show_preview  # NOQA

all_files_data = ["src/__init__.py", "src/app.py", "src/utils/__init__.py"]
all_files_data_more_than_five = [
    "src/__init__.py",
    "src/app.py",
    "src/model/model_calculator.py",
    "src/service/service_calculator.py",
    "src/controller/controller_calculator.py",
    "src/utils/__init__.py",
    "src/tests/test_calculator.py"
]

all_dirs_data = [ "src", "src/model"]
all_dirs_data_more_than_five = [
    "src",
    "src/model",
    "src/service",
    "src/controller",
    "src/utils",
    "src/tests"
]


def test_show_preview_with_no_all_files():
    context = {
        "all_dirs": all_dirs_data
    }
    with pytest.raises(KeyError):
        show_preview(context)


def test_show_preview_with_no_all_dirs():
    context = {
        "all_files": all_files_data
    }
    with pytest.raises(KeyError):
        show_preview(context)


def test_show_preview_with_no_files_to_analyze(capsys):
    context = {
        "all_files": [],
        "all_dirs": []
    }
    show_preview(context)
    captured = capsys.readouterr()
    assert captured.out == "Found 0 files and 0 directories\n"


def test_show_preview_correct_behavior(capsys):
    context = {
        "all_files": all_files_data,
        "all_dirs": all_dirs_data
    }
    show_preview(context)
    captured = capsys.readouterr()

    expected_output = (
        "Found 3 files and 2 directories\n"
        f"First 5 files: {all_files_data}\n"
        f"First 5 directories: {all_dirs_data}\n"
    )

    assert captured.out == expected_output


def test_show_preview_correct_behavior_more_than_five(capsys):
    context = {
        "all_files": all_files_data_more_than_five,
        "all_dirs": all_dirs_data_more_than_five
    }
    show_preview(context)
    captured = capsys.readouterr()

    files = all_files_data_more_than_five[slice(0,5,1)]
    dirs = all_dirs_data_more_than_five[slice(0,5,1)]

    expected_output = (
        "Found 7 files and 6 directories\n"
        f"First 5 files: {files}\n"
        f"First 5 directories: {dirs}\n"
    )

    assert captured.out == expected_output
