from src.dice import is_drop_instruction, is_math_expression, is_roll_instruction


def test_is_roll_instruction():
    assert is_roll_instruction("4d6") == True
    assert is_roll_instruction("20d5") == True
    assert is_roll_instruction("2d50") == True
    assert is_roll_instruction("40d50") == True
    assert is_roll_instruction("4D6") == False
    assert is_roll_instruction("dl") == False
    assert is_roll_instruction("dh") == False
    assert is_roll_instruction("+") == False
    assert is_roll_instruction("-") == False
    assert is_roll_instruction("+4d6") == False
    assert is_roll_instruction("-4d6") == False
    assert is_roll_instruction("bajs") == False


def test_is_drop_instruction():
    assert is_drop_instruction("dl") == True
    assert is_drop_instruction("dh") == True
    assert is_drop_instruction("d2l") == True
    assert is_drop_instruction("d2h") == True
    assert is_drop_instruction("d2hl") == False
    assert is_drop_instruction("d2lh") == False
    assert is_drop_instruction("d20l") == True
    assert is_drop_instruction("d20h") == True
    assert is_drop_instruction("4d20ls") == False
    assert is_drop_instruction("4d20") == False
    assert is_drop_instruction("bajs") == False


def test_is_math_expression():
    assert is_math_expression("+4") == True
    assert is_math_expression("-4") == True
    assert is_math_expression("+4d4") == True
    assert is_math_expression("-4d4") == True
    assert is_math_expression("+4") == True
    assert is_math_expression("4d6") == False
    assert is_math_expression("dl") == False
    assert is_math_expression("d6l") == False
    assert is_math_expression("-") == False
    assert is_math_expression("+") == False
    assert is_math_expression("bajs") == False
