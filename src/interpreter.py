from re import Pattern
import re

from typing import List, Tuple
from src import exception


class Interpreter:
    # <比較演算子>
    COMPARE_OPERATOR = ">=|<=|==|!=|>|<"
    # <ORビット演算式>
    OR_OPERATOR = "\\|"
    # <ANDビット演算子>
    AND_OPERATOR = "\\&"
    # <和差演算子>
    ADD_SUB_OPERATOR = "(\\+|-)"
    # <乗除演算子>
    MUL_DIV_OPERATOR = "\\*|/"
    # <論理演算子>
    LOGICAL_OPERATOR = "かつ|または"

    OPERATORS = f"{COMPARE_OPERATOR}|{OR_OPERATOR}|{AND_OPERATOR}|{ADD_SUB_OPERATOR}|{MUL_DIV_OPERATOR}|{LOGICAL_OPERATOR}"


    PALENTHESIS_START = "^\\("
    PALENTHESIS_END = "^\\)"

    # <正数字> ::= 1-9
    POSITIVE_NUM = "1-9"
    # <数字> ::= 0 | <正数字>
    NUM = "0-9"
    # <英字> ::= a-z | A-Z
    ALPHABET = "A-z"
    # <数値> ::= <正数字><数値> | -<正数字><数値> | <数字>
    INT_VAL = "-?" + f"[{NUM}]+"
    REAL_VAL = f"{INT_VAL}(?:\\.[{NUM}]+)?"
    NUM_VAL = f"({REAL_VAL})"
    # <名前>
    NAME = f"[{ALPHABET}]([{ALPHABET}]|[{NUM}])*"
    # <被演算子>
    OPERAND = f"({NUM_VAL}|{NAME})"

    # <型>
    INT_TYPE = "整数型"
    REAL_TYPE = "実数型"
    STR_TYPE = "文字列型"
    BOOL_TYPE = "論理型"
    ARR_SUFFIX = "の配列"
    TYPE_MAP = {
        INT_TYPE: int,
        REAL_TYPE: float,
        STR_TYPE: str,
        BOOL_TYPE: bool,
        f"{INT_TYPE}{ARR_SUFFIX}": List[int],
        f"{REAL_TYPE}{ARR_SUFFIX}": List[float],
        f"{STR_TYPE}{ARR_SUFFIX}": List[str],
        f"{BOOL_TYPE}{ARR_SUFFIX}": List[bool],
    }

    operator_func_map = {
        "+": lambda val1, val2: val1 + val2,
        "-": lambda val1, val2: val1 - val2,
        "*": lambda val1, val2: val1 * val2,
        "/": lambda val1, val2: val1 / val2,
        "|": lambda val1, val2: val1 | val2,
        "&": lambda val1, val2: val1 & val2,
        ">": lambda val1, val2: val1 > val2,
        "<": lambda val1, val2: val1 < val2,
        ">=": lambda val1, val2: val1 >= val2,
        "<=": lambda val1, val2: val1 <= val2,
        "!=": lambda val1, val2: val1 != val2,
        "==": lambda val1, val2: val1 == val2,
        "かつ": lambda val1, val2: val1 and val2,
        "または": lambda val1, val2: val1 or val2,
    }
    operator_priority_map = {
        "+": ["*", "/"],
        "-": ["*", "/"],
        "*": [],
        "/": [],
        ">": ["+", "-", "*", "/"],
        "<": ["+", "-", "*", "/"],
        ">=": ["+", "-", "*", "/"],
        "<=": ["+", "-", "*", "/"],
        "==": ["+", "-", "*", "/"],
        "!=": ["+", "-", "*", "/"],
        "&": ["+", "-", "*", "/", ">", "<", ">=", "<=", "==", "!="],
        "|": ["+", "-", "*", "/", "&", ">", "<", ">=", "<=", "==", "!="],
        "かつ": ["+", "-", "*", "/", "&", "|", ">", "<", ">=", "<=", "==", "!="],
        "または": [
            "+",
            "-",
            "*",
            "/",
            "&",
            "|",
            ">",
            "<",
            ">=",
            "<=",
            "==",
            "!=",
            "かつ",
        ],
    }


    def __init__(self):
        self.name_val_map = {}
        self.name_type_map = {}
        self.complie_patterns()

    def complie_patterns(self):
        self.name_pattern = re.compile(self.NAME)
        self.num_val_pattern = re.compile(self.NUM_VAL)
        self.operand_pattern = re.compile(self.OPERAND)
        self.add_sub_operator_pattern = re.compile(self.ADD_SUB_OPERATOR)
        self.mul_div_operator_pattern = re.compile(self.MUL_DIV_OPERATOR)
        self.and_operator_pattern = re.compile(self.AND_OPERATOR)
        self.or_operator_pattern = re.compile(self.OR_OPERATOR)
        self.operators_pattern = re.compile(self.OPERATORS)

        self.parenthesis_start_pattern = re.compile(self.PALENTHESIS_START)
        self.parenthesis_end_pattern = re.compile(self.PALENTHESIS_END)

    def interpret_arithmetic_formula(
        self, line: str, stack: List[str] = None, pended_op=None
    ):
        result, remain = self.interpret_arithmetic_operand(line, stack)
        while True:
            res = self.process_operator(remain, stack, result, pended_op=pended_op)
            if not res:
                break
            result, remain = res
        return result, remain

    def process_operator(
        self,
        remain: str,
        stack: List[str],
        val,
        exception: exception.PatternException = None,
        pended_op: str = None,
    ):
        res = self.get_pattern_and_remain(self.operators_pattern, remain, exception)
        if not res:
            return None
        op, tmp_remain = res
        if pended_op is not None and pended_op in self.operator_priority_map[op]:
            return None
        else:
            remain = tmp_remain
        val2, tmp_remain = self.interpret_arithmetic_operand(remain, stack)
        # 優先度の高い演算子がある場合は先に計算
        res = self.get_pattern_and_remain(self.operators_pattern, tmp_remain)
        if res and res[0] in self.operator_priority_map[op]:
            val2, remain = self.interpret_arithmetic_formula(
                remain, stack, pended_op=op
            )
        else:
            remain = tmp_remain

        if stack is not None:
            stack.append(op)
        return self.operator_func_map[op](val, val2), remain

    def interpret_arithmetic_operand(self, line: str, stack: List[str] = None):
        res = self.get_pattern_and_remain(self.parenthesis_start_pattern, line)
        if res:
            _, remain = res
            val, remain = self.interpret_arithmetic_formula(remain, stack)
            _, remain = self.get_pattern_and_remain(
                self.parenthesis_end_pattern,
                remain,
                exception.InvalidParenthesisException,
            )
            return val, remain
        return self.interpret_operand(line, stack)

    def interpret_operand(self, line: str, stack: List[str] = None):
        res = self.get_pattern_and_remain(self.name_pattern, line)
        if res:
            name, remain = res
            if name not in self.name_val_map:
                raise exception.NameNotDefinedException(name)
            if stack is not None:
                stack.append(name)
            return self.name_val_map[name], remain
        num_val, remain = self.get_pattern_and_remain(
            self.num_val_pattern, line, exception.InvalidFormulaException
        )
        if stack is not None:
            stack.append(num_val)
        try:
            return int(num_val), remain
        except ValueError:
            return float(num_val), remain

    def get_pattern_and_remain(
        self, pattern: Pattern, target: str, exception: Exception = None
    ) -> Tuple[str, str]:
        matched = pattern.match(target)
        if not matched:
            if exception is None:
                return None
            else:
                raise exception(target)
        return target[matched.start() : matched.end()], target[matched.end() :].strip()
