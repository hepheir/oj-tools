from typing import Generic, Iterable, TypeVar

from oj.constants import *


T = TypeVar('T')


class Validator(Generic[T]):
    def validate_one(self, obj: T) -> bool:
        raise NotImplementedError

    def validate_all(self, iterable: Iterable[T]) -> bool:
        return all(map(self.validate_one, iterable))

    def validate_any(self, iterable: Iterable[T]) -> bool:
        return any(map(self.validate_one, iterable))


class RangeValidator(Generic[T], Validator[T]):
    def __init__(self, lo: T = None, hi: T = None) -> None:
        super().__init__()
        self.lo = lo
        self.hi = hi

    def validate_one(self, obj: T) -> bool:
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