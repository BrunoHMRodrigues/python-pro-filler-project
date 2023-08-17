import pytest
from datetime import datetime
from unittest.mock import patch
from pro_filer.actions.main_actions import show_details

def test_show_details_correct_file(capsys):
    file_path = "path/to/your/test_file.png"
    
    context = {
        "base_path": file_path
    }

    # Use o decorador patch para substituir as funções relacionadas ao sistema de arquivos
    with patch("os.path.exists") as mock_exists, \
         patch("os.path.getsize") as mock_getsize, \
         patch("os.path.isdir") as mock_isdir, \
         patch("os.path.splitext") as mock_splitext, \
         patch("os.path.getmtime") as mock_getmtime:
         
        # Configura os retornos simulados das funções mockadas
        mock_exists.return_value = True
        mock_getsize.return_value = 22438
        mock_isdir.return_value = False  # Simula que não é um diretório
        mock_splitext.return_value = ("test_file", ".png")
        mock_getmtime.return_value = 1673484000  # Timestamp fictício

        show_details(context)
        captured = capsys.readouterr()

    file_name = "test_file.png"
    file_size = 22438
    file_extension = ".png"
    file_type = "file"
    last_modified_date = datetime.fromtimestamp(1673484000).strftime("%Y-%m-%d")

    expected_output = (
        f"File name: {file_name}\n"
        f"File size in bytes: {file_size}\n"
        f"File type: {file_type}\n"
        f"File extension: {file_extension}\n"
        f"Last modified date: {last_modified_date}\n"
    )

    assert captured.out == expected_output


def test_show_details_correct_dir(capsys):
    file_path = "path/to/your/dir"
    
    context = {
        "base_path": file_path
    }

    # Use o decorador patch para substituir as funções relacionadas ao sistema de arquivos
    with patch("os.path.exists") as mock_exists, \
         patch("os.path.getsize") as mock_getsize, \
         patch("os.path.isdir") as mock_isdir, \
         patch("os.path.splitext") as mock_splitext, \
         patch("os.path.getmtime") as mock_getmtime:
         
        # Configura os retornos simulados das funções mockadas
        mock_exists.return_value = True
        mock_getsize.return_value = 12490
        mock_isdir.return_value = True  # Simula que é um diretório
        mock_splitext.return_value = ("dir", "")
        mock_getmtime.return_value = 1673484000  # Timestamp fictício

        show_details(context)
        captured = capsys.readouterr()

    file_name = "dir"
    file_size = 12490
    file_extension = "[no extension]"
    file_type = "directory"
    last_modified_date = datetime.fromtimestamp(1673484000).strftime("%Y-%m-%d")

    expected_output = (
        f"File name: {file_name}\n"
        f"File size in bytes: {file_size}\n"
        f"File type: {file_type}\n"
        f"File extension: {file_extension}\n"
        f"Last modified date: {last_modified_date}\n"
    )

    assert captured.out == expected_output


def test_show_details_no_existent(capsys):
    file_path = "path/to/your/no_file_exist.png"
    
    context = {
        "base_path": file_path
    }

    show_details(context)
    captured = capsys.readouterr()
    assert captured.out == "File 'no_file_exist.png' does not exist\n"