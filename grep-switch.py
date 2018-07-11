import sys


def grep(pattern, filename):
    if len(pattern) < 1:
        print("The length of pattern is zero!")
        return

    # 定义patter的两种状态:
    # enclosing_state: 被单引号括起来的状态
    # escape_state: 转义状态
    enclosing_state = False
    escape_state = False

    pattern_valid = ""

    for i in range(len(pattern)):
        # 如果pattern以引号开始,那么它必然要以引号结束
        if i is 0 and pattern[i] is "\'":
            enclosing_state = True

        if i is len(pattern) - 1:
            # pattern以引号开始,但最后一个字符被转义或非引号,则报错
            if enclosing_state is True:
                if escape_state is True or pattern[i] is not "\'":
                    print("Syntax error: pattern enclosed should end with '")
                    return
            # pattern不以引号开始,但最后一位为引号,报错
            else:
                if escape_state is False and pattern[i] is "\'":
                    print("Syntax error: pattern enclosed should begin with '")
                    return

        # 当前字符为转义字符,那么就会有2种情况
        # 1 - 当前为转义状态,那么转义字符被转义
        # 2 - 不为转义状态,那么将状态设置为转义状态
        if pattern[i] is "\\":
            if escape_state is True:
                pattern_valid += pattern[i]
                escape_state = False
            else:
                escape_state = True

        # 当前字符为单引号 - 两种情况
        # 1 - 转义状态,单引号有效
        # 2 - 非转义状态,且不为pattern的开头或结尾处,句法错误
        if pattern[i] is '\'' and i is not 0:
            if escape_state is True:
                pattern_valid += pattern[i]
                escape_state = False

            elif escape_state is False and i is not len(pattern) - 1:
                print('Syntax error: the pattern used single quote illegally')
                return

        # 当前字符为空格
        # 被括状态 - 空格有效
        # 否则 - 句法错误
        if pattern[i] is ' ':
            if enclosing_state is True:
                pattern_valid += pattern[i]
            else:
                print('Syntax error: the pattern contains space without being quoted!')
                return

        # 转义符后的普通字符
        # 转义状态 - 该字符被跳过
        # 非转义状态 - 字符有效
        if pattern[i] not in ['\'', ' ', '\\']:
            if escape_state is True:
                escape_state = False
            else:
                pattern_valid += pattern[i]

    # 无有效字符
    if len(pattern_valid) < 1:
        print("Syntax error: no valid chars!")
        return

    line_length_constraint = True
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.find(pattern_valid) >= 0:
                print(line)
            if len(line) >= len(pattern_valid):
                line_length_constraint = False

    if line_length_constraint:
        print("Funny Error: Pattern is longer than all of lines in the file!")


if __name__ == "__main__":
    p = sys.argv[1]
    f = sys.argv[2]
    grep(p, f)

