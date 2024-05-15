from pathlib import Path
import hashlib
import textwrap


class TestCaseIO:
    def __init__(self) -> None:
        self._content = ''

    def __str__(self) -> str:
        return self._content

    def __len__(self) -> int:
        return len(self._content)

    def from_text(self, text: str, dedent=False, strip=True):
        self._content = text
        self._post_process(dedent=dedent, strip=strip)

    def from_file(self, file_path: str, dedent=False, strip=True):
        with open(file_path, 'r') as f:
            self._content = f.read()
        self._post_process(dedent=dedent, strip=strip)

    def extract_as_file(self, file_path: str) -> None:
        with open(file_path, 'w') as f:
            f.write(self._content)

    def _post_process(self, dedent: bool, strip: bool) -> None:
        if dedent:
            self._content = textwrap.dedent(self._content)
        if strip:
            self._content = self._content.strip()


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
        self._input = TestCaseIO()
        self._output = TestCaseIO()

    def __hash__(self) -> int:
        return hash(self._id)

    @property
    def id(self) -> str:
        return self._id

    @property
    def input(self) -> TestCaseIO:
        """input data."""
        return self._input

    @property
    def output(self) -> TestCaseIO:
        """output data."""
        return self._output

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
        md5.update(str(self.output).strip().encode())
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
        self._input.extract_as_file(dir_path / self.input_name)
        self._output.extract_as_file(dir_path / self.output_name)
