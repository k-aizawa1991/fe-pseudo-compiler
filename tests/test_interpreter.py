from src.interpreter import Interpreter


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


def test_interpret_arithmetic_formula_double_mul():
    interpreter = Interpreter()
    actual_val, remain = interpreter.interpret_arithmetic_formula("1*2*3-4", [])
    assert actual_val == 2
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
