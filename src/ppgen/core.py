# core.py - 核心密码生成逻辑
import random
import re
from importlib import resources
from .evaluator import evaluate_password_strength


def load_word_list():
    """加载词表文件,返回汉字和拼音的字典"""
    word_dict = {}
    try:
        with resources.open_text("ppgen", "chinese_words.txt") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    word = parts[0]
                    pinyin_with_tones = parts[1]
                    char_count = len(re.findall(r"\d", pinyin_with_tones))  # 计算字数
                    pinyin = re.sub(r"\d", "", pinyin_with_tones)  # 移除拼音中的数字
                    word_dict[word] = {
                        "pinyin": pinyin.replace("'", ""),  # 移除分隔符
                        "char_count": char_count,
                    }
    except FileNotFoundError:
        print("Error: 词表文件未找到.")
        return None
    return word_dict


def capitalize_pinyin(pinyin):
    """将拼音首字母大写

    Args:
        pinyin: 拼音字符串

    Returns:
        str: 首字母大写的拼音
    """
    return pinyin[0].upper() + pinyin[1:] if pinyin else pinyin


def generate_complex_password(word_dict, min_length=10, capitalize=False):
    """使用拼音生成复杂密码

    Args:
        word_dict: 汉字和拼音的字典
        min_length: 密码最小长度,默认为10

    Returns:
        tuple: (密码字符串, 对应的汉字字符串)
    """
    special_chars = "!@#*~"
    numbers = "0123456789"

    # 生成足够长的拼音组合
    pinyins = []
    chinese_chars = []
    while (
        sum(len(p) for p in pinyins) < min_length - 3
    ):  # 预留3个字符用于特殊字符和数字
        word = random.choice(list(word_dict.keys()))
        pinyin = word_dict[word]["pinyin"]
        if capitalize:
            pinyin = capitalize_pinyin(pinyin)
        pinyins.append(pinyin)
        chinese_chars.append(word)

    # 用特殊字符或数字隔开拼音
    password = []
    separators = []  # 记录分隔符
    for i, pinyin in enumerate(pinyins):
        password.extend(list(pinyin))
        # 在拼音之间添加分隔符，最后一个拼音后不添加
        if i < len(pinyins) - 1:
            if random.random() < 0.5:
                sep = random.choice(special_chars)
            else:
                sep = random.choice(numbers)
            password.append(sep)
            separators.append(sep)

    # 在末尾添加两个特殊字符或数字
    final_chars = []
    for _ in range(2):
        if random.random() < 0.5:
            char = random.choice(special_chars)
        else:
            char = random.choice(numbers)
        password.append(char)
        final_chars.append(char)

    # 构建提示信息：汉字(拼音)格式
    hints = []
    for i, (char, pinyin) in enumerate(zip(chinese_chars, pinyins)):
        hints.append(f"{char}({pinyin})")
        if i < len(separators):  # 添加分隔符
            hints.append(separators[i])
    hints.extend(final_chars)  # 添加末尾的特殊字符/数字

    return "".join(password), "".join(hints)


def generate_passphrase(
    word_dict, min_length=10, word_count=4, character_count=2, capitalize=False
):
    """生成 passphrase

    Args:
        word_dict: 汉字和拼音的字典
        min_length: 密码最小长度,默认为10
        word_count: 使用的拼音词数量,如果指定则忽略min_length。默认None时至少使用3个词。
        character_count: 指定单个词有几个字

    Returns:
        tuple: (passphrase字符串, 对应的汉字提示)
    """
    pinyins = []
    chinese_chars = []

    if word_count is not None:
        # 使用指定数量的词，但确保至少3个
        actual_count = max(3, word_count)
        # 先过滤出符合字数要求的词
        valid_words = [
            word
            for word in word_dict.keys()
            if word_dict[word]["char_count"] == character_count
        ]
        if not valid_words:
            return "", "没有找到符合字数要求的词"

        words = random.sample(valid_words, actual_count)
        chinese_chars.extend(words)
        for word in words:
            pinyin = word_dict[word]["pinyin"]
            if capitalize:
                pinyin = capitalize_pinyin(pinyin)
            pinyins.append(pinyin)
    else:
        # 使用min_length模式，但确保至少3个词
        while len(pinyins) < 3 or sum(len(p) for p in pinyins) < min_length:
            # 先过滤出符合字数要求的词
            valid_words = [
                word
                for word in word_dict.keys()
                if word_dict[word]["char_count"] == character_count
            ]
            if not valid_words:
                return "", "没有找到符合字数要求的词"

            words = random.sample(valid_words, 1)
            chinese_chars.extend(words)
            for word in words:
                pinyin = word_dict[word]["pinyin"]
                if capitalize:
                    pinyin = capitalize_pinyin(pinyin)
                pinyins.append(pinyin)

    # 构建提示信息：汉字(拼音)格式
    hints = []
    for char, pinyin in zip(chinese_chars, pinyins):
        hints.append(f"{char}({pinyin})")

    return "-".join(pinyins), "-".join(hints)  # 使用 - 分隔


if __name__ == "__main__":
    word_dict = load_word_list()
    if word_dict:
        # 复杂密码示例
        complex_pw, complex_hints = generate_complex_password(word_dict, min_length=12)
        print("复杂密码示例:", complex_pw)
        print("记忆提示:", complex_hints)

        # 基于最小长度的 passphrase
        passphrase_pw, passphrase_hints = generate_passphrase(word_dict, min_length=10)
        print("\nPassphrase 示例 (min_length=10):", passphrase_pw)
        print("记忆提示:", passphrase_hints)

        # 基于词数的 passphrase
        passphrase_pw_count, passphrase_hints_count = generate_passphrase(word_dict)
        print("\nPassphrase 示例 (word_count=3):", passphrase_pw_count)
        print("记忆提示:", passphrase_hints_count)
        strength = evaluate_password_strength(complex_pw)
        print("密码强度得分 (示例):", strength)
