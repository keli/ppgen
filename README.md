# ppgen

一个基于汉语拼音的密码/密码短语生成器。它可以生成易记的强密码，同时提供中文记忆提示。

## 特性

- 支持两种密码生成模式：
  - 复杂密码：使用拼音组合，并添加特殊字符和数字
  - 密码短语：使用多个拼音词组，通过连字符连接
- 为每个生成的密码提供中文和拼音的记忆提示
- 支持密码强度评估
- 支持文本和JSON输出格式
- 可配置参数：最小长度、词数量、生成数量等

## 安装

```bash
pip install ppgen
```

## 使用方法

### 基本用法

生成密码短语（默认模式）：
```bash
ppgen
```

生成复杂密码：
```bash
ppgen --password
```

### 常用选项

- `-p, --password`: 生成复杂密码而不是密码短语
- `-c, --count`: 生成密码的数量（默认：5）
- `-l, --min_length`: 密码最小长度（默认：12）
- `-w, --word_count`: 密码短语模式下使用的拼音词数量（默认：4）
- `-o, --output`: 输出格式，可选 text 或 json（默认：text）

### 示例

生成3个密码短语：
```bash
ppgen -c 3
```

生成最小长度为15的复杂密码：
```bash
ppgen -p -l 15
```

使用5个词生成密码短语：
```bash
ppgen -w 5
```

JSON格式输出：
```bash
ppgen -o json
```

## 输出示例

文本格式输出：
```
密码: zhongwen-yuyan-jisuanji-ruanjian
强度: 4
记忆提示: 中文(zhongwen)-语言(yuyan)-计算机(jisuanji)-软件(ruanjian)
---
```

JSON格式输出：
```json
[
  {
    "password": "zhongwen-yuyan-jisuanji-ruanjian",
    "strength": 4,
    "hints": "中文(zhongwen)-语言(yuyan)-计算机(jisuanji)-软件(ruanjian)"
  }
]
```

