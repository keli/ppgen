# cli.py - 命令行接口
import click
import json
from .core import (
    load_word_list,
    generate_complex_password,
    generate_passphrase,
)
from .evaluator import evaluate_password_strength


@click.command()
@click.option(
    "--password",
    "-p",
    is_flag=True,
    help="生成复杂密码而不是密码短语.",
)
@click.option("--count", "-c", default=5, type=int, help="生成密码的数量.")
@click.option(
    "--min_length",
    "-l",
    default=12,
    type=int,
    help="密码最小长度 (密码短语模式下如果指定了word_count则忽略此参数).",
)
@click.option(
    "--word_count",
    "-w",
    default=4,
    type=int,
    help="密码短语模式下使用的拼音词数量 (可选,默认4个词).",
)
@click.option(
    "--output",
    "-o",
    default="text",
    type=click.Choice(["text", "json"]),
    help="输出格式: text 或 json.",
)
def ppgen(password, count, min_length, word_count, output):
    """
    ppgen: 一个基于常用汉语词表的密码生成工具。
    """
    word_dict = load_word_list()
    if not word_dict:
        return

    passwords = []
    for _ in range(count):
        if password:
            password_str, hints = generate_complex_password(word_dict, min_length)
            strength_score = evaluate_password_strength(password_str)
            passwords.append(
                {"password": password_str, "strength": strength_score, "hints": hints}
            )
        else:
            password_str, hints = generate_passphrase(word_dict, min_length, word_count)
            strength_score = evaluate_password_strength(password_str)
            passwords.append(
                {"password": password_str, "strength": strength_score, "hints": hints}
            )

    if output == "json":
        click.echo(json.dumps(passwords, indent=2, ensure_ascii=False))
    else:  # text 输出
        for pw_data in passwords:
            click.echo(f"密码: {pw_data['password']}  强度: {pw_data['strength']}")
            if "hints" in pw_data:
                click.echo(f"记忆提示: {pw_data['hints']}")
            click.echo("---")


if __name__ == "__main__":
    ppgen()
