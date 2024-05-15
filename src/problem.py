from pathlib import Path
import json
import os
import tempfile
import typing
import zipfile

from testcase import TestCase


class Problem:
    def __init__(self, title: str) -> None:
        self.title = title
        self.spj = False
        self.testcases: typing.Dict[str, TestCase] = {}

    def add_testcase(self, testcase: TestCase):
        """Add a testcase for this problem."""
        self.testcases[testcase] = testcase

    def as_dict(self) -> dict:
        return {
            "spj": self.spj,
            "testcases": {
                testcase.id: testcase.as_dict() for testcase in self.testcases.values()
            },
        }

    def extract_as_files(self, dirname: typing.Optional[str]=None) -> None:
        """Save problem in a directory.

        dirname: default is `./PROBLEM_TITLE`
        """
        dir_path = Path(dirname) if dirname is not None else Path(f'./{self.title}')
        info_filename = 'info'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for testcase in self.testcases.values():
            testcase.extract_as_files(dir=dir_path)
        with open(dir_path / info_filename, 'w') as f:
            json.dump(self.as_dict(), f, ensure_ascii=True)

    def extract_as_zip(self, filename: typing.Optional[str]=None) -> None:
        """Save problem as .zip file

        filename: default is `./PROBLEM_TITLE.zip`
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = Path(filename) if filename is not None else Path(f'./{self.title}.zip')
            dir_path = Path(tmp_dir)
            self.extract_as_files(dir_path)
            with zipfile.ZipFile(zip_path, 'w') as fzip:
                for basename in os.listdir(dir_path):
                    fzip.write(filename=dir_path/basename, arcname=basename)