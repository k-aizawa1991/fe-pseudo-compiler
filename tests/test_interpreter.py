from src.interpreter import Interpreter


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
