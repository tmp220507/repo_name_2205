def simple_calc(input_list):
    if len(input_list) == 0:
        assert False
    if '+' in input_list or '-' in input_list:
        assert '*' not in input_list and '/' not in input_list
    if '*' in input_list or '/' in input_list:
        assert '+' not in input_list and '-' not in input_list

    result = input_list[0]
    for i in range(2, len(input_list), 2):
        op = input_list[i - 1]
        if op == '+':
            result = result + input_list[i]
        elif op == '-':
            result = result - input_list[i]
        elif op == '*':
            result = result * input_list[i]
        elif op == '/':
            result = result / input_list[i]
        else:
            assert False
    return result


def calc_without_bracket(input_list):
    assert '(' not in input_list and ')' not in input_list
    if len(input_list) == 0:
        assert False
    if len(input_list) == 1:
        return input_list[0]
    if input_list[0] == '-':
        input_list = [0] + input_list
    if len(input_list) == 3:
        return simple_calc(input_list)

    split = []
    for i in range(3, len(input_list), 2):
        if input_list[i] in '*/' and input_list[i - 2] in '+-':
            split.append(i - 1)
        if input_list[i] in '+-' and input_list[i - 2] in '*/':
            if len(split) == 0:
                split = [0]
            split.append(i - 1)
    if len(split) % 2 == 1:
        split.append(len(input_list) - 1)

    for i in range(len(split) - 2, -1, -2):
        start = split[i]
        stop = split[i + 1]
        tmp_result = simple_calc(input_list[start : stop + 1])
        input_list[start] = tmp_result
        del input_list[start + 1 : stop + 1]
    return simple_calc(input_list)


def calc_list(input_list):
    if '(' not in input_list:
        return calc_without_bracket(input_list)

    for i in range(len(input_list)):
        if input_list[i] == ')':
            stop = i
            break
    for i in range(stop - 1, -1, -1):
        if input_list[i] == '(':
            start = i
            break

    tmp_result = calc_list(input_list[start + 1 : stop])
    input_list[start] = tmp_result
    del input_list[start + 1 : stop + 1]
    return calc_list(input_list)


def calc(input_str):
    input_list = []
    num = 0
    clear = True
    for s in input_str:
        if s in '1234567890':
            num = num * 10 + int(s)
            clear = False
        elif s in '()+-*/':
            if not clear:
                input_list.append(num)
            input_list.append(s)
            num = 0
            clear = True
        else:
            assert False
    if not clear:
        input_list.append(num)
    return calc_list(input_list)


assert calc('-5+3') == -2
assert calc('-5*3') == -15
assert calc('1+30*5') == 151
assert calc('3*5+11') == 26
assert calc('(-5+3)') == -2
assert calc('(-5+3)*7') == -14
assert calc('7+(-5+3)') == 5
assert calc('(7+(-5+3))') == 5
assert calc('(-5+3)*(7+(-5+3))') == -10
assert calc('(-5+3)/(7+(-5+3))') == -0.4


