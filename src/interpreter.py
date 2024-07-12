import re
from re import Pattern
from typing import List, Tuple

from src import exception
from src.lts.lts import LabeledTransitionSystem


class Interpreter:
    # <否定演算子>
    NOT_OPERATOR = "not"
    # <乗除演算子>
    MUL_DIV_MOD_OPERATOR = "\\*|/|mod|×|÷"
    # <和差演算子>
    ADD_SUB_OPERATOR = "\\+|-|＋|－"
    # <比較演算子>
    COMPARE_OPERATOR = "≧|≦|=|＝|≠|＞|＜|<|>"
    # <ANDビット演算子>
    AND_OPERATOR = "\\&"
    # <ORビット演算式>
    OR_OPERATOR = "\\|"
    # <論理演算子>
    LOGICAL_OPERATOR = "かつ|または"
    SINGLE_OPERATORS = f"{NOT_OPERATOR}|{ADD_SUB_OPERATOR}"
    OPERATORS = f"{COMPARE_OPERATOR}|{OR_OPERATOR}|{AND_OPERATOR}|{ADD_SUB_OPERATOR}|{MUL_DIV_MOD_OPERATOR}|{LOGICAL_OPERATOR}"

    PALENTHESIS_START = "^\\("
    PALENTHESIS_END = "^\\)"

    # <論理値>::= true | false
    LOGICAL_VALUE = "true|false"
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

    TYPE = f"^({INT_TYPE}|{REAL_TYPE}|{STR_TYPE}|{BOOL_TYPE})({ARR_SUFFIX})?"
    # <IF句>
    IF = "^if"
    ELSE = "^else"
    ELSEIF = "^elseif"
    ENDIF = "^endif$"

    COLON = "^[:,：]"
    COMMA = "^,"
    ASSIGN = "^<-|←|＜－"

    LOGICAL_VAL_MAP = {"true": True, "false": False}

    OPERATOR_FUNC_MAP = {
        "+": lambda val1, val2: val1 + val2,
        "＋": lambda val1, val2: val1 + val2,
        "-": lambda val1, val2: val1 - val2,
        "－": lambda val1, val2: val1 - val2,
        "*": lambda val1, val2: val1 * val2,
        "×": lambda val1, val2: val1 * val2,
        "mod": lambda val1, val2: val1 % val2,
        "/": lambda val1, val2: val1 / val2,
        "÷": lambda val1, val2: val1 / val2,
        "|": lambda val1, val2: val1 | val2,
        "&": lambda val1, val2: val1 & val2,
        "＞": lambda val1, val2: val1 > val2,
        ">": lambda val1, val2: val1 > val2,
        "＜": lambda val1, val2: val1 < val2,
        "<": lambda val1, val2: val1 > val2,
        "≧": lambda val1, val2: val1 >= val2,
        "≦": lambda val1, val2: val1 <= val2,
        "≠": lambda val1, val2: val1 != val2,
        "=": lambda val1, val2: val1 == val2,
        "＝": lambda val1, val2: val1 == val2,
        "かつ": lambda val1, val2: val1 and val2,
        "または": lambda val1, val2: val1 or val2,
    }
    SINGLE_OPERATOR_FUNC_MAP = {
        "not": lambda val: not val,
        "+": lambda val: +val,
        "＋": lambda val: +val,
        "-": lambda val: -val,
        "－": lambda val: -val,
    }
    OP_LV1 = ["not"]
    OP_LV2 = ["*", "/", "×", "÷", "mod"]
    OP_LV3 = ["+", "-", "＋", "－"]
    OP_LV4 = [">", "＞", "＜", "<", "≧", "≦", "=", "＝", "≠"]
    OP_LV5 = ["&"]
    OP_LV6 = ["|"]
    OP_LV7 = ["かつ"]
    OP_LV8 = ["または"]

    operator_priority_map = {
        "not": [],
        "+": OP_LV1 + OP_LV2,
        "＋": OP_LV1 + OP_LV2,
        "-": OP_LV1 + OP_LV2,
        "－": OP_LV1 + OP_LV2,
        "*": OP_LV1,
        "×": OP_LV1,
        "/": OP_LV1,
        "÷": OP_LV1,
        "mod": OP_LV1,
        "＞": OP_LV1 + OP_LV2 + OP_LV3,
        ">": OP_LV1 + OP_LV2 + OP_LV3,
        "＜": OP_LV1 + OP_LV2 + OP_LV3,
        "<": OP_LV1 + OP_LV2 + OP_LV3,
        "≧": OP_LV1 + OP_LV2 + OP_LV3,
        "≦": OP_LV1 + OP_LV2 + OP_LV3,
        "=": OP_LV1 + OP_LV2 + OP_LV3,
        "＝": OP_LV1 + OP_LV2 + OP_LV3,
        "≠": OP_LV1 + OP_LV2 + OP_LV3,
        "&": OP_LV1 + OP_LV2 + OP_LV3 + OP_LV4,
        "|": OP_LV1 + OP_LV2 + OP_LV3 + OP_LV4 + OP_LV5,
        "かつ": OP_LV1 + OP_LV2 + OP_LV3 + OP_LV4 + OP_LV5 + OP_LV6,
        "または": OP_LV1 + OP_LV2 + OP_LV3 + OP_LV4 + OP_LV5 + OP_LV6 + OP_LV7,
    }

    def __init__(self):
        self.name_val_map = {}
        self.name_type_map = {}
        self.lts = LabeledTransitionSystem()
        self.current_state = self.lts.get_init_state()
        self.complie_patterns()

    def complie_patterns(self):
        self.type_pattern = re.compile(self.TYPE)
        self.if_pattern = re.compile(self.IF)
        self.else_pattern = re.compile(self.ELSE)
        self.elseif_pattern = re.compile(self.ELSEIF)
        self.endif_pattern = re.compile(self.ENDIF)
        self.name_pattern = re.compile(self.NAME)
        self.num_val_pattern = re.compile(self.NUM_VAL)
        self.operand_pattern = re.compile(self.OPERAND)
        self.add_sub_operator_pattern = re.compile(self.ADD_SUB_OPERATOR)
        self.mul_div_mod_operator_pattern = re.compile(self.MUL_DIV_MOD_OPERATOR)
        self.and_operator_pattern = re.compile(self.AND_OPERATOR)
        self.or_operator_pattern = re.compile(self.OR_OPERATOR)
        self.operators_pattern = re.compile(self.OPERATORS)
        self.single_operators_pattern = re.compile(self.SINGLE_OPERATORS)
        self.logical_value_pattern = re.compile(self.LOGICAL_VALUE)

        self.parenthesis_start_pattern = re.compile(self.PALENTHESIS_START)
        self.parenthesis_end_pattern = re.compile(self.PALENTHESIS_END)
        self.colon_pattern = re.compile(self.COLON)
        self.comma_pattern = re.compile(self.COMMA)
        self.assign_pattern = re.compile(self.ASSIGN)

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
        return self.OPERATOR_FUNC_MAP[op](val, val2), remain

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
        res = self.get_pattern_and_remain(self.single_operators_pattern, line)
        if res:
            single_op, line = res
        else:
            single_op = None
        res = self.get_pattern_and_remain(self.logical_value_pattern, line)
        if res:
            val, remain = res
            val = self.LOGICAL_VAL_MAP[val]
            if single_op is not None:
                val = self.SINGLE_OPERATOR_FUNC_MAP[single_op](val)
            return val, remain
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
            val = int(num_val)
        except ValueError:
            val = float(num_val)
        if single_op is not None:
            val = self.SINGLE_OPERATOR_FUNC_MAP[single_op](val)
        return val, remain

    def get_pattern_and_remain(
        self, pattern: Pattern, target: str, exception: Exception = None
    ) -> Tuple[str, str]:
        target = target.strip()
        matched = pattern.match(target)
        if not matched:
            if exception is None:
                return None
            else:
                raise exception(target)
        return target[matched.start() : matched.end()], target[matched.end() :].strip()

    def process_var_assigns(self, remain):
        vars_list = []
        while True:
            name, remain = self.get_pattern_and_remain(
                self.name_pattern, remain, exception.NamePatternException
            )
            vars_list.append(name)
            res = self.get_pattern_and_remain(self.assign_pattern, remain)
            if res:
                _, remain = res
                val, remain = self.interpret_arithmetic_formula(remain)
                self.name_val_map[name] = val
            else:
                self.name_val_map[name] = None
            res = self.get_pattern_and_remain(self.comma_pattern, remain)
            if res:
                _, remain = res
                continue
            else:
                break
        return vars_list, remain

    def interpret_var_declare(self, line):
        res = self.get_pattern_and_remain(self.type_pattern, line)
        if not res:
            return None
        type_str, remain = res
        _, remain = self.get_pattern_and_remain(
            self.colon_pattern, remain, exception.DeclareException
        )
        vars, remain = self.process_var_assigns(remain)

        for var in vars:
            self.name_type_map[var] = type_str
        return remain

    def interpret_if_block(self, lines: List[str], indent: str = "", line_pointa=0):
        if len(lines) == 0 or (
            indent != "" and not self.check_indent(lines[line_pointa], indent)
        ):
            return line_pointa
        res = self.get_pattern_and_remain(self.if_pattern, lines[line_pointa])
        end_states = []
        if not res:
            return line_pointa
        _, remain = res
        child_indent = self.extract_indent(lines[line_pointa + 1])
        if len(indent) >= len(child_indent):
            raise exception.InvalidIndentException(line_num=line_pointa + 1)
        start_state = self.current_state
        state = self.lts.create_state()
        self.lts.add_transition(start_state, remain, state)
        self.current_state = state
        line_pointa = self.interpret_process(lines, child_indent, line_pointa + 1)
        end_states.append(self.current_state)
        while True:
            if len(lines) == 0:
                break
            res = self.get_pattern_and_remain(self.elseif_pattern, lines[line_pointa])
            if not res:
                break
            _, remain = res
            child_indent = self.extract_indent(lines[line_pointa + 1])
            if len(indent) >= len(child_indent):
                raise exception.InvalidIndentException(line_num=line_pointa + 1)
            state = self.lts.create_state()
            self.lts.add_transition(start_state, remain, state)
            self.current_state = state
            line_pointa = self.interpret_process(lines, child_indent, line_pointa + 1)
            end_states.append(self.current_state)
        if len(lines) <= line_pointa:
            raise exception.InvalidFormulaException()
        res = self.get_pattern_and_remain(self.else_pattern, lines[line_pointa])
        if res:
            child_indent = self.extract_indent(lines[line_pointa + 1])
            if len(indent) >= len(child_indent):
                raise exception.InvalidIndentException(line_num=line_pointa + 1)
            state = self.lts.create_state()
            self.lts.add_transition(start_state, "else", state)
            self.current_state = state
            line_pointa = self.interpret_process(
                lines, child_indent, line_pointa=line_pointa + 1
            )
            end_states.append(self.current_state)
        if len(lines) <= line_pointa:
            raise exception.InvalidFormulaException()
        res = self.get_pattern_and_remain(self.endif_pattern, lines[line_pointa])
        if not res:
            raise exception.InvalidIfBlockException(line_num=line_pointa)
        line_pointa += 1
        endif_state = self.lts.create_state()
        for end_state in end_states:
            self.lts.add_transition(end_state, "endif", endif_state)
        self.current_state = endif_state

        return line_pointa

    def interpret_process(self, lines: List[str], indent: str = "", line_pointa=0):
        while lines is not None and len(lines) != 0:
            print(line_pointa, "行目", lines[line_pointa])
            if self.extract_indent(lines[line_pointa]) != indent:
                break
            line_pointa = self.interpret_if_block(
                lines, indent=indent, line_pointa=line_pointa
            )
            if self.interpret_var_declare(
                lines[line_pointa]
            ) or self.interpret_arithmetic_formula(lines[line_pointa]):
                state = self.lts.create_state()
                self.lts.add_transition(
                    self.current_state, lines[line_pointa].strip(), state
                )
                self.current_state = state
                line_pointa += 1
        return line_pointa

    def check_indent(self, line: str, indent: str):
        return line.startswith(indent)

    def extract_indent(self, line: str):
        count = 0
        indent = ""
        while True:
            if line[count] == " ":
                indent += " "
                count += 1
            else:
                return indent
