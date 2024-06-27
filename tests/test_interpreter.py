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
    actual_val, remain = interpreter.process_mul_div("*2*6/3", [], 1)
    assert actual_val == 2
    assert remain == "*6/3"


def test_process_add_sub():
    interpreter = Interpreter()

    actual_val, remain = interpreter.process_add_sub("+2+3-4", [], 1)
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
