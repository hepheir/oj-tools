from pathlib import Path
import hashlib
import json
import os
import tempfile
import typing
import zipfile


__all__ = [
    'LONG_LONG_SIZE',
    'INTEGER_SIZE',
    'TestCase',
    'Problem'
]


LONG_LONG_SIZE = 2305843009213693952
INTEGER_SIZE = 2147483648


class TestCase:
    __auto_increment__ = 0

    @classmethod
    def _auto_id(cls) -> int:
        cls.__auto_increment__ += 1
        return cls.__auto_increment__

    def __init__(self, id: str = None, auto_increment: bool = True) -> None:
        if id is None:
            assert auto_increment, "provide id, or enable auto_increment"
            id = str(self._auto_id())
        self._id = id
        self._input = ''
        self._output = ''

    def __hash__(self) -> int:
        return hash(self._id)

    @property
    def input(self) -> str:
        """content of input data."""
        return self._input

    @input.setter
    def input(self, s: str) -> None:
        self._input = s

    @property
    def output(self) -> str:
        """content of output data."""
        return self._output

    @output.setter
    def output(self, s: str) -> None:
        self._output = s

    @property
    def input_size(self) -> int:
        """Length of input data."""
        return len(self._input)

    @property
    def output_size(self) -> int:
        """Length of output data."""
        return len(self._output)

    @property
    def input_name(self) -> str:
        """A filename for the input."""
        return f'{self._id}.in'

    @property
    def output_name(self) -> str:
        """A filename for the output."""
        return f'{self._id}.out'

    @property
    def stripped_output_md5(self) -> str:
        md5 = hashlib.md5()
        md5.update(self.output.strip().encode())
        return md5.hexdigest()

    def as_dict(self) -> dict:
        return {
            "stripped_output_md5": self.stripped_output_md5,
            "input_size": self.input_size,
            "output_size": self.output_size,
            "input_name": self.input_name,
            "output_name": self.output_name,
        }

    def extract_as_file(self, dir='./') -> None:
        """Save testcase as `input_name` and `output_name` in a specific directory."""
        dir_path = Path(dir)
        with open(dir_path / self.input_name, 'w') as f:
            f.write(self.input)
        with open(dir_path / self.output_name, 'w') as f:
            f.write(self.output)


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
