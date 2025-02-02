# evaluator.py - 密码强度评估模块


def evaluate_password_strength(password):
    """评估密码强度 (简单示例)"""
    length_score = len(password) * 4
    digit_score = sum(c.isdigit() for c in password) * 4
    special_char_score = sum(c in "!@#*~" for c in password) * 5
    lowercase_score = sum(c.islower() for c in password) * 2
    uppercase_score = sum(c.isupper() for c in password) * 2
    total_score = (
        length_score
        + digit_score
        + special_char_score
        + lowercase_score
        + uppercase_score
    )
    return total_score
