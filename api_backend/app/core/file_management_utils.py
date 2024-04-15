import zipfile
from io import BytesIO
from typing import Any, Dict, List


def zip_files(files: List[Dict[str, Any]], zip_filename: str) -> bytes:
    """
    Zip files and return a StreamingResponse
    :param files: list of files to zip, each file is a dict with keys: name, data, extension
    :param zip_filename: the name of the zip file
    :return: a StreamingResponse
    reference: https://www.tutorialsbuddy.com/how-to-zip-multiple-files-in-python-for-download-using-fastapi
    """
    io = BytesIO()
    zip_filename = f"{zip_filename}.zip" if not zip_filename.endswith(".zip") else zip_filename
    with zipfile.ZipFile(io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        for file in files:
            zip.writestr(f"{file['name']}.{file['extension']}", file['data'])
        zip.close()
    return io.getvalue()
