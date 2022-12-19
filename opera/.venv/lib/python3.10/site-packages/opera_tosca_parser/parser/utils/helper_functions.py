from pathlib import Path
from tarfile import is_tarfile
from typing import Union
from zipfile import is_zipfile


def determine_archive_format(path: Union[str, Path]) -> str:
    """
    The main CLI method to be called
    :param path: Path to archive file
    :return: Name of the archive format (zip, tar)
    """
    if is_tarfile(path):
        return "tar"
    elif is_zipfile(path):
        return "zip"
    else:
        raise Exception(
            f"Unsupported archive format: '{path}'. The packaging format should be one of: zip, tar."
        )
