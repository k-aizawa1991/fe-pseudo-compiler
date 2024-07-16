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
    actual_val == 15
    assert remain == ""

    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("3 & 12")
    actual_val == 0
    assert remain == ""


def test_process_var_assigns():
    interpreter = Interpreter()
    actual_list, remain = interpreter.process_var_assigns("a←1+2+3, b, c←5")

    assert actual_list == ["a", "b", "c"]
    assert interpreter.name_val_map["a"] == 6
    assert interpreter.name_val_map["b"] is None
    assert interpreter.name_val_map["c"] == 5
    assert remain == ""


def test_interpret_var_declare():
    interpreter = Interpreter()
    remain = interpreter.interpret_var_declare("整数型：a←1, b, c←1+2+3")
    assert interpreter.name_val_map["a"] == 1
    assert interpreter.name_val_map["b"] is None
    assert interpreter.name_val_map["c"] == 6
    assert interpreter.name_type_map["a"] == "整数型"
    assert interpreter.name_type_map["b"] == "整数型"
    assert interpreter.name_type_map["c"] == "整数型"
    remain == ""


def test_process_var_assigns_and_use():
    interpreter = Interpreter()
    actual_list, remain = interpreter.process_var_assigns("a←1+2+3, b, c←5.4")

    assert actual_list == ["a", "b", "c"]
    assert interpreter.name_val_map["a"] == 6
    assert interpreter.name_val_map["b"] is None
    assert interpreter.name_val_map["c"] == 5.4
    assert remain == ""

    interpreter.process_var_assigns("b←a + c * 2")
    assert interpreter.name_val_map["b"] == 16.8
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
    remains = interpreter.interpret_if_block(lines)
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
    remains = interpreter.interpret_if_block(lines)
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
    remains = interpreter.interpret_if_block(lines)
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
    remains = interpreter.interpret_if_block(lines)
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
        interpreter.interpret_if_block(lines)

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
        interpreter.interpret_if_block(lines)

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
        interpreter.interpret_if_block(lines)

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
        interpreter.interpret_if_block(lines)

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
        "    endif",
        "endif",
        "c=a+b",
    ]
    remains = interpreter.interpret_if_block(lines)
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

    assert remains == 11


def test_interpret_while_block():
    interpreter = Interpreter()
    lines = [
        "while(a>4)",
        "    整数型:a←1+2",
        "    整数型:b←2+3",
        "endwhile",
        "c=a+b",
    ]
    remains = interpreter.interpret_while_block(lines)
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
        "        endif",
        "    endwhile",
        "endwhile",
        "c=a+b",
    ]
    remains = interpreter.interpret_while_block(lines)
    print(interpreter.lts)
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

    assert remains == 12


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
        interpreter.interpret_while_block(lines)
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
        interpreter.interpret_while_block(lines)

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
    remains = interpreter.interpret_do_while_block(lines)
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
        "        endif",
        "    endwhile",
        "while(1>3)",
        "c=a+b",
    ]
    remains = interpreter.interpret_do_while_block(lines)
    print(interpreter.lts)
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

    assert remains == 12


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
        interpreter.interpret_do_while_block(lines)
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
        interpreter.interpret_do_while_block(lines)

    # エラーメッセージを検証
    assert str(e.value) == "3行目:インデントに誤りがあります。"
