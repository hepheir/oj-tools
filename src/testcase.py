from pathlib import Path
import hashlib


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

    @property
    def output(self) -> str:
        """content of output data."""
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
