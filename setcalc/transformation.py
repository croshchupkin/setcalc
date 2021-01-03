from __future__ import annotations
from typing import Union

from lark import (
    Transformer,
    Tree,
    Token)

from .ast_node_processing import (
    ExpressionResult,
    create_operation)


class SetCalcTransformer(Transformer):
    def expression(self, items: list[Union[Tree, Token]]) -> ExpressionResult:
        op_type = items[0].value
        target_count = int(items[1].value)
        sets_list = [
            i if isinstance(i, ExpressionResult) else i.value
            for i in items[2].children]
        operation = create_operation(op_type, target_count, sets_list)
        return operation()

    def FILENAME(self, file_path: Token) -> str:
        file_path.value = file_path.value.strip('"')
        return file_path
