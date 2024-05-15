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
