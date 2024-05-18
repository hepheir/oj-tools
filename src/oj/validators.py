from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import *

from oj.constants import *


__all__ = [
    'ValidationError',
    'AbstractValidator',
    'RangeValidator',
    'TimeComplexityValidator',
    'IntCoverageValidator',
]


T = TypeVar('T')


class ValidationError(Exception):
    pass


class AbstraceValidator(Generic[T], ABC):
    def __init__(self, raise_exception=True) -> None:
        super().__init__()
        self._raise_exception = raise_exception

    @abstractmethod
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


class RangeValidator(AbstraceValidator[float]):
    def __init__(self,
                 lo: float=None,
                 hi: float=None,
                 raise_exception=True) -> None:
        """특정 범위에 있는지를 검사한다.

        lo 이상 hi 이하의 범위에 있지 않다면 예외를 발생시킨다.
        """
        super().__init__(raise_exception=raise_exception)
        self.lo = lo
        self.hi = hi
        if lo is not None and hi is not None and lo > hi:
            raise ValueError('하한이 상한보다 높을 수 없습니다.')

    def __validator__(self, x: float) -> bool:
        if (self.lo is not None) and (self.lo > x):
            return False
        if (self.hi is not None) and (self.hi < x):
            return False
        return True


class TimeComplexityValidator(RangeValidator[float]):
    def __init__(self,
                 seconds: float,
                 T_per_second: float=5e8,
                 raise_exception=True) -> None:
        super().__init__(hi=T_per_second * seconds,
                         raise_exception=raise_exception)



@dataclass
class Rule:
    lo: Optional[float]
    hi: Optional[float]
    allow: bool


class RuleBasedRangeValidator(AbstraceValidator[float]):
    def __init__(self, rules: Iterable[Rule], raise_exception=True) -> None:
        """나중에 추가된 규칙이 더 높은 우선 순위를 갖는다."""
        super().__init__(raise_exception=raise_exception)
        self._rules: List[Rule] = [*rules]

    def __validator__(self, x: float) -> bool:
        for rule in self._rules:
            if rule.allow and not self._is_in_range(x, rule.lo, rule.hi):
                return False
            if not rule.allow and self._is_in_range(x, rule.lo, rule.hi):
                return False
        return True

    def _is_in_range(self, x: float, lo: float, hi: float) -> bool:
        if (lo is not None) and (lo > x):
            return False
        if (hi is not None) and (hi < x):
            return False
        return True


class IntCoverageValidator(RuleBasedRangeValidator):
    def __init__(self,
                 allow_int32=None,
                 allow_uint32=None,
                 allow_int64=None,
                 allow_uint64=None,
                 allow_natural=None,
                 raise_exception=True) -> None:
        rules = [
            rule
            for rule in [
                Rule(lo=INT32_MIN_VALUE,    hi=INT32_MAX_VALUE,     allow=allow_int32),
                Rule(lo=UINT32_MIN_VALUE,   hi=UINT32_MAX_VALUE,    allow=allow_uint32),
                Rule(lo=INT64_MIN_VALUE,    hi=INT64_MAX_VALUE,     allow=allow_int64),
                Rule(lo=UINT64_MIN_VALUE,   hi=UINT64_MAX_VALUE,    allow=allow_uint64),
                Rule(lo=1,                  hi=None,                allow=allow_natural),
            ]
            if rule.allow is not None
        ]

        if len(rules) == 0:
            raise ValueError("적어도 하나 이상의 제약조건을 추가해야 합니다.")

        super().__init__(rules=rules,
                         raise_exception=raise_exception)
