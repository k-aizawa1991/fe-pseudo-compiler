import re
from re import Pattern
from typing import Dict, List, Tuple

from src import exception
from src.lts.lts import LabeledTransitionSystem


class StateType:
    UNDEFINED = 0
    ASSIGN = 1
    DECLARE = 2
    FORMULA = 3
    RETURN = 5
    IF = 10
    WHILE = 20
    FOR = 30


class PseudoCompiledLTS(LabeledTransitionSystem):
    def __init__(
        self,
        init_state_name: str = None,
    ):
        super().__init__(init_state_name)
        self.state_type_map: Dict[str, StateType] = {}
        self.arg_list: List[str] = []
        self.name_val_map: Dict[str, str | int | float | bool] = {}
        self.name_type_map: Dict[str, str] = {}

    def set_state_type(self, state: str, state_type: StateType):
        if state not in self.transitions:
            raise exception.DoesNotExistException(state)
        self.state_type_map[state] = state_type

    def get_state_type(self, state: str):
        if state not in self.transitions:
            raise exception.DoesNotExistException(state)
        if state not in self.state_type_map:
            return StateType.UNDEFINED
        return self.state_type_map[state]


class Interpreter:
    # <否定演算子>
    NOT_OPERATOR = "not"
    # <乗除演算子>
    MUL_DIV_MOD_OPERATOR = "\\*|/|mod|×|÷"
    # <和差演算子>
    ADD_SUB_OPERATOR = "\\+|-|＋|－"
    # <日本語比較開始演算子>
    COMPARE_START_OPERATOR_JP = "が"
    # <日本語比較演算子>
    COMPARE_OPERATOR_JP = (
        "(と|に)等し(い|くない)|以上|以下|より(大きい|小さい)|未満|未定義(でない)?"
    )
    ARRAY_APPEND_START = "の末尾\\s*に\\s*"
    ARRAY_APPEND_END = "を追加する"
    VALUE = "の値"
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
    SQUARE_BRACKET_START = "^\\["
    SQUARE_BRACKET_END = "^\\]"
    CURLY_BRACKET_START = "^\\{"
    CURLY_BRACKET_END = "^\\}"

    # <論理値>::= true | false
    LOGICAL_VALUE = "true|false"
    # <正数字> ::= 1-9
    POSITIVE_NUM = "1-9"
    # <数字> ::= 0 | <正数字>
    NUM = "0-9"
    # <英字> ::= a-z | A-Z
    ALPHABET = "a-zA-Z"
    # <数値> ::= <正数字><数値> | -<正数字><数値> | <数字>
    INT_VAL = "-?" + f"[{NUM}]+"
    REAL_VAL = f"{INT_VAL}(?:\\.[{NUM}]+)?"
    NUM_VAL = f"({REAL_VAL})"
    CONNECTION_CHAR_JP = "の"
    # 漢数字（十まで）
    JP_NUM = "一|二|三|四|五|六|七|八|九|十"
    # 次元
    JP_DIMENSION = "次元"

    # <名前>
    NAME = f"[{ALPHABET}_]([{ALPHABET}_]|[{NUM}])*"
    # <被演算子>
    OPERAND = f"({NUM_VAL}|{NAME})"

    # <型>
    INT_TYPE = "整数型"
    REAL_TYPE = "実数型"
    STR_TYPE = "文字列型"
    BOOL_TYPE = "論理型"
    ARR_SINGLE_SUFFIX = "配列"
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
        f"{INT_TYPE}{ARR_SINGLE_SUFFIX}": List[int],
        f"{REAL_TYPE}{ARR_SINGLE_SUFFIX}": List[float],
        f"{STR_TYPE}{ARR_SINGLE_SUFFIX}": List[str],
        f"{BOOL_TYPE}{ARR_SINGLE_SUFFIX}": List[bool],
    }

    TYPE = f"^({INT_TYPE}|{REAL_TYPE}|{STR_TYPE}|{BOOL_TYPE})({CONNECTION_CHAR_JP}(({INT_VAL})|{JP_NUM}){JP_DIMENSION}{ARR_SINGLE_SUFFIX}|({ARR_SINGLE_SUFFIX})?({ARR_SUFFIX})*)"

    # <引数宣言>
    FUNC_ARG = f"{TYPE[1:]}:[ ]*{NAME}"
    # <関数句>
    FUNC_START = "^[◯|○]"
    FUNC_ARGS = f"^\\(({FUNC_ARG}(,[ ]*{FUNC_ARG})*)?\\)"

    # <FOR句>
    FOR = "^for"
    ENDFOR = "^endfor$"
    FOR_OP1 = "を"
    FOR_OP2 = "から"
    FOR_OP3 = "まで"
    FOR_OP4 = "繰り返す"
    FOR_OP4_2 = "ずつ増やす"
    LENGTH = "の要素数"
    QUOTIENT = "の商"
    REMAINDER = "の余り"
    EXTRA_OPERATOR = f"{QUOTIENT}|{REMAINDER}"
    # <IF句>
    IF = "^if"
    ELSE = "^else"
    ELSEIF = "^elseif"
    ENDIF = "^endif$"

    # <WHILE句>
    WHILE = "^while"
    ENDWHILE = "^endwhile$"
    DO = "^do"

    COLON = "^[:,：]"
    COMMA = "^,"
    ASSIGN = "^<-|←|＜－"

    RETURN = "^return"

    LOGICAL_VAL_MAP = {"true": True, "false": False}
    JP_OPERATOR_FUNC_MAP = {
        "と等しい": lambda val1, val2: val1 == val2,
        "に等しい": lambda val1, val2: val1 == val2,
        "と等しくない": lambda val1, val2: val1 != val2,
        "に等しくない": lambda val1, val2: val1 != val2,
        "以上": lambda val1, val2: val1 >= val2,
        "以下": lambda val1, val2: val1 <= val2,
        "より大きい": lambda val1, val2: val1 > val2,
        "より小さい": lambda val1, val2: val1 < val2,
        "未満": lambda val1, val2: val1 < val2,
    }
    JP_SINGLE_OPERATOR_FUNC_MAP = {
        "未定義": lambda val: val is None,
        "未定義でない": lambda val: val is not None,
    }
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
        "<": lambda val1, val2: val1 < val2,
        "≧": lambda val1, val2: val1 >= val2,
        "≦": lambda val1, val2: val1 <= val2,
        "≠": lambda val1, val2: val1 != val2,
        "=": lambda val1, val2: val1 == val2,
        "＝": lambda val1, val2: val1 == val2,
        "かつ": lambda val1, val2: val1 and val2,
        "または": lambda val1, val2: val1 or val2,
        "の商": lambda val1, val2: int(val1 / val2),
        "の余り": lambda val1, val2: val1 % val2,
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
        self.lts = PseudoCompiledLTS()
        self.func_lts_map = {}
        self.current_state = self.lts.get_init_state()
        self.complie_patterns()

    def complie_patterns(self):
        self.type_pattern = re.compile(self.TYPE)
        self.while_pattern = re.compile(self.WHILE)
        self.endwhile_pattern = re.compile(self.ENDWHILE)
        self.do_pattern = re.compile(self.DO)
        self.if_pattern = re.compile(self.IF)
        self.else_pattern = re.compile(self.ELSE)
        self.elseif_pattern = re.compile(self.ELSEIF)
        self.endif_pattern = re.compile(self.ENDIF)

        self.for_pattern = re.compile(self.FOR)
        self.endfor_pattern = re.compile(self.ENDFOR)
        self.for_op1_pattern = re.compile(self.FOR_OP1)
        self.for_op2_pattern = re.compile(self.FOR_OP2)
        self.for_op3_pattern = re.compile(self.FOR_OP3)
        self.for_op4_pattern = re.compile(self.FOR_OP4)
        self.for_op4_2_pattern = re.compile(self.FOR_OP4_2)

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
        self.compare_start_operator_jp_pattern = re.compile(
            self.COMPARE_START_OPERATOR_JP
        )
        self.compare_operator_jp_pattern = re.compile(self.COMPARE_OPERATOR_JP)
        self.length_pattern = re.compile(self.LENGTH)
        self.extra_operator_pattern = re.compile(self.EXTRA_OPERATOR)
        self.array_append_start_pattern = re.compile(self.ARRAY_APPEND_START)
        self.array_append_end_pattern = re.compile(self.ARRAY_APPEND_END)
        self.value_pattern = re.compile(self.VALUE)

        self.parenthesis_start_pattern = re.compile(self.PALENTHESIS_START)
        self.parenthesis_end_pattern = re.compile(self.PALENTHESIS_END)
        self.square_bracket_start_pattern = re.compile(self.SQUARE_BRACKET_START)
        self.square_bracket_end_pattern = re.compile(self.SQUARE_BRACKET_END)
        self.curly_bracket_start_pattern = re.compile(self.CURLY_BRACKET_START)
        self.curly_bracket_end_pattern = re.compile(self.CURLY_BRACKET_END)

        self.colon_pattern = re.compile(self.COLON)
        self.comma_pattern = re.compile(self.COMMA)
        self.assign_pattern = re.compile(self.ASSIGN)
        self.func_start_pattern = re.compile(self.FUNC_START)
        self.func_args_pattern = re.compile(self.FUNC_ARGS)

        self.return_pattern = re.compile(self.RETURN)

    def interpret_arithmetic_formula(
        self,
        line: str,
        stack: List[str] = None,
        pended_op=None,
        indent: str = "",
        dry_run: bool = False,
        line_num: str = None,
        lts: PseudoCompiledLTS | None = None,
    ):
        if indent != "" and not self.check_indent(line, indent):
            raise exception.InvalidIndentException(line_num=line_num)
        result, remain = self.interpret_arithmetic_operand(
            line, stack, dry_run=dry_run, lts=lts
        )
        while True:
            res = self.process_operator(
                remain, stack, result, pended_op=pended_op, dry_run=dry_run, lts=lts
            )
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
        dry_run: bool = False,
        lts: PseudoCompiledLTS | None = None,
    ):
        res = self.get_pattern_and_remain(
            self.compare_start_operator_jp_pattern, remain
        )
        if res:
            _, remain = res
            res = self.get_pattern_and_remain(self.compare_operator_jp_pattern, remain)
            if res:
                comp_op, remain = res
                if comp_op not in self.JP_SINGLE_OPERATOR_FUNC_MAP:
                    raise exception(remain)
                if dry_run:
                    return None, remain
                return self.JP_SINGLE_OPERATOR_FUNC_MAP[comp_op](val), remain

            val2, remain = self.interpret_arithmetic_operand(
                remain, stack, exception, lts=lts
            )
            comp_op, remain = self.get_pattern_and_remain(
                self.compare_operator_jp_pattern, remain, exception
            )
            if dry_run:
                return None, remain
            return self.JP_OPERATOR_FUNC_MAP[comp_op](val, val2), remain

        res = self.get_pattern_and_remain(self.operators_pattern, remain, exception)
        if not res:
            return None
        op, tmp_remain = res
        if pended_op is not None and pended_op in self.operator_priority_map[op]:
            return None
        else:
            remain = tmp_remain
        val2, tmp_remain = self.interpret_arithmetic_operand(remain, stack, lts=lts)
        # 割り算の商や余りという語句が存在する場合は個々で処理
        res = self.get_pattern_and_remain(self.extra_operator_pattern, tmp_remain)
        if res:
            op, tmp_remain = res
        # 優先度の高い演算子がある場合は先に計算
        res = self.get_pattern_and_remain(self.operators_pattern, tmp_remain)
        if res and res[0] in self.operator_priority_map[op]:
            val2, remain = self.interpret_arithmetic_formula(
                remain, stack, pended_op=op, lts=lts, dry_run=dry_run
            )
        else:
            remain = tmp_remain

        if stack is not None:
            stack.append(op)
        if dry_run:
            return None, remain
        return self.OPERATOR_FUNC_MAP[op](val, val2), remain

    def interpret_arithmetic_operand(
        self,
        line: str,
        stack: List[str] = None,
        dry_run: bool = False,
        lts: PseudoCompiledLTS | None = None,
    ):
        if lts is None:
            lts = self.lts
        res = self.get_pattern_and_remain(self.parenthesis_start_pattern, line)
        if res:
            _, remain = res
            val, remain = self.interpret_arithmetic_formula(
                remain, stack, dry_run=dry_run, lts=lts
            )
            _, remain = self.get_pattern_and_remain(
                self.parenthesis_end_pattern,
                remain,
                exception.InvalidParenthesisException,
            )
            return val, remain
        return self.interpret_operand(line, stack, dry_run=dry_run, lts=lts)

    def interpret_operand(
        self,
        line: str,
        stack: List[str] = None,
        dry_run: bool = False,
        lts: PseudoCompiledLTS | None = None,
    ):
        if lts is None:
            lts = self.lts
        res = self.get_pattern_and_remain(self.single_operators_pattern, line)
        if res:
            single_op, line = res
        else:
            single_op = None
        res = self.get_pattern_and_remain(self.logical_value_pattern, line)
        if res:
            val, remain = res
            val = self.LOGICAL_VAL_MAP[val]
            if single_op is not None and not dry_run:
                val = self.SINGLE_OPERATOR_FUNC_MAP[single_op](val)
            return val, remain
        res = self.get_pattern_and_remain(self.name_pattern, line)
        if res:
            name, remain = res
            if name in self.func_lts_map:
                res = self.get_pattern_and_remain(
                    self.parenthesis_start_pattern,
                    remain,
                    exception.InvalidFuncCallException,
                )
                vars = []
                while res:
                    _, remain = res
                    try:
                        val, remain = self.interpret_arithmetic_formula(remain, lts=lts)
                        vars.append(val)
                    except Exception:
                        break
                    res = self.get_pattern_and_remain(self.comma_pattern, remain)
                res = self.get_pattern_and_remain(
                    self.parenthesis_end_pattern,
                    remain,
                    exception.InvalidFuncCallException,
                )
                if not dry_run:
                    return self.execute_lts(self.func_lts_map[name], vars), remain
                return None, remain
            if name not in lts.name_val_map:
                raise exception.NameNotDefinedException(name)
            if stack is not None:
                stack.append(name)
            res = self.get_pattern_and_remain(self.square_bracket_start_pattern, remain)
            idx_list = []
            while res:
                _, remain = res
                if type(lts.name_val_map[name]) is not list and not dry_run:
                    raise exception.InvalidArrayException(name)
                index, remain = self.interpret_arithmetic_formula(remain, lts=lts)
                _, remain = self.get_pattern_and_remain(
                    self.square_bracket_end_pattern,
                    remain,
                    exception.InvalidSquareBracketException,
                )
                idx_list.append(index)
                res = self.get_pattern_and_remain(
                    self.square_bracket_start_pattern, remain
                )
            if len(idx_list) > 0:
                if dry_run:
                    return None, remain
                return_target = lts.name_val_map[name]
                for index in idx_list:
                    if int(index) > len(return_target) or int(index) < 1:
                        raise exception.InvalidArrayIndexException(name)
                    return_target = return_target[int(index) - 1]
                return return_target, remain
            res = self.get_pattern_and_remain(self.length_pattern, remain)
            if res:
                _, remain = res
                if type(lts.name_val_map[name]) is not list:
                    raise exception.InvalidArrayException(name)
                if dry_run:
                    return None, remain
                return len(lts.name_val_map[name]), remain

            return lts.name_val_map[name], remain
        num_val, remain = self.get_pattern_and_remain(
            self.num_val_pattern, line, exception.InvalidFormulaException
        )
        if stack is not None:
            stack.append(num_val)
        try:
            val = int(num_val)
        except ValueError:
            val = float(num_val)
        if single_op is not None and not dry_run:
            val = self.SINGLE_OPERATOR_FUNC_MAP[single_op](val)
        return val, remain

    def get_pattern_and_remain(
        self,
        pattern: Pattern,
        target: str,
        e: Exception | None = None,
        indent: str = "",
        line_num: int = 0,
    ) -> Tuple[str, str]:
        if indent != "" and not self.check_indent(target, indent):
            raise exception.InvalidIndentException(line_num=line_num)
        target = target.strip()
        matched = pattern.match(target)
        if not matched:
            if e is None:
                return None
            else:
                raise e(target)
        return target[matched.start() : matched.end()], target[matched.end() :].strip()

    def process_var_assigns(
        self,
        remain,
        indent="",
        line_num=0,
        dry_run: bool = False,
        lts: PseudoCompiledLTS | None = None,
    ):
        array_idx_dict: Dict[str, List[int]] = {}
        if lts is None:
            lts = self.lts
        vars_list = []
        while True:
            name, remain = self.get_pattern_and_remain(
                self.name_pattern,
                remain,
                exception.NamePatternException,
                indent=indent,
                line_num=line_num,
            )
            res = self.get_pattern_and_remain(self.square_bracket_start_pattern, remain)
            while res:
                _, remain = res
                idx, remain = self.interpret_arithmetic_formula(
                    remain, lts=lts, dry_run=dry_run
                )
                if name not in array_idx_dict:
                    array_idx_dict[name] = []
                array_idx_dict[name].append(idx)
                _, remain = self.get_pattern_and_remain(
                    self.square_bracket_end_pattern,
                    remain,
                    exception.InvalidSquareBracketException,
                )
                res = self.get_pattern_and_remain(
                    self.square_bracket_start_pattern, remain
                )
            vars_list.append(name)
            res = self.get_pattern_and_remain(
                self.array_append_start_pattern,
                remain,
            )
            if res:
                _, remain = res
                res = self.get_pattern_and_remain(
                    self.curly_bracket_start_pattern, remain
                )
                if res:
                    val, remain = self.process_array_definition(
                        remain, lts, dry_run=dry_run
                    )
                else:
                    val, remain = self.interpret_arithmetic_formula(
                        remain, dry_run=dry_run, lts=lts
                    )
                res = self.get_pattern_and_remain(self.value_pattern, remain)
                if res:
                    _, remain = res
                _, remain = self.get_pattern_and_remain(
                    self.array_append_end_pattern,
                    remain,
                    exception.InvalidArrayAppendException,
                )
                print("hoge", val, dry_run)
                if not dry_run:
                    if type(lts.name_val_map[name]) is not list:
                        raise exception.InvalidArrayException(name)
                    if name in array_idx_dict:
                        target = self.get_target_array(lts, name, array_idx_dict[name])
                        target[int(array_idx_dict[name][-1] - 1)].append(val)
                        print(target)
                    else:
                        lts.name_val_map[name].append(val)
                        print(lts.name_val_map[name])
                return [name], remain

            res = self.get_pattern_and_remain(
                self.assign_pattern, remain, line_num=line_num
            )
            if res:
                _, remain = res
                # 配列の代入は独立して実施
                res = self.get_pattern_and_remain(
                    self.curly_bracket_start_pattern, remain
                )
                if res:
                    array, remain = self.process_array_definition(
                        remain, lts, dry_run=dry_run
                    )
                    if name in array_idx_dict:
                        target = self.get_target_array(lts, name, array_idx_dict[name])
                        target[int(array_idx_dict[name][-1] - 1)] = array
                    else:
                        lts.name_val_map[name] = array
                else:
                    val, remain = self.interpret_arithmetic_formula(
                        remain, dry_run=dry_run, lts=lts
                    )
                    if name in array_idx_dict and not dry_run:
                        target = self.get_target_array(lts, name, array_idx_dict[name])
                        target[int(array_idx_dict[name][-1] - 1)] = val
                    else:
                        lts.name_val_map[name] = val
            else:
                if name in array_idx_dict and not dry_run:
                    target = self.get_target_array(lts, name, array_idx_dict[name])
                    target[int(array_idx_dict[name][-1] - 1)] = None
                else:
                    lts.name_val_map[name] = None
            res = self.get_pattern_and_remain(
                self.comma_pattern, remain, indent=indent, line_num=line_num
            )
            if res:
                _, remain = res
                continue
            else:
                break
        return vars_list, remain

    def get_target_array(
        self, lts: PseudoCompiledLTS, name: str, target_list: List[int]
    ):
        target = lts.name_val_map[name]
        for idx in range(0, len(target_list) - 1):
            target = target[int(target_list[idx]) - 1]
        return target

    def process_array_definition(
        self, line: str, lts: PseudoCompiledLTS, dry_run: bool = False
    ):
        array = []
        res = self.get_pattern_and_remain(self.curly_bracket_start_pattern, line)
        if not res:
            return None
        _, remain = res
        while True:
            if self.get_pattern_and_remain(self.curly_bracket_end_pattern, remain):
                break
            res = self.get_pattern_and_remain(self.curly_bracket_start_pattern, remain)
            if res:
                inner_array, remain = self.process_array_definition(
                    remain, lts, dry_run=dry_run
                )
                if not dry_run:
                    array.append(inner_array)
            else:
                val, remain = self.interpret_arithmetic_formula(
                    remain, dry_run=dry_run, lts=lts
                )
                if not dry_run:
                    array.append(val)
            res = self.get_pattern_and_remain(self.comma_pattern, remain)
            if res:
                _, remain = res
            else:
                break
        _, remain = self.get_pattern_and_remain(
            self.curly_bracket_end_pattern,
            remain,
            exception.InvalidCurlyBracketException,
        )
        return array, remain

    def interpret_var_assign(
        self,
        line: str,
        indent: str = "",
        line_num: int = 0,
        dry_run: bool = False,
        lts: PseudoCompiledLTS | None = None,
    ):
        if lts is None:
            lts = self.lts
        res = self.get_pattern_and_remain(
            self.name_pattern,
            line,
            indent=indent,
            line_num=line_num,
        )
        if not res:
            return None
        var_name, remain = res
        res = self.get_pattern_and_remain(
            self.square_bracket_start_pattern, remain, line_num=line_num
        )
        while res:
            _, remain = res
            _, remain = self.interpret_arithmetic_formula(remain, lts=lts, dry_run=dry_run)
            _, remain = self.get_pattern_and_remain(
                self.square_bracket_end_pattern,
                remain,
                exception.InvalidSquareBracketException,
            )
            res = self.get_pattern_and_remain(
                self.square_bracket_start_pattern, remain, line_num=line_num
            )
        res = self.get_pattern_and_remain(
            self.array_append_start_pattern, remain, line_num=line_num
        )
        if res:
            _, remain = res
            res = self.get_pattern_and_remain(self.curly_bracket_start_pattern, remain)
            if res:
                _, remain = self.process_array_definition(remain, lts, dry_run=dry_run)
            else:
                _, remain = self.interpret_arithmetic_formula(
                    remain, lts=lts, dry_run=dry_run
                )
            res = self.get_pattern_and_remain(self.value_pattern, remain)
            if res:
                _, remain = res
            _, remain = self.get_pattern_and_remain(
                self.array_append_end_pattern,
                remain,
                exception.InvalidArrayAppendException,
                line_num=line_num,
            )
        else:
            res = self.get_pattern_and_remain(
                self.assign_pattern, remain, line_num=line_num
            )
            if not res:
                if len(remain) != 0 and not dry_run:
                    raise exception.InvalidVarAssignException(line_num=line_num)
                return None
            if var_name not in lts.name_val_map:
                raise exception.NameNotDefinedException(var_name)
        _, remain = self.process_var_assigns(line, dry_run=dry_run, lts=lts)
        return remain

    def interpret_return(
        self,
        line: str,
        indent: str = "",
        line_num: int = 0,
        dry_run: bool = False,
        lts: PseudoCompiledLTS | None = None,
    ):
        res = self.get_pattern_and_remain(
            self.return_pattern,
            line,
            indent=indent,
            line_num=line_num,
        )
        if not res:
            return None
        _, remain = res
        if remain.strip() == "":
            return ""
        return self.interpret_arithmetic_formula(
            remain, dry_run=dry_run, line_num=line_num, lts=lts
        )

    def interpret_var_declare(
        self,
        line,
        indent="",
        line_num=0,
        dry_run: bool = False,
        lts: PseudoCompiledLTS | None = None,
    ):
        if lts is None:
            lts = self.lts
        res = self.get_pattern_and_remain(
            self.type_pattern,
            line,
            indent=indent,
            line_num=line_num,
        )
        if not res:
            return None
        type_str, remain = res
        _, remain = self.get_pattern_and_remain(
            self.colon_pattern,
            remain,
            exception.DeclareException,
        )
        vars, remain = self.process_var_assigns(remain, dry_run=dry_run, lts=lts)

        for var in vars:
            lts.name_type_map[var] = type_str
        return remain

    def interpret_if_block(
        self,
        lines: List[str],
        return_tuples: List[Tuple[str, str]],
        indent: str = "",
        line_pointa=0,
        lts: PseudoCompiledLTS | None = None,
    ):
        if len(lines) == 0 or (
            indent != "" and not self.check_indent(lines[line_pointa], indent)
        ):
            return line_pointa
        res = self.get_pattern_and_remain(
            self.if_pattern, lines[line_pointa], indent=indent, line_num=line_pointa
        )
        end_states = []
        if not res:
            return line_pointa
        _, remain = res
        if lts is None:
            lts = self.lts
        # 分岐を管理する状態にマーク
        lts.set_state_type(self.current_state, StateType.IF)
        line_pointa, start_state = self.process_nested_process(
            lines,
            line_pointa,
            return_tuples,
            remain,
            indent,
            self.current_state,
            lts=lts,
        )

        end_states.append(self.current_state)
        while True:
            if len(lines) == 0:
                break
            res = self.get_pattern_and_remain(
                self.elseif_pattern,
                lines[line_pointa],
                indent=indent,
                line_num=line_pointa,
            )
            if not res:
                break
            _, remain = res
            line_pointa, _ = self.process_nested_process(
                lines, line_pointa, return_tuples, remain, indent, start_state, lts=lts
            )
            end_states.append(self.current_state)
        if len(lines) <= line_pointa:
            raise exception.InvalidFormulaException()
        res = self.get_pattern_and_remain(
            self.else_pattern, lines[line_pointa], indent=indent, line_num=line_pointa
        )
        if res:
            line_pointa, _ = self.process_nested_process(
                lines, line_pointa, return_tuples, "else", indent, start_state, lts=lts
            )
            end_states.append(self.current_state)
        else:
            state = lts.create_state()
            lts.add_transition(start_state, "else", state)
            self.current_state = state
            end_states.append(self.current_state)

        if len(lines) <= line_pointa:
            raise exception.InvalidFormulaException()
        res = self.get_pattern_and_remain(
            self.endif_pattern, lines[line_pointa], indent=indent, line_num=line_pointa
        )
        if not res:
            raise exception.InvalidIfBlockException(line_num=line_pointa)
        line_pointa += 1
        endif_state = lts.create_state()
        for end_state in end_states:
            lts.add_transition(end_state, "endif", endif_state)
        self.current_state = endif_state

        return line_pointa

    def interpret_while_block(
        self,
        lines: List[str],
        return_tuples: List[Tuple[str, str]],
        indent: str = "",
        line_pointa=0,
        lts: PseudoCompiledLTS | None = None,
    ):
        if len(lines) == 0 or (
            indent != "" and not self.check_indent(lines[line_pointa], indent)
        ):
            return line_pointa

        res = self.get_pattern_and_remain(
            self.while_pattern, lines[line_pointa], indent=indent, line_num=line_pointa
        )
        if not res:
            return line_pointa
        if lts is None:
            lts = self.lts
        _, remain = res
        # 繰り返し条件を管理する状態にマーク
        lts.set_state_type(self.current_state, StateType.WHILE)
        line_pointa, start_state = self.process_nested_process(
            lines,
            line_pointa,
            return_tuples,
            remain,
            indent,
            self.current_state,
            lts=lts,
        )
        res = self.get_pattern_and_remain(
            self.endwhile_pattern,
            lines[line_pointa],
            indent=indent,
            line_num=line_pointa,
        )
        if not res:
            raise exception.InvalidWhileBlockException(line_num=line_pointa)
        line_pointa += 1
        lts.add_transition(self.current_state, "", start_state)
        endwhile_state = lts.create_state()
        lts.add_transition(start_state, "endwhile", endwhile_state)

        self.current_state = endwhile_state

        return line_pointa

    def interpret_do_while_block(
        self,
        lines: List[str],
        return_tuples: List[Tuple[str, str]],
        indent: str = "",
        line_pointa=0,
        lts: PseudoCompiledLTS | None = None,
    ):
        if len(lines) == 0 or (
            indent != "" and not self.check_indent(lines[line_pointa], indent)
        ):
            return line_pointa

        res = self.get_pattern_and_remain(
            self.do_pattern, lines[line_pointa], indent=indent, line_num=line_pointa
        )
        if not res:
            return line_pointa
        if lts is None:
            lts = self.lts
        _, _ = res
        line_pointa, start_state = self.process_nested_process(
            lines, line_pointa, return_tuples, "do", indent, self.current_state, lts=lts
        )
        res = self.get_pattern_and_remain(
            self.while_pattern,
            lines[line_pointa],
            indent=indent,
            line_num=line_pointa,
        )
        if not res:
            raise exception.InvalidDoWhileBlockException(line_num=line_pointa)
        line_pointa += 1
        _, remain = res
        lts.set_state_type(self.current_state, StateType.WHILE)
        lts.add_transition(self.current_state, remain, start_state)
        endwhile_state = lts.create_state()
        lts.add_transition(self.current_state, "else", endwhile_state)

        self.current_state = endwhile_state

        return line_pointa

    def interpret_for_block(
        self,
        lines: List[str],
        return_tuples: List[Tuple[str, str]],
        indent: str = "",
        line_pointa=0,
        lts: PseudoCompiledLTS | None = None,
    ):
        if len(lines) == 0 or (
            indent != "" and not self.check_indent(lines[line_pointa], indent)
        ):
            return line_pointa

        res = self.get_pattern_and_remain(
            self.for_pattern, lines[line_pointa], indent=indent, line_num=line_pointa
        )
        if not res:
            return line_pointa
        if lts is None:
            lts = self.lts
        _, remain = res
        lts.set_state_type(self.current_state, StateType.FOR)
        line_pointa, start_state = self.process_nested_process(
            lines,
            line_pointa,
            return_tuples,
            remain,
            indent,
            self.current_state,
            lts=lts,
        )
        res = self.get_pattern_and_remain(
            self.endfor_pattern,
            lines[line_pointa],
            indent=indent,
            line_num=line_pointa,
        )
        if not res:
            raise exception.InvalidForBlockException(line_num=line_pointa)
        line_pointa += 1
        _, remain = res
        lts.add_transition(self.current_state, remain, start_state)
        endfor_state = lts.create_state()
        lts.add_transition(start_state, "endfor", endfor_state)

        self.current_state = endfor_state

        return line_pointa

    def process_for_sentence(
        self, line: str, line_num: int = 0, lts: PseudoCompiledLTS | None = None
    ):
        if lts is None:
            lts = self.lts
        _, remain = self.get_pattern_and_remain(
            self.parenthesis_start_pattern,
            line,
            exception.InvalidForSentenceException,
            line_num=line_num,
        )
        name, remain = self.get_pattern_and_remain(
            self.name_pattern,
            remain,
            exception.InvalidForSentenceException,
            line_num=line_num,
        )
        _, remain = self.get_pattern_and_remain(
            self.for_op1_pattern,
            remain,
            exception.InvalidForSentenceException,
            line_num=line_num,
        )
        res = self.get_pattern_and_remain(self.name_pattern, line)
        if res:
            from_val, remain = res
            if from_val not in lts.name_val_map:
                raise exception.NameNotDefinedException(from_val, line_num=line_num)
        else:
            from_val, remain = self.interpret_arithmetic_formula(remain, lts=lts)
        _, remain = self.get_pattern_and_remain(
            self.for_op2_pattern,
            remain,
            exception.InvalidForSentenceException,
            line_num=line_num,
        )
        res = self.get_pattern_and_remain(self.name_pattern, line)
        if res:
            to_val, remain = res
            if to_val not in lts.name_val_map:
                raise exception.NameNotDefinedException(to_val, line_num=line_num)
        else:
            to_val, remain = self.interpret_arithmetic_formula(remain, lts=lts)
        _, remain = self.get_pattern_and_remain(
            self.for_op3_pattern,
            remain,
            exception.InvalidForSentenceException,
            line_num=line_num,
        )
        res = self.get_pattern_and_remain(self.for_op4_pattern, remain)
        if res:
            increment_val = 1
        else:
            increment_val, remain = self.interpret_arithmetic_formula(remain, lts=lts)
            _, remain = self.get_pattern_and_remain(
                self.for_op4_2_pattern,
                remain,
            )
        _, remain = self.get_pattern_and_remain(
            self.parenthesis_end_pattern,
            remain,
            exception.InvalidForSentenceException,
            line_num=line_num,
        )

        try:
            return name, int(from_val), int(to_val), increment_val
        except ValueError:
            raise exception.InvalidForSentenceException()

    def process_nested_process(
        self,
        lines: List[str],
        line_pointa: int,
        return_tuples: List[Tuple[str, str]],
        in_label: str | None = None,
        indent: str = "",
        start_state: str | None = None,
        lts: PseudoCompiledLTS | None = None,
    ):
        child_indent = self.extract_indent(lines[line_pointa + 1])
        if len(indent) >= len(child_indent):
            raise exception.InvalidIndentException(line_num=line_pointa + 1)
        if lts is None:
            lts = self.lts
        if start_state is None:
            start_state = lts.init_state
        if in_label is not None:
            state = lts.create_state()
            lts.add_transition(start_state, in_label, state)
        else:
            state = start_state
        self.current_state = state
        line_pointa = self.interpret_process(
            lines, return_tuples, child_indent, line_pointa + 1, lts=lts
        )
        if line_pointa < len(lines) and not self.check_indent(
            lines[line_pointa], indent
        ):
            raise exception.InvalidIndentException(line_num=line_pointa)
        return line_pointa, start_state

    def interpret_func_block(
        self,
        lines: List[str],
        indent: str = "",
        line_pointa=0,
    ):
        if len(lines) == 0 or (
            indent != "" and not self.check_indent(lines[line_pointa], indent)
        ):
            return line_pointa

        res = self.get_pattern_and_remain(
            self.func_start_pattern,
            lines[line_pointa],
            indent=indent,
            line_num=line_pointa,
        )
        if not res:
            return line_pointa
        _, remain = res
        res = self.get_pattern_and_remain(
            self.type_pattern,
            remain,
        )
        if res:
            return_type, remain = res
            _, remain = self.get_pattern_and_remain(
                self.colon_pattern, remain, exception.DeclareException
            )
        func_name, remain = self.get_pattern_and_remain(
            self.name_pattern,
            remain,
            exception.FuncNameException,
            indent=indent,
            line_num=line_pointa,
        )
        return_tuples: List[Tuple[str, str]] = []

        func_lts = PseudoCompiledLTS()
        self.process_func_args(remain, line_pointa, func_lts)
        self.func_lts_map[func_name] = func_lts
        current_state = self.current_state
        line_pointa, _ = self.process_nested_process(
            lines, line_pointa, return_tuples, lts=func_lts
        )
        return_state = func_lts.create_state()
        for source_state, label in return_tuples:
            # 自動で作成されるendifやendfor, endwhileなどを削除
            func_lts.clear_transition(source_state)
            func_lts.add_transition(source_state, label, return_state)
        ends = [
            end
            for end in func_lts.transitions
            if len(func_lts.transitions[end]) == 0 and end != return_state
        ]
        for end in ends:
            func_lts.set_state_type(end, StateType.RETURN)
            func_lts.add_transition(end, "return", return_state)
        self.current_state = current_state
        return line_pointa

    def process_func_args(
        self, line: str, line_num, lts: PseudoCompiledLTS | None = None
    ):
        if lts is None:
            lts = self.lts
        _, remain = self.get_pattern_and_remain(
            self.parenthesis_start_pattern,
            line,
            exception.InvalidFuncDeclareException,
            line_num=line_num,
        )
        res = self.get_pattern_and_remain(self.type_pattern, remain)
        while res:
            var_type, remain = res
            _, remain = self.get_pattern_and_remain(
                self.colon_pattern,
                remain,
                exception.InvalidFuncDeclareException,
                line_num=line_num,
            )
            var_name, remain = self.get_pattern_and_remain(
                self.name_pattern,
                remain,
                exception.NamePatternException,
                line_num=line_num,
            )
            lts.arg_list.append(var_name)
            lts.name_val_map[var_name] = None
            lts.name_type_map[var_name] = var_type
            res = self.get_pattern_and_remain(self.comma_pattern, remain)
            if res:
                _, remain = res
                res = self.get_pattern_and_remain(self.type_pattern, remain)
        _, remain = self.get_pattern_and_remain(
            self.parenthesis_end_pattern,
            remain,
            exception.InvalidFuncDeclareException,
            line_num=line_num,
        )
        return lts.arg_list, remain

    def interpret_process(
        self,
        lines: List[str],
        return_tuples: List[Tuple[str, str]],
        indent: str = "",
        line_pointa=0,
        lts: PseudoCompiledLTS | None = None,
    ):
        interpret_targets = [
            self.interpret_if_block,
            self.interpret_while_block,
            self.interpret_do_while_block,
            self.interpret_for_block,
        ]
        if lts is None:
            lts = self.lts
        while lines is not None and line_pointa < len(lines):
            is_processed = False
            if self.extract_indent(lines[line_pointa]) != indent:
                break
            tmp_line_pointa = self.interpret_func_block(
                lines, indent=indent, line_pointa=line_pointa
            )
            if tmp_line_pointa != line_pointa:
                line_pointa = tmp_line_pointa
                continue
            for target_func in interpret_targets:
                tmp_line_pointa = target_func(
                    lines=lines,
                    return_tuples=return_tuples,
                    indent=indent,
                    line_pointa=line_pointa,
                    lts=lts,
                )
                if tmp_line_pointa != line_pointa:
                    line_pointa = tmp_line_pointa
                    is_processed = True
                    break
            if is_processed:
                continue
            if (
                self.interpret_return(lines[line_pointa], lts=lts, dry_run=True)
                is not None
            ):
                lts.set_state_type(self.current_state, StateType.RETURN)
                return_tuples.append((self.current_state, lines[line_pointa].strip()))
                line_pointa += 1
                break
            state_type = (
                StateType.DECLARE
                if (
                    self.interpret_var_declare(
                        lines[line_pointa],
                        indent=indent,
                        line_num=line_pointa,
                        dry_run=True,
                        lts=lts,
                    )
                    is not None
                )
                else StateType.ASSIGN
                if (
                    self.interpret_var_assign(
                        lines[line_pointa],
                        indent=indent,
                        line_num=line_pointa,
                        dry_run=True,
                        lts=lts,
                    )
                    is not None
                )
                else StateType.FORMULA
                if (
                    self.interpret_arithmetic_formula(
                        lines[line_pointa],
                        indent=indent,
                        line_num=line_pointa,
                        dry_run=True,
                        lts=lts,
                    )
                    is not None
                )
                else None
            )
            if state_type is not None:
                state = lts.create_state()
                lts.set_state_type(self.current_state, state_type)
                lts.add_transition(
                    self.current_state, lines[line_pointa].strip(), state
                )
                self.current_state = state
                line_pointa += 1
        return line_pointa

    def interpret_main_process(
        self,
        lines: List[str],
    ):
        return_tuples = []
        line_pointa = self.interpret_process(lines, return_tuples)
        return_state = self.lts.create_state()
        for source_state, label in return_tuples:
            # 自動で作成されるendifやendfor, endwhileなどを削除
            self.lts.clear_transition(source_state)
            self.lts.add_transition(source_state, label, return_state)
        ends = [
            end
            for end in self.lts.transitions
            if len(self.lts.transitions[end]) == 0 and end != return_state
        ]
        for end in ends:
            self.lts.set_state_type(end, StateType.RETURN)
            self.lts.add_transition(end, "return", return_state)
        return line_pointa

    def check_indent(self, line: str, indent: str):
        if indent == "":
            return not line.startswith(" ")
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

    def execute_lts(self, lts: PseudoCompiledLTS | None = None, vars: List[str] = []):
        if lts is None:
            lts = self.lts
        if len(lts.arg_list) != len(vars):
            raise exception.InvalidFuncCallException()
        for arg, arg_val in zip(lts.arg_list, vars):
            lts.name_val_map[arg] = arg_val
        state = lts.init_state
        val = None
        while state is not None:
            state, val = self.fire_transition(state, lts)
        return val

    def fire_transition(self, state: str, lts: PseudoCompiledLTS):
        # 基本的に最初の遷移ラベルは使うのでここで取得してしまう
        label = lts.get_transition_label(state)
        val = None
        if lts.get_state_type(state) in [StateType.IF, StateType.WHILE]:
            return self.get_transition_on_condition_state(state, lts)
        if lts.get_state_type(state) == StateType.FOR:
            name, from_val, to_val, increment_val = self.process_for_sentence(label, lts=lts)
            if lts.name_val_map[name] is None:
                lts.name_val_map[name] = from_val
            elif lts.name_val_map[name] + increment_val <= to_val:
                lts.name_val_map[name] += increment_val
            else:
                lts.name_val_map[name] = None
                label = "endfor"
        if lts.get_state_type(state) == StateType.DECLARE:
            self.interpret_var_declare(label, lts=lts)
        if lts.get_state_type(state) == StateType.ASSIGN:
            self.interpret_var_assign(label, lts=lts)
        if lts.get_state_type(state) == StateType.FORMULA:
            self.interpret_arithmetic_formula(label, lts=lts)
        if lts.get_state_type(state) == StateType.RETURN:
            val = None
            res = self.interpret_return(label, lts=lts)
            if res:
                val = res[0]
            return None, val
        return lts.get_transition_state(state, label), val

    def get_transition_on_condition_state(self, state: str, lts: PseudoCompiledLTS):
        label_index = 0
        label = lts.get_transition_label(state, index=label_index)
        val, _ = self.interpret_arithmetic_formula(label, lts=lts)
        while not val:
            label_index += 1
            label = lts.get_transition_label(state, index=label_index)
            if label in ["else", "endwhile"]:
                break
            val, _ = self.interpret_arithmetic_formula(label, lts=lts)
        return lts.get_transition_state(state, label), val
