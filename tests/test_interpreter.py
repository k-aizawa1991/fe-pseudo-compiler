import pytest
from src.interpreter import Interpreter
from src import exception


def test_get_real_num_pattern():
    interpreter = Interpreter()
    actual_str, remain = interpreter.get_pattern_and_remain(
        interpreter.num_val_pattern, "123+4"
    )
    assert actual_str == "123"
    assert remain == "+4"


def test_get_int_num_pattern():
    interpreter = Interpreter()
    actual_str, remain = interpreter.get_pattern_and_remain(
        interpreter.num_val_pattern, "0.123+4.56"
    )
    assert actual_str == "0.123"
    assert remain == "+4.56"


def test_interpret_operand_num():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_operand("145+14", [])
    assert actual_val == 145
    assert remain == "+14"


def test_process_mul_div():
    interpreter = Interpreter()
    actual_val, remain = interpreter.process_operator("*2*6/3", [], 1)
    assert actual_val == 2
    assert remain == "*6/3"


def test_process_add_sub():
    interpreter = Interpreter()

    actual_val, remain = interpreter.process_operator("+2+3-4", [], 1)
    assert actual_val == 3
    assert remain == "+3-4"


def test_interpret_arithmetic_formula():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("(1+2)*3-4", [])
    assert actual_val == 5
    assert remain == ""


def test_interpret_arithmetic_formula_not():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("not true", [])
    assert not actual_val
    assert remain == ""


def test_interpret_arithmetic_formula_mod():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("12 mod 5", [])
    assert actual_val == 2
    assert remain == ""


def test_interpret_arithmetic_formula_double_mul_div():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("1*2*3/4", [])
    assert actual_val == 1.5
    assert remain == ""


def test_interpret_arithmetic_formula_div_sub():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("24/2/3-4", [])
    assert actual_val == 0
    assert remain == ""


def test_interpret_arithmetic_decimal():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("2.5 / 0.25 / 5 / 2")
    assert actual_val == 2.5 / 0.25 / 5 / 2
    assert remain == ""


def test_interpret_arithmetic_formula_double_add_mul_sub():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("1+2+3*4*5-6-7", [])
    assert actual_val == 50
    assert remain == ""


def test_interpret_arithmetic_formula_double_parenthesis():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("((1+2)*3-4)*5", [])
    assert actual_val == 25
    assert remain == ""


def test_interpret_formula_gtlt():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("2+3＞2*3")
    assert not actual_val
    assert remain == ""

    actual_val, remain = interpreter.interpret_arithmetic_formula("2+3＜2*3")
    assert actual_val
    assert remain == ""


def test_interpret_formula_gtelte():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("2+3≧2*3")
    assert not actual_val
    assert remain == ""

    actual_val, remain = interpreter.interpret_arithmetic_formula("2+3≦2*3")
    assert actual_val
    assert remain == ""


def test_interpret_formula_eqneq():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("2+3＝2*3")
    assert not actual_val
    assert remain == ""

    actual_val, remain = interpreter.interpret_arithmetic_formula("2+3≠2*3")
    assert actual_val
    assert remain == ""


def test_interpret_formula_multi_compare():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("2＜3＜4")
    assert actual_val
    assert remain == ""

    actual_val, remain = interpreter.interpret_arithmetic_formula("2＜3＞4")
    assert not actual_val
    assert remain == ""


def test_interpret_formula_and():
    interpreter = Interpreter()
    stack = []
    actual_val, remain = interpreter.interpret_arithmetic_formula(
        "2+3＝2*3 かつ 4+5＝4*5", stack
    )
    print(stack)
    assert not actual_val
    assert remain == ""

    stack = []
    actual_val, remain = interpreter.interpret_arithmetic_formula(
        "2+3≠2*3 かつ 4+5＝4*5"
    )
    assert not actual_val
    assert remain == ""

    actual_val, remain = interpreter.interpret_arithmetic_formula(
        "2+3≠2*3 かつ 4+5≠4*5"
    )
    assert actual_val
    assert remain == ""


def test_interpret_formula_or():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula(
        "2+3＝2*3 または 4+5＝4*5"
    )
    assert not actual_val
    assert remain == ""

    actual_val, remain = interpreter.interpret_arithmetic_formula(
        "2+3≠2*3 または 4+5＝4*5"
    )
    assert actual_val
    assert remain == ""

    actual_val, remain = interpreter.interpret_arithmetic_formula(
        "2+3≠2*3 または 4+5≠4*5"
    )
    assert actual_val
    assert remain == ""


def test_interpret_formula_or_and():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula(
        "1+2≠1*2 または 2+3＝2*3 かつ 4+5＝4*5"
    )
    assert actual_val
    assert remain == ""

    actual_val, remain = interpreter.interpret_arithmetic_formula(
        "1+2＝1*2 または 2+3≠2*3 かつ 4+5≠4*5"
    )
    assert actual_val
    assert remain == ""

    actual_val, remain = interpreter.interpret_arithmetic_formula(
        "1+2＝1*2 または 2+3＝2*3 かつ 4+5≠4*5"
    )
    assert not actual_val
    assert remain == ""


def test_interpret_formula_bit():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("3 | 12")
    assert actual_val == 15
    assert remain == ""

    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("3 & 12")
    assert actual_val == 0
    assert remain == ""


def test_interpret_formula_jp_com_op():
    interpreter = Interpreter()
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 1と等しい")
    assert actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 2に等しい")
    assert not actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 2と等しくない")
    assert actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 1に等しくない")
    assert not actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 1以上")
    assert actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 1以下")
    assert actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 1より大きい")
    assert not actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 1より小さい")
    assert not actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 1未満")
    assert not actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 未定義")
    assert not actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 未定義でない")
    assert actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 1 でない")
    assert not actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("1 が 1 である")
    assert actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("4 が 2 で割り切れる")
    assert actual_val
    actual_val, _ = interpreter.interpret_arithmetic_formula("4 が 3 で割り切れる")
    assert not actual_val



def test_interpret_formula_jp_extra_op():
    interpreter = Interpreter()
    actual_val, _ = interpreter.interpret_arithmetic_formula("3 ÷ 2の商")
    assert actual_val == 1
    actual_val, _ = interpreter.interpret_arithmetic_formula("3 ÷ 2の余り")
    assert actual_val == 1


def test_interpret_formula_jp_length_op():
    interpreter = Interpreter()
    interpreter.interpret_var_declare("整数型の配列: a ← {{1, 2},{3, 4},{5, 6}}")
    actual_val, _ = interpreter.interpret_arithmetic_formula("aの要素数")
    assert actual_val == 3
    actual_val, _ = interpreter.interpret_arithmetic_formula("aの行数")
    assert actual_val == 3
    actual_val, _ = interpreter.interpret_arithmetic_formula("aの列数")
    assert actual_val == 2

def test_process_var_assigns():
    interpreter = Interpreter()
    actual_list, remain = interpreter.process_var_assigns("a←1+2+3, b, c←5")

    assert actual_list == ["a", "b", "c"]
    assert interpreter.lts.name_val_map["a"] == 6
    assert interpreter.lts.name_val_map["b"] is None
    assert interpreter.lts.name_val_map["c"] == 5
    assert remain == ""


def test_process_var_assigns_array():
    interpreter = Interpreter()
    actual_list, remain = interpreter.process_var_assigns("a←{1+2,3}, b←{4,5*6}, c←{}")
    assert actual_list == ["a", "b", "c"]
    assert interpreter.lts.name_val_map["a"] == [3, 3]
    assert interpreter.lts.name_val_map["b"] == [4, 30]
    assert interpreter.lts.name_val_map["c"] == []
    assert remain == ""


def test_process_var_assigns_invalid_square_bracet():
    interpreter = Interpreter()
    with pytest.raises(exception.InvalidCurlyBracketException) as e:
        interpreter.process_var_assigns("a←{1+2,3")
    assert str(e.value) == '"{"に対応する"}"が存在しません。'


def test_process_var_assigns_invalid_array():
    interpreter = Interpreter()
    interpreter.process_var_assigns("a←1+2")
    with pytest.raises(exception.InvalidArrayException) as e:
        interpreter.process_var_assigns("b←a[0]")
    assert str(e.value) == "aは配列ではありません。"


def test_process_var_assigns_array_access():
    interpreter = Interpreter()
    actual_list, remain = interpreter.process_var_assigns("a←{1+2,3}, b←{4,5*6}, c←{}")
    actual_list, remain = interpreter.process_var_assigns("d←a[1]+b[2]")
    assert actual_list == ["d"]
    assert interpreter.lts.name_val_map["a"] == [3, 3]
    assert interpreter.lts.name_val_map["b"] == [4, 30]
    assert interpreter.lts.name_val_map["c"] == []
    assert interpreter.lts.name_val_map["d"] == 33
    actual_list, remain = interpreter.process_var_assigns("b[1]←a[1]+b[2]")
    assert interpreter.lts.name_val_map["b"] == [33, 30]

    assert remain == ""


def test_process_var_assigns_n_array():
    interpreter = Interpreter()
    interpreter.process_var_assigns("a←{{1,2},{3}}, b←{{{4,5},{6,7}},{{8},{9}}}, c←{}")
    assert interpreter.lts.name_val_map["a"] == [[1, 2], [3]]
    assert interpreter.lts.name_val_map["b"] == [[[4, 5], [6, 7]], [[8], [9]]]
    assert interpreter.lts.name_val_map["c"] == []
    interpreter.process_var_assigns("a[1][2]←a[1][1]+b[1][2][2]")
    assert interpreter.lts.name_val_map["a"] == [[1, 8], [3]]


def test_interpret_var_declare_n_array():
    interpreter = Interpreter()
    interpreter.interpret_var_declare("整数型の二次元配列: a←{{1,2},{3}}")
    interpreter.interpret_var_declare("整数型の三次元配列: b←{{{4,5},{6,7}},{{8},{9}}}")
    interpreter.interpret_var_declare("整数型配列: c←{}")
    assert interpreter.lts.name_val_map["a"] == [[1, 2], [3]]
    assert interpreter.lts.name_val_map["b"] == [[[4, 5], [6, 7]], [[8], [9]]]
    assert interpreter.lts.name_val_map["c"] == []
    interpreter.interpret_var_assign("a[1][2]←a[1][1]+b[1][2][2]")
    assert interpreter.lts.name_val_map["a"] == [[1, 8], [3]]


def test_process_var_assigns_array_invalid_access():
    interpreter = Interpreter()
    actual_list, remain = interpreter.process_var_assigns("a←{1+2,3}, b←{4,5*6}, c←{}")
    with pytest.raises(exception.InvalidArrayIndexException) as e:
        interpreter.process_var_assigns("d←a[1]+b[3]")
    assert str(e.value) == "bの配列外にアクセスしています。"


def test_interpret_var_declare():
    interpreter = Interpreter()
    remain = interpreter.interpret_var_declare("整数型：a←1, b, c←1+2+3")
    assert interpreter.lts.name_val_map["a"] == 1
    assert interpreter.lts.name_val_map["b"] is None
    assert interpreter.lts.name_val_map["c"] == 6
    assert interpreter.lts.name_type_map["a"] == "整数型"
    assert interpreter.lts.name_type_map["b"] == "整数型"
    assert interpreter.lts.name_type_map["c"] == "整数型"
    remain == ""


def test_interpret_var_declare_array():
    interpreter = Interpreter()
    interpreter.interpret_var_declare(
        "整数型の二次元配列: a ← {{0,1,2},{3,4,5},{6,7,8}}"
    )
    interpreter.interpret_var_declare(
        "整数型配列の配列： b ← {{8,7,6},{5,4,3},{2,1,0}}"
    )
    assert interpreter.lts.name_val_map["a"] == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    assert interpreter.lts.name_val_map["b"] == [[8, 7, 6], [5, 4, 3], [2, 1, 0]]


def test_interpret_var_assign():
    interpreter = Interpreter()
    remain = interpreter.interpret_var_declare("整数型：a←1")
    remain = interpreter.interpret_var_assign("a←a+2+3")
    assert interpreter.lts.name_val_map["a"] == 6
    assert remain == ""


def test_interpret_var_assign_array_append():
    interpreter = Interpreter()
    # TODO 配列への値の追加のテスト
    interpreter.interpret_var_declare("整数型の配列：a← {}")
    interpreter.interpret_var_declare("整数型配列の配列：b ← {{},{}}")
    interpreter.interpret_var_assign("aの末尾 に 1を追加する")
    interpreter.interpret_var_assign("b[1]の末尾 に {1,2,3}を追加する")
    print(interpreter.lts.name_val_map)
    assert interpreter.lts.name_val_map["a"] == [1]
    assert interpreter.lts.name_val_map["b"] == [[[1, 2, 3]], []]


def test_interpret_var_assign_invalid_array_append():
    interpreter = Interpreter()
    # TODO 配列への値の追加のテスト
    interpreter.interpret_var_declare("整数型の配列：a← {}")
    with pytest.raises(exception.InvalidArrayAppendException) as e:
        interpreter.interpret_var_assign("aの末尾 に 1を追加")
    assert str(e.value) == "配列への値の追加文が正しくありません。"


def test_interpret_var_assign_append_invalid_var():
    interpreter = Interpreter()
    # TODO 配列への値の追加のテスト
    interpreter.interpret_var_declare("整数型：a← 3")
    with pytest.raises(exception.InvalidArrayException) as e:
        interpreter.interpret_var_assign("aの末尾 に 1を追加する")
    assert str(e.value) == "aは配列ではありません。"


def test_process_var_assigns_and_use():
    interpreter = Interpreter()
    actual_list, remain = interpreter.process_var_assigns("a←1+2+3, b, c←5.4")

    assert actual_list == ["a", "b", "c"]
    assert interpreter.lts.name_val_map["a"] == 6
    assert interpreter.lts.name_val_map["b"] is None
    assert interpreter.lts.name_val_map["c"] == 5.4
    assert remain == ""

    interpreter.process_var_assigns("b←a + c * 2")
    assert interpreter.lts.name_val_map["b"] == 16.8
    actual_val, remain = interpreter.interpret_arithmetic_formula("a+b+c")
    assert actual_val == 16.8 + 5.4 + 6


def test_interpret_if_block():
    interpreter = Interpreter()
    lines = [
        "if(1>3)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "elseif(4<2)",
        "    整数型:a←4",
        "    整数型:b←5+1",
        "else",
        "    整数型:a←7",
        "    整数型:b←8",
        "endif",
        "c=a+b",
    ]
    remains = interpreter.interpret_if_block(lines, [])
    assert len(interpreter.lts.transitions) == 11
    assert interpreter.lts.get_transition_state("S0", "(1>3)") == "S1"
    assert interpreter.lts.get_transition_state("S1", "整数型:a←1+2") == "S2"
    assert interpreter.lts.get_transition_state("S2", "整数型:b←2+3") == "S3"
    assert interpreter.lts.get_transition_state("S3", "endif") == "S10"
    assert interpreter.lts.get_transition_state("S0", "(4<2)") == "S4"
    assert interpreter.lts.get_transition_state("S4", "整数型:a←4") == "S5"
    assert interpreter.lts.get_transition_state("S5", "整数型:b←5+1") == "S6"
    assert interpreter.lts.get_transition_state("S6", "endif") == "S10"
    assert interpreter.lts.get_transition_state("S0", "else") == "S7"
    assert interpreter.lts.get_transition_state("S7", "整数型:a←7") == "S8"
    assert interpreter.lts.get_transition_state("S8", "整数型:b←8") == "S9"
    assert interpreter.lts.get_transition_state("S9", "endif") == "S10"

    assert remains == 10


def test_interpret_if_block_without_any_else():
    interpreter = Interpreter()
    lines = [
        "if(1>3)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "endif",
        "c=a+b",
    ]
    remains = interpreter.interpret_if_block(lines, [])
    assert len(interpreter.lts.transitions) == 6
    assert interpreter.lts.get_transition_state("S0", "(1>3)") == "S1"
    assert interpreter.lts.get_transition_state("S1", "整数型:a←1+2") == "S2"
    assert interpreter.lts.get_transition_state("S2", "整数型:b←2+3") == "S3"
    assert interpreter.lts.get_transition_state("S3", "endif") == "S5"
    assert interpreter.lts.get_transition_state("S0", "else") == "S4"
    assert interpreter.lts.get_transition_state("S4", "endif") == "S5"

    assert remains == 4


def test_interpret_if_block_without_elseif():
    interpreter = Interpreter()
    lines = [
        "if(1>3)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "else",
        "    整数型:a←7",
        "    整数型:b←8",
        "endif",
        "c=a+b",
    ]
    remains = interpreter.interpret_if_block(lines, [])
    assert len(interpreter.lts.transitions) == 8
    assert interpreter.lts.get_transition_state("S0", "(1>3)") == "S1"
    assert interpreter.lts.get_transition_state("S1", "整数型:a←1+2") == "S2"
    assert interpreter.lts.get_transition_state("S2", "整数型:b←2+3") == "S3"
    assert interpreter.lts.get_transition_state("S3", "endif") == "S7"
    assert interpreter.lts.get_transition_state("S0", "else") == "S4"
    assert interpreter.lts.get_transition_state("S4", "整数型:a←7") == "S5"
    assert interpreter.lts.get_transition_state("S5", "整数型:b←8") == "S6"
    assert interpreter.lts.get_transition_state("S6", "endif") == "S7"

    assert remains == 7


def test_interpret_if_block_without_else():
    interpreter = Interpreter()
    lines = [
        "if(1>3)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "elseif(4<2)",
        "    整数型:a←4",
        "    整数型:b←5+1",
        "endif",
        "c=a+b",
    ]
    remains = interpreter.interpret_if_block(lines, [])
    assert len(interpreter.lts.transitions) == 9
    assert interpreter.lts.get_transition_state("S0", "(1>3)") == "S1"
    assert interpreter.lts.get_transition_state("S1", "整数型:a←1+2") == "S2"
    assert interpreter.lts.get_transition_state("S2", "整数型:b←2+3") == "S3"
    assert interpreter.lts.get_transition_state("S3", "endif") == "S8"
    assert interpreter.lts.get_transition_state("S0", "(4<2)") == "S4"
    assert interpreter.lts.get_transition_state("S4", "整数型:a←4") == "S5"
    assert interpreter.lts.get_transition_state("S5", "整数型:b←5+1") == "S6"
    assert interpreter.lts.get_transition_state("S6", "endif") == "S8"
    assert interpreter.lts.get_transition_state("S0", "else") == "S7"
    assert interpreter.lts.get_transition_state("S7", "endif") == "S8"

    assert remains == 7


def test_interpret_if_block_invalid_if_end():
    interpreter = Interpreter()
    lines = [
        "if(1>3)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "endi",
        "c=a+b",
    ]
    with pytest.raises(exception.InvalidIfBlockException) as e:
        interpreter.interpret_if_block(lines, [])

    # エラーメッセージを検証
    assert str(e.value) == "4行目:if文が正しく終了しませんでした。"


def test_interpret_if_block_invalid_indent():
    interpreter = Interpreter()
    lines = [
        "if(1>3)",
        "    整数型:a←1+2",
        "  整数型:b←2+3",
        "endif",
        "c=a+b",
    ]
    with pytest.raises(exception.InvalidIndentException) as e:
        interpreter.interpret_if_block(lines, [])

    # エラーメッセージを検証
    assert str(e.value) == "3行目:インデントに誤りがあります。"


def test_interpret_if_block_invalid_indent_elseif():
    interpreter = Interpreter()
    lines = [
        "if(1>3)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "elseif(4<2)",
        "    整数型:a←4",
        "  整数型:b←5+1",
        "endif",
        "c=a+b",
    ]

    with pytest.raises(exception.InvalidIndentException) as e:
        interpreter.interpret_if_block(lines, [])

    # エラーメッセージを検証
    assert str(e.value) == "6行目:インデントに誤りがあります。"


def test_interpret_if_block_invalid_indent_else():
    interpreter = Interpreter()
    lines = [
        "if(1>3)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "else",
        "    整数型:a←7",
        "  整数型:b←8",
        "endif",
        "c=a+b",
    ]
    with pytest.raises(exception.InvalidIndentException) as e:
        interpreter.interpret_if_block(lines, [])

    # エラーメッセージを検証
    assert str(e.value) == "6行目:インデントに誤りがあります。"


def test_interpret_nested_if_block():
    interpreter = Interpreter()
    lines = [
        "if(1>3)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "    if(4<2)",
        "        整数型:a←4",
        "        整数型:b←5+1",
        "    else",
        "        整数型:a←7",
        "        整数型:b←8+2",
        "        return",
        "    endif",
        "endif",
        "c=a+b",
    ]
    actual_returns = []
    remains = interpreter.interpret_if_block(lines, actual_returns)
    assert len(interpreter.lts.transitions) == 13
    print(interpreter.lts)
    assert interpreter.lts.get_transition_state("S0", "(1>3)") == "S1"
    assert interpreter.lts.get_transition_state("S1", "整数型:a←1+2") == "S2"
    assert interpreter.lts.get_transition_state("S2", "整数型:b←2+3") == "S3"
    assert interpreter.lts.get_transition_state("S3", "(4<2)") == "S4"
    assert interpreter.lts.get_transition_state("S4", "整数型:a←4") == "S5"
    assert interpreter.lts.get_transition_state("S5", "整数型:b←5+1") == "S6"
    assert interpreter.lts.get_transition_state("S6", "endif") == "S10"
    assert interpreter.lts.get_transition_state("S3", "else") == "S7"
    assert interpreter.lts.get_transition_state("S7", "整数型:a←7") == "S8"
    assert interpreter.lts.get_transition_state("S8", "整数型:b←8+2") == "S9"
    assert interpreter.lts.get_transition_state("S9", "endif") == "S10"
    assert interpreter.lts.get_transition_state("S10", "endif") == "S12"
    assert interpreter.lts.get_transition_state("S0", "else") == "S11"
    assert interpreter.lts.get_transition_state("S11", "endif") == "S12"
    assert ("S9", "return") in actual_returns
    assert remains == 12


def test_interpret_while_block():
    interpreter = Interpreter()
    lines = [
        "while(a>4)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "endwhile",
        "c=a+b",
    ]
    remains = interpreter.interpret_while_block(lines, [])
    print(interpreter.lts)
    assert len(interpreter.lts.transitions) == 5
    assert interpreter.lts.get_transition_state("S0", "(a>4)") == "S1"
    assert interpreter.lts.get_transition_state("S0", "endwhile") == "S4"
    assert interpreter.lts.get_transition_state("S1", "整数型:a←1+2") == "S2"
    assert interpreter.lts.get_transition_state("S2", "整数型:b←2+3") == "S3"
    assert interpreter.lts.get_transition_state("S3", "") == "S0"

    assert remains == 4


def test_interpret_nested_while_block():
    interpreter = Interpreter()
    lines = [
        "while(1>3)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "    while(4<2)",
        "        整数型:a←4",
        "        整数型:b←5+1",
        "        if(a>4)",
        "            整数型:a←6+1",
        "            整数型:b←7+2",
        "        else",
        "            return",
        "        endif",
        "    endwhile",
        "endwhile",
        "c=a+b",
    ]
    actual_returns = []
    remains = interpreter.interpret_while_block(lines, actual_returns)
    assert len(interpreter.lts.transitions) == 14
    print(interpreter.lts)
    assert interpreter.lts.get_transition_state("S0", "(1>3)") == "S1"
    assert interpreter.lts.get_transition_state("S0", "endwhile") == "S13"
    assert interpreter.lts.get_transition_state("S1", "整数型:a←1+2") == "S2"
    assert interpreter.lts.get_transition_state("S2", "整数型:b←2+3") == "S3"
    assert interpreter.lts.get_transition_state("S3", "(4<2)") == "S4"
    assert interpreter.lts.get_transition_state("S3", "endwhile") == "S12"
    assert interpreter.lts.get_transition_state("S4", "整数型:a←4") == "S5"
    assert interpreter.lts.get_transition_state("S5", "整数型:b←5+1") == "S6"
    assert interpreter.lts.get_transition_state("S6", "(a>4)") == "S7"
    assert interpreter.lts.get_transition_state("S7", "整数型:a←6+1") == "S8"
    assert interpreter.lts.get_transition_state("S8", "整数型:b←7+2") == "S9"
    assert interpreter.lts.get_transition_state("S9", "endif") == "S11"
    assert interpreter.lts.get_transition_state("S6", "else") == "S10"
    assert interpreter.lts.get_transition_state("S10", "endif") == "S11"
    assert interpreter.lts.get_transition_state("S11", "") == "S3"
    assert interpreter.lts.get_transition_state("S12", "") == "S0"
    assert ("S10", "return") in actual_returns

    assert remains == 14


def test_interpret_while_block_invalid_end():
    interpreter = Interpreter()
    lines = [
        "while(1>3)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "endwhil",
        "c=a+b",
    ]
    with pytest.raises(exception.InvalidWhileBlockException) as e:
        interpreter.interpret_while_block(lines, [])
        print(interpreter.lts)

    # エラーメッセージを検証
    assert str(e.value) == "4行目:while文が正しく終了しませんでした。"


def test_interpret_while_block_invalid_indent():
    interpreter = Interpreter()
    lines = [
        "while(a>4)",
        "    整数型:a←1+2",
        "  整数型:b←2+3",
        "endwhile",
        "c=a+b",
    ]
    with pytest.raises(exception.InvalidIndentException) as e:
        interpreter.interpret_while_block(lines, [])

    # エラーメッセージを検証
    assert str(e.value) == "3行目:インデントに誤りがあります。"


def test_interpret_do_while_block():
    interpreter = Interpreter()
    lines = [
        "do",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "while(a>4)",
        "c=a+b",
    ]
    remains = interpreter.interpret_do_while_block(lines, [])
    print(interpreter.lts)
    assert len(interpreter.lts.transitions) == 5
    assert interpreter.lts.get_transition_state("S0", "do") == "S1"
    assert interpreter.lts.get_transition_state("S1", "整数型:a←1+2") == "S2"
    assert interpreter.lts.get_transition_state("S2", "整数型:b←2+3") == "S3"
    assert interpreter.lts.get_transition_state("S3", "(a>4)") == "S0"
    assert interpreter.lts.get_transition_state("S3", "else") == "S4"

    assert remains == 4


def test_interpret_nested_do_while_block():
    interpreter = Interpreter()
    lines = [
        "do",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "    while(4<2)",
        "        整数型:a←4",
        "        整数型:b←5+1",
        "        if(a>4)",
        "            整数型:a←6+1",
        "            整数型:b←7+2",
        "        else",
        "            return",
        "        endif",
        "    endwhile",
        "while(1>3)",
        "c=a+b",
    ]
    actual_returns = []
    remains = interpreter.interpret_do_while_block(lines, actual_returns)
    assert len(interpreter.lts.transitions) == 14
    print(interpreter.lts)
    assert interpreter.lts.get_transition_state("S0", "do") == "S1"
    assert interpreter.lts.get_transition_state("S1", "整数型:a←1+2") == "S2"
    assert interpreter.lts.get_transition_state("S2", "整数型:b←2+3") == "S3"
    assert interpreter.lts.get_transition_state("S3", "(4<2)") == "S4"
    assert interpreter.lts.get_transition_state("S3", "endwhile") == "S12"
    assert interpreter.lts.get_transition_state("S4", "整数型:a←4") == "S5"
    assert interpreter.lts.get_transition_state("S5", "整数型:b←5+1") == "S6"
    assert interpreter.lts.get_transition_state("S6", "(a>4)") == "S7"
    assert interpreter.lts.get_transition_state("S7", "整数型:a←6+1") == "S8"
    assert interpreter.lts.get_transition_state("S8", "整数型:b←7+2") == "S9"
    assert interpreter.lts.get_transition_state("S9", "endif") == "S11"
    assert interpreter.lts.get_transition_state("S6", "else") == "S10"
    assert interpreter.lts.get_transition_state("S10", "endif") == "S11"
    assert interpreter.lts.get_transition_state("S11", "") == "S3"
    assert interpreter.lts.get_transition_state("S12", "(1>3)") == "S0"
    assert interpreter.lts.get_transition_state("S12", "else") == "S13"
    assert ("S10", "return") in actual_returns
    assert remains == 14


def test_interpret_do_while_block_invalid_end():
    interpreter = Interpreter()
    lines = [
        "do",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "whil(1>3)",
        "c=a+b",
    ]
    with pytest.raises(exception.InvalidDoWhileBlockException) as e:
        interpreter.interpret_do_while_block(lines, [])
        print(interpreter.lts)

    # エラーメッセージを検証
    assert str(e.value) == "4行目:do while文が正しく終了しませんでした。"


def test_interpret_do_while_block_invalid_indent():
    interpreter = Interpreter()
    lines = [
        "do",
        "    整数型:a←1+2",
        "  整数型:b←2+3",
        "while(a>4)",
        "c=a+b",
    ]
    with pytest.raises(exception.InvalidIndentException) as e:
        interpreter.interpret_do_while_block(lines, [])

    # エラーメッセージを検証
    assert str(e.value) == "3行目:インデントに誤りがあります。"


def test_interpret_for_block():
    interpreter = Interpreter()
    lines = [
        "for (aを1から4まで繰り返す)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "endfor",
        "c=a+b",
    ]
    remains = interpreter.interpret_for_block(lines, [])
    print(interpreter.lts)
    assert len(interpreter.lts.transitions) == 5
    assert interpreter.lts.get_transition_state("S0", "(aを1から4まで繰り返す)") == "S1"
    assert interpreter.lts.get_transition_state("S0", "endfor") == "S4"
    assert interpreter.lts.get_transition_state("S1", "整数型:a←1+2") == "S2"
    assert interpreter.lts.get_transition_state("S2", "整数型:b←2+3") == "S3"
    assert interpreter.lts.get_transition_state("S3", "") == "S0"

    assert remains == 4


def test_interpret_nested_for_block():
    interpreter = Interpreter()
    lines = [
        "for (aを1から4まで繰り返す)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "    while(4<2)",
        "        整数型:a←4",
        "        整数型:b←5+1",
        "        if(a>4)",
        "            整数型:a←6+1",
        "            整数型:b←7+2",
        "        else",
        "            return",
        "        endif",
        "    endwhile",
        "endfor",
        "c=a+b",
    ]
    actual_returns = []
    remains = interpreter.interpret_for_block(lines, actual_returns)
    print(interpreter.lts)
    assert len(interpreter.lts.transitions) == 14
    assert interpreter.lts.get_transition_state("S0", "(aを1から4まで繰り返す)") == "S1"
    assert interpreter.lts.get_transition_state("S0", "endfor") == "S13"
    assert interpreter.lts.get_transition_state("S1", "整数型:a←1+2") == "S2"
    assert interpreter.lts.get_transition_state("S2", "整数型:b←2+3") == "S3"
    assert interpreter.lts.get_transition_state("S3", "(4<2)") == "S4"
    assert interpreter.lts.get_transition_state("S3", "endwhile") == "S12"
    assert interpreter.lts.get_transition_state("S4", "整数型:a←4") == "S5"
    assert interpreter.lts.get_transition_state("S5", "整数型:b←5+1") == "S6"
    assert interpreter.lts.get_transition_state("S6", "(a>4)") == "S7"
    assert interpreter.lts.get_transition_state("S7", "整数型:a←6+1") == "S8"
    assert interpreter.lts.get_transition_state("S8", "整数型:b←7+2") == "S9"
    assert interpreter.lts.get_transition_state("S9", "endif") == "S11"
    assert interpreter.lts.get_transition_state("S6", "else") == "S10"
    assert interpreter.lts.get_transition_state("S10", "endif") == "S11"
    assert interpreter.lts.get_transition_state("S11", "") == "S3"
    assert interpreter.lts.get_transition_state("S12", "") == "S0"
    assert ("S10", "return") in actual_returns
    assert remains == 14


def test_interpret_for_block_invalid_end():
    interpreter = Interpreter()
    lines = [
        "for (aを1から4まで繰り返す)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "endfo",
        "c=a+b",
    ]
    with pytest.raises(exception.InvalidForBlockException) as e:
        interpreter.interpret_for_block(lines, [])

    # エラーメッセージを検証
    assert str(e.value) == "4行目:for文が正しく終了しませんでした。"


def test_interpret_for_block_invalid_indent():
    interpreter = Interpreter()
    lines = [
        "for (aを1から4まで繰り返す)",
        "    整数型:a←1+2",
        "  整数型:b←2+3",
        "endfor",
        "c=a+b",
    ]
    with pytest.raises(exception.InvalidIndentException) as e:
        interpreter.interpret_for_block(lines, [])

    # エラーメッセージを検証
    assert str(e.value) == "3行目:インデントに誤りがあります。"


def test_interpret_func_block():
    interpreter = Interpreter()
    lines = [
        "◯ test_func(整数型:x)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "c=a+b",
    ]
    remains = interpreter.interpret_func_block(lines)
    print(interpreter.lts)
    assert "test_func" in interpreter.func_lts_map
    test_func_lts = interpreter.func_lts_map["test_func"]
    assert len(test_func_lts.transitions) == 4
    assert len(interpreter.lts.transitions) == 1
    assert test_func_lts.get_transition_state("S0", "整数型:a←1+2") == "S1"
    assert test_func_lts.get_transition_state("S1", "整数型:b←2+3") == "S2"
    assert test_func_lts.get_transition_state("S2", "return") == "S3"

    assert remains == 3


def test_interpret_nested_func_block():
    interpreter = Interpreter()
    lines = [
        "◯ test_func(整数型:x)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "    while(4<2)",
        "        整数型:a←4",
        "        整数型:b←5+1",
        "        if(a>4)",
        "            整数型:a←6+1",
        "            整数型:b←7+2",
        "        else",
        "            return",
        "        endif",
        "    endwhile",
        "c=a+b",
    ]
    remains = interpreter.interpret_func_block(lines)
    print(interpreter.func_lts_map["test_func"])
    assert "test_func" in interpreter.func_lts_map
    test_func_lts = interpreter.func_lts_map["test_func"]
    assert len(test_func_lts.transitions) == 13
    assert len(interpreter.lts.transitions) == 1
    print(interpreter.lts)
    assert test_func_lts.get_transition_state("S0", "整数型:a←1+2") == "S1"
    assert test_func_lts.get_transition_state("S1", "整数型:b←2+3") == "S2"
    assert test_func_lts.get_transition_state("S2", "(4<2)") == "S3"
    assert test_func_lts.get_transition_state("S2", "endwhile") == "S11"
    assert test_func_lts.get_transition_state("S11", "return") == "S12"
    assert test_func_lts.get_transition_state("S3", "整数型:a←4") == "S4"
    assert test_func_lts.get_transition_state("S4", "整数型:b←5+1") == "S5"
    assert test_func_lts.get_transition_state("S5", "(a>4)") == "S6"
    assert test_func_lts.get_transition_state("S6", "整数型:a←6+1") == "S7"
    assert test_func_lts.get_transition_state("S7", "整数型:b←7+2") == "S8"
    assert test_func_lts.get_transition_state("S8", "endif") == "S10"
    assert test_func_lts.get_transition_state("S5", "else") == "S9"
    assert test_func_lts.get_transition_state("S9", "return") == "S12"
    assert test_func_lts.get_transition_state("S10", "") == "S2"

    assert remains == 13


def test_interpret_func_block_invalid_indent():
    interpreter = Interpreter()
    lines = [
        "◯ test_func(整数型:x)",
        "    整数型:a←1+2",
        "  整数型:b←2+3",
        "c=a+b",
    ]
    with pytest.raises(exception.InvalidIndentException) as e:
        interpreter.interpret_func_block(lines)

    # エラーメッセージを検証
    assert str(e.value) == "3行目:インデントに誤りがあります。"


def test_interpret_main_process():
    interpreter = Interpreter()

    lines = [
        "◯ test_func(整数型:x)",
        "    if (xが5以上)",
        "        x←x+1",
        "    elseif (xが3以上)",
        "        x←x+5",
        "    else",
        "        x←x+12",
        "        return x",
        "    endif",
        "    x←x%2",
        "    return x",
        "整数型:x",
        "x←2",
        "for (iを1から10まで繰り返す)",
        "    while (xは10以上)",
        "        x←x-10",
        "    endwhile",
        "    x←test_func(x)",
        "endfor",
        "if (xは10以上)",
        "    x←x-10",
        "endif",
    ]
    remains = interpreter.interpret_main_process(lines)
    print(interpreter.func_lts_map["test_func"])
    print(interpreter.lts)
    assert "test_func" in interpreter.func_lts_map
    test_func_lts = interpreter.func_lts_map["test_func"]
    assert len(test_func_lts.transitions) == 10
    assert len(interpreter.lts.transitions) == 14

    assert test_func_lts.get_transition_state("S0", "(xが5以上)") == "S1"
    assert test_func_lts.get_transition_state("S1", "x←x+1") == "S2"
    assert test_func_lts.get_transition_state("S2", "endif") == "S7"
    assert test_func_lts.get_transition_state("S0", "(xが3以上)") == "S3"
    assert test_func_lts.get_transition_state("S3", "x←x+5") == "S4"
    assert test_func_lts.get_transition_state("S4", "endif") == "S7"
    assert test_func_lts.get_transition_state("S0", "else") == "S5"
    assert test_func_lts.get_transition_state("S5", "x←x+12") == "S6"
    assert test_func_lts.get_transition_state("S6", "return x") == "S9"
    assert test_func_lts.get_transition_state("S7", "x←x%2") == "S8"
    assert test_func_lts.get_transition_state("S8", "return x") == "S9"

    assert interpreter.lts.get_transition_state("S0", "整数型:x") == "S1"
    assert interpreter.lts.get_transition_state("S1", "x←2") == "S2"
    assert (
        interpreter.lts.get_transition_state("S2", "(iを1から10まで繰り返す)") == "S3"
    )
    assert interpreter.lts.get_transition_state("S2", "endfor") == "S8"
    assert interpreter.lts.get_transition_state("S3", "(xは10以上)") == "S4"
    assert interpreter.lts.get_transition_state("S3", "endwhile") == "S6"
    assert interpreter.lts.get_transition_state("S4", "x←x-10") == "S5"
    assert interpreter.lts.get_transition_state("S5", "") == "S3"
    assert interpreter.lts.get_transition_state("S6", "x←test_func(x)") == "S7"
    assert interpreter.lts.get_transition_state("S7", "") == "S2"
    assert interpreter.lts.get_transition_state("S8", "(xは10以上)") == "S9"
    assert interpreter.lts.get_transition_state("S9", "x←x-10") == "S10"
    assert interpreter.lts.get_transition_state("S10", "endif") == "S12"
    assert interpreter.lts.get_transition_state("S8", "else") == "S11"
    assert interpreter.lts.get_transition_state("S11", "endif") == "S12"
    assert interpreter.lts.get_transition_state("S12", "return") == "S13"


def test_execute_lts_declare_assign_formula():
    interpreter = Interpreter()

    lines = [
        "整数型: x, y←2, z←1+4, w ← 10 & 6, v ← 10 | 6",
        "論理型: a, b",
        "x← (1 ＋ 2) ÷ 3 × (4 mod 5)",
        "w ≠ v",
        "a← x ≧ y かつ y ≦ z",
        "b← a または z ≠ 5",
    ]
    interpreter.interpret_main_process(lines)
    interpreter.execute_lts()
    assert interpreter.lts.name_val_map["x"] == 4
    assert interpreter.lts.name_val_map["y"] == 2
    assert interpreter.lts.name_val_map["z"] == 5
    assert interpreter.lts.name_val_map["w"] == 2
    assert interpreter.lts.name_val_map["v"] == 14
    assert interpreter.lts.name_val_map["a"]
    assert interpreter.lts.name_val_map["b"]


def test_execute_lts_func():
    interpreter = Interpreter()

    lines = ["◯ test_gt(整数型:a, 整数型:b)", "    return a > b"]
    interpreter.interpret_main_process(lines)
    lts = interpreter.func_lts_map["test_gt"]
    assert interpreter.execute_lts(lts, vars=[3, 2])
    assert not interpreter.execute_lts(lts, vars=[2, 3])


def test_execute_lts_func_invalid_call():
    interpreter = Interpreter()

    lines = ["◯ test_gt(整数型:a, 整数型:b)", "    return a > b"]
    interpreter.interpret_main_process(lines)
    lts = interpreter.func_lts_map["test_gt"]
    with pytest.raises(exception.InvalidFuncCallException):
        assert interpreter.execute_lts(lts, vars=[3])


def test_execute_lts_func_call():
    interpreter = Interpreter()

    lines = [
        "◯ test_gt(整数型:a, 整数型:b)",
        "    return a > b",
        "整数型: a←3, b←2",
        "論理型: c←test_gt(a,b)",
    ]
    interpreter.interpret_main_process(lines)
    interpreter.execute_lts()
    assert interpreter.lts.name_val_map["c"]


def test_execute_lts_if_process():
    interpreter = Interpreter()

    lines = [
        "◯ test_func(整数型:x)",
        "    if (xが5以上)",
        "        x←x+1",
        "    elseif (xが3以上)",
        "        x←x+5",
        "    else",
        "        x←x+12",
        "        return x",
        "    endif",
        "    x←x/2",
        "    return x",
    ]
    interpreter.interpret_main_process(lines)
    lts = interpreter.func_lts_map["test_func"]
    interpreter.execute_lts(lts, vars=[6])
    assert lts.name_val_map["x"] == 3.5
    interpreter.execute_lts(lts, vars=[4])
    assert lts.name_val_map["x"] == 4.5
    interpreter.execute_lts(lts, vars=[2])
    assert lts.name_val_map["x"] == 14


def test_execute_lts_for_process():
    interpreter = Interpreter()

    lines = [
        "整数型: a, x←0",
        "for (aを1から10まで2ずつ増やす)",
        "    x←x+a",
        "endfor",
        "return x",
    ]
    interpreter = Interpreter()
    interpreter.interpret_main_process(lines)
    assert interpreter.execute_lts() == 25


def test_execute_lts_for_process_var():
    interpreter = Interpreter()

    lines = [
        "整数型: a, x←0, end←10, start← 2, increment←2",
        "for (aをstartからendまでincrementずつ増やす)",
        "    x←x+a",
        "endfor",
        "return x",
    ]
    interpreter = Interpreter()
    interpreter.interpret_main_process(lines)
    assert interpreter.execute_lts() == 30


def test_execute_lts_while_process():
    interpreter = Interpreter()

    lines = [
        "整数型: x←0",
        "while (x<10)",
        "    x←x+1",
        "endwhile",
        "return x",
    ]
    interpreter = Interpreter()
    interpreter.interpret_main_process(lines)
    assert interpreter.execute_lts() == 10


def test_execute_lts_with_no_while_process():
    interpreter = Interpreter()

    lines = [
        "整数型: x←11",
        "while (x<10)",
        "    x←x+1",
        "endwhile",
        "return x",
    ]
    interpreter = Interpreter()
    interpreter.interpret_main_process(lines)
    assert interpreter.execute_lts() == 11


def test_execute_lts_do_while_process():
    interpreter = Interpreter()

    lines = [
        "整数型: x←0",
        "do",
        "    x←x+1",
        "while (x<10)",
        "return x",
    ]
    interpreter = Interpreter()
    interpreter.interpret_main_process(lines)
    assert interpreter.execute_lts() == 10


def test_execute_lts_do_while_with_one_process():
    interpreter = Interpreter()

    lines = [
        "整数型: x←11",
        "do",
        "    x←x+1",
        "while (x<10)",
        "return x",
    ]
    interpreter = Interpreter()
    interpreter.interpret_main_process(lines)
    assert interpreter.execute_lts() == 12


def test_interpret_sample1():
    lines = [
        "○整数型: fee(整数型: age)",
        "    整数型: ret",
        "    if (age が 3 以下)",
        "        ret ← 100",
        "    elseif (age が 9 以下)",
        "        ret ← 300",
        "    else",
        "        ret ← 500",
        "    endif",
        "    return ret",
        "整数型: ann ← 8",
        "整数型: fee_value ← fee(ann) ",
    ]
    interpreter = Interpreter()
    interpreter.interpret_main_process(lines)
    interpreter.execute_lts()
    assert interpreter.lts.name_val_map["fee_value"] == 300


def test_interpret_sample2():
    lines = [
        "整数型の配列: array ← {1, 2, 3, 4, 5}",
        "整数型: right, left",
        "整数型: tmp",
        "for (left を 1 から (arrayの要素数 ÷ 2 の商) まで 1 ずつ増やす)",
        "    right ← array の要素数 － left ＋ 1",
        "    tmp ← array[right]",
        "    array[right] ← array[left]",
        "    array[left] ← tmp",
        "endfor",
    ]
    interpreter = Interpreter()
    interpreter.interpret_main_process(lines)
    print(interpreter.lts)
    interpreter.execute_lts()
    assert interpreter.lts.name_val_map["array"] == [5, 4, 3, 2, 1]


def test_interpret_sample3():
    lines = [
        "○整数型配列の配列: transformSparseMatrix(整数型の二次元配列: matrix)",
        "    整数型: i, j",
        "    整数型配列の配列: sparseMatrix",
        "    sparseMatrix ← {{}, {}, {}}",
        "    for (i を 1 から matrixの行数 まで 1 ずつ増やす)",
        "        for (j を 1 から matrixの列数 まで 1 ずつ増やす)",
        "            if (matrix[i][j] が 0 でない)",
        "                sparseMatrix[1]の末尾 に iの値 を追加する",
        "                sparseMatrix[2]の末尾 に jの値 を追加する",
        "                sparseMatrix[3]の末尾 に matrix[i][j]の値 を追加する",
        "            endif",
        "        endfor",
        "    endfor",
        "    return sparseMatrix",
    ]
    interpreter = Interpreter()
    interpreter.interpret_main_process(lines)
    print(interpreter.func_lts_map["transformSparseMatrix"])
    test_list = [
        [3, 0, 0, 0, 0],
        [0, 2, 2, 0, 0],
        [0, 0, 0, 1, 3],
        [0, 0, 0, 2, 0],
        [0, 0, 0, 0, 1],
    ]
    actual_val = interpreter.execute_lts(
        interpreter.func_lts_map["transformSparseMatrix"], vars=[test_list]
    )
    print(interpreter.func_lts_map["transformSparseMatrix"].name_val_map)
    assert actual_val == [
        [1, 2, 2, 3, 3, 4, 5],
        [1, 2, 3, 4, 5, 4, 5],
        [3, 2, 2, 1, 3, 2, 1],
    ]
