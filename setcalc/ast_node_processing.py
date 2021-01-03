from __future__ import annotations
from abc import ABCMeta, abstractmethod
from collections import Counter
from enum import Enum
import functools
from pathlib import Path
import re
from typing import Union


class OperationTypes(str, Enum):
    EQ = 'EQ'
    LE = 'LE'
    GR = 'GR'


def normalize_path(file_path: Union[str, Path]) -> Path:
    """
    Given a string containing a path to file, return a Path
    object. If a Path object is provided - it just passes though the function.
    """
    if isinstance(file_path, Path):
        return file_path
    return Path(file_path).expanduser().resolve()


@functools.lru_cache
def get_numbers_set_from_file(file_path: Path) -> set[int]:
    """
    Read a file, return the set of numbers it contained.
    Results are cached to speed up getting data for already processed files
    at the expense of memory.
    """
    file_path = normalize_path(file_path)
    return {
        int(stripped_line)
        for stripped_line in map(str.strip, file_path.open())
        if re.search(r'^\d+$', stripped_line)}


def compute_number_counts(sets_list: list[set[int]]) -> Counter:
    """
    Count an return the number of occurrences of all numbers in
    all of the provided sets.
    """
    res = Counter(sets_list.pop())
    for s in sets_list:
        res += Counter(s)

    return res


def create_operation(
        typ: OperationTypes,
        target_count: int,
        sets_list: list[Union[str, ExpressionResult]]) -> Operation:
    cls = None
    if typ == OperationTypes.EQ.value:
        cls = EQOperation
    elif typ == OperationTypes.LE.value:
        cls = LEOperation
    elif typ == OperationTypes.GR.value:
        cls = GROperation

    assert cls is not None, f'Invalid operation type: {typ}'

    return cls(target_count, sets_list)


class ExpressionResult(set):
    """
    A type alias for a set containing the results of the expression
    evaluation
    """


class Operation(metaclass=ABCMeta):
    def __init__(self,
                 target_count: int,
                 sets_list: list[Union[str, ExpressionResult]]) -> None:
        assert (target_count > 0), f'"{target_count}" must be a posive integer'
        self.target_count = target_count
        self.sets_list = sets_list

    def __call__(self) -> ExpressionResult:
        return self.execute()

    def execute(self) -> ExpressionResult:
        operands_list = []
        for s in self.sets_list:
            # this is a result of an operation having been applied to a
            # subexpression
            if isinstance(s, ExpressionResult):
                operands_list.append(s)
            # otherwise, expect a path to a file
            else:
                operands_list.append(
                    get_numbers_set_from_file(normalize_path(s)))

        return self._do_operation(operands_list)

    @abstractmethod
    def _do_operation(
            self,
            sets_list: list[Union[set[int], ExpressionResult]]) -> ExpressionResult:
        pass


class EQOperation(Operation):
    def _do_operation(
            self,
            operands_list: list[Union[set[int], ExpressionResult]]) -> ExpressionResult:
        number_counts = compute_number_counts(operands_list)
        return ExpressionResult(
            num for num, count in number_counts.items()
            if count == self.target_count)


class LEOperation(Operation):
    def _do_operation(
            self,
            operands_list: list[Union[set[int], ExpressionResult]]) -> ExpressionResult:
        number_counts = compute_number_counts(operands_list)
        return ExpressionResult(
            num for num, count in number_counts.items()
            if count < self.target_count)


class GROperation(Operation):
    def _do_operation(
            self,
            operands_list: list[Union[set[int], ExpressionResult]]) -> ExpressionResult:
        number_counts = compute_number_counts(operands_list)
        return ExpressionResult(
            num for num, count in number_counts.items()
            if count > self.target_count)
