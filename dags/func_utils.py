from ast import Pass
from operator import index
import os
from fnmatch2 import fnmatch2
from zipfile import ZipFile
import openpyxl
import csv
from pathlib import Path
from unidecode import unidecode
import shutil

def get_files(path: str, file_name: str):
    """Returns file list

    Args:
        path (str): Directory path
        file_name (str): file name or unix file regex

    Returns:
        _type_: list of files
    """
    files = [f.name for f in os.scandir(path) if f.is_file()]

    if file_name:
        files = [file for file in files if fnmatch2(file, file_name)]
    
    [print(f"Found {file}") for file in files]
    
    return files


def uncompress(file_name: str, pattern: str, path_to_extract:str):
    """Uncompress file

    Args:
        file_name (str): Compressed file name
        pattern (str): Wich file for uncompress
    """

    with ZipFile(file=file_name, mode="r") as zip:
        files_to_extract = [file_extract for file_extract in zip.filelist if (not pattern) or fnmatch2(file_extract.filename, pattern)]

        for file in files_to_extract:
            zip.extract(member=file.filename, path=path_to_extract)
            print(f"Extracted {file.filename} => {path_to_extract}")


def filter_files(path: str, pattern: str, match: bool=True)-> list:
    """Filter files

    Args:
        path (str): root path
        pattern (str): pattern for filter files
        match (bool, optional): match or files that dont match

    Returns:
        _type_: files filtered from pattern and match
    """

    files_filtered = []
    
    for root,dirs,files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            file_match = fnmatch2(full_path, pattern) or pattern in full_path

            if (match and file_match) or (not match and not file_match):
                files_filtered.append(full_path)
    
    print(f"Filtered files {path} with {pattern} match {match}")
    return files_filtered


def remove_files(files):
    [os.remove(file) for file in files]
    print(f"Removed files {files}")


def remove_directories(path):
    [shutil.rmtree(os.path.join(path, file)) for file in os.scandir(path) if os.path.isdir(file)]


def pre_process_spreadsheet(filename:str, sheet_name:str, remove_str:str, max_rows_to_remove:int=10):
    wb = openpyxl.load_workbook(filename)

    for sheet in wb.get_sheet_names():
        sh = wb.get_sheet_by_name(sheet)

        if sheet_name in sh.title.lower():
            print(f'Found {sheet_name}, removing')
            wb.remove_sheet(sh)
        else:
            count_rows = 0
            for row in sh.rows:
                if not row[0].value or remove_str.strip().lower() in str(row[0].value).lower():
                    sh.delete_rows(1)
                    print(f'Found blank or {remove_str} in row [{filename}, {sh.title}, {row[0].value}]')
                
                count_rows += 1

                if(count_rows >= max_rows_to_remove):
                    break
    
    wb.save(filename)
    print(f'Removed {sheet_name} from file {filename}')


def file_lowercase(path: str, filename: str):
    file_lowercase = filename.lower()
    os.rename(os.path.join(path, filename), os.path.join(path, file_lowercase))
    print(f"{path}/{filename} -> {path}/{file_lowercase}")

def convert_spredsheet_csv(filename:str):
    wb = openpyxl.load_workbook(filename)
    parent_dir = Path(filename).parent

    for sheet in wb:
        if ("capa" not in sheet.title.lower()) and ("indice" not in sheet.title.lower()):
            output_file = os.path.join(parent_dir,
                                        unidecode(
                                            sheet.title.strip().lower().replace(" ", "_").replace("/", "_")) + ".csv")
            if not os.path.exists(output_file):
                print(f"Processing {filename}[{sheet.title}]")
                with open(output_file, "w") as f:
                    csv_file = csv.writer(f, delimiter=",", quotechar='"')

                    for row in sheet.rows:
                        if row[0].value and "tabela" not in str(row[0].value).lower():
                            csv_file.writerow([cell.value for cell in row])
                    print(f"Spredsheet {filename} => {output_file}")
                print(f"Processed {filename}[{sheet.title}]")
            else:
                print(f"Skipped {filename}[{sheet.title}] already processed")
