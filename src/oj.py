from pathlib import Path
import json
import os
import tempfile
import typing
import zipfile

from testcase import TestCase


__all__ = [
    'LONG_LONG_SIZE',
    'INTEGER_SIZE',
    'TestCase',
    'Problem'
]


LONG_LONG_SIZE = 2305843009213693952
INTEGER_SIZE = 2147483648


class Problem:
    def __init__(self, title: str) -> None:
        self.title = title
        self.spj = False
        self.testcases: typing.Dict[str, TestCase] = {}

    def add_testcase(self, testcase: TestCase):
        """Add a testcase for this problem."""
        self.testcases[testcase.id] = testcase

    def as_dict(self) -> dict:
        return {
            "spj": self.spj,
            "testcases": {
                key: val.as_dict() for key, val in self.testcases.items()
            },
        }

    def extract_as_zip(self, filename: typing.Optional[str]=None) -> None:
        """Save problem as .zip file

        filename: default is `./PROBLEM_TITLE.zip`
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = Path(filename) if filename is not None else Path(f'./{self.title}.zip')
            dir_path = Path(tmp_dir)
            info_filename = 'info'

            for testcase in self.testcases.values():
                testcase.extract_as_file(dir=dir_path)

            with open(dir_path / info_filename, 'w') as f:
                json.dump(self.as_dict(), f, ensure_ascii=True)

            with zipfile.ZipFile(zip_path, 'w') as fzip:
                for testcase in self.testcases.values():
                    fzip.write(filename=dir_path / testcase.input_name, arcname=testcase.input_name)
                    fzip.write(filename=dir_path / testcase.output_name, arcname=testcase.output_name)
                fzip.write(filename=dir_path / info_filename, arcname=info_filename)
