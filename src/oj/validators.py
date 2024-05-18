from typing import *
import abc

from oj.constants import *


T = TypeVar('T')


class ValidationError(Exception):
    pass


class AbstraceValidator(Generic[T], abc.ABC):
    def __init__(self, raise_exception = False) -> None:
        super().__init__()
        self._raise_exception = raise_exception

    @abc.abstractmethod
    def __validator__(self, obj: T) -> bool:
        ...

    def validate(self, *objs: Tuple[T], method: Callable[[Iterable[T]], bool]=all) -> bool:
        is_validated = method(map(self.__validator__, objs))
        if is_validated or not self._raise_exception:
            return is_validated
        raise ValidationError(f'{objs} did not passed the validation.')

    def validate_all(self, iterable: Iterable[T]) -> bool:
        return self.validate(*iterable, method=all)

    def validate_any(self, iterable: Iterable[T]) -> bool:
        return self.validate(*iterable, method=any)


class RangeValidator(Generic[T], AbstraceValidator[T]):
    def __init__(self, lo: T = None, hi: T = None, raise_exception = False) -> None:
        """특정 범위에 있는지를 검사한다.

        lo 이상 hi 이하의 범위에 있지 않다면 예외를 발생시킨다.
        """
        super().__init__(raise_exception=raise_exception)
        self.lo = lo
        self.hi = hi

    def __validator__(self, obj: T) -> bool:
        if (self.lo is not None) and (self.lo > obj):
            return False
        if (self.hi is not None) and (self.hi < obj):
            return False
        return True


# Built-in validators

int32_converage_validator = RangeValidator(lo=INT32_MIN_VALUE, hi=INT32_MAX_VALUE)
uint32_converage_validator = RangeValidator(lo=UINT32_MIN_VALUE, hi=UINT32_MAX_VALUE)

int64_converage_validator = RangeValidator(lo=INT64_MIN_VALUE, hi=INT64_MAX_VALUE)
uint64_converage_validator = RangeValidator(lo=UINT64_MIN_VALUE, hi=UINT64_MAX_VALUE)

natural_converage_validator = RangeValidator(lo=1)

big_o_converage_validator = RangeValidator(hi=int(5e7))
