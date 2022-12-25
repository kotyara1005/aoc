TEST = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""


def parse_input():
    pass


def snafu_to_decimal(s):
    m = {"=": -2, "-": -1}
    result = 0

    for p, c in enumerate(reversed(s)):
        result += 5**p * int(m.get(c, c))

    # print(s, result)
    return result


def decimal_to_snafu(d):
    m = {3: "=", 4: "-"}
    result = []
    for i in range(32):
        reminder = d % 5
        if reminder < 3:
            val = str(reminder)
        else:
            val = m[reminder]
            d += 5 - reminder

        d = d // 5
        result.append(val)

        if d == 0:
            break

    return ''.join(reversed(result))


def part_one(s):
    return decimal_to_snafu(sum(snafu_to_decimal(line) for line in s.splitlines()))


if __name__ == '__main__':
    """
    1=-0-2     1747
     12111      906
      2=0=      198
        21       11
      2=01      201
       111       31
     20012     1257
       112       32
     1=-1=      353
      1-12      107
        12        7
        1=        3
       122       37
    """
    assert snafu_to_decimal("1=-0-2") == 1747
    assert snafu_to_decimal("12111") == 906
    assert snafu_to_decimal("2=0=") == 198
    assert snafu_to_decimal("21") == 11
    assert snafu_to_decimal("2=01") == 201
    assert snafu_to_decimal("111") == 31
    assert snafu_to_decimal("20012") == 1257
    assert snafu_to_decimal("112") == 32
    assert snafu_to_decimal("1=-1=") == 353
    assert snafu_to_decimal("1-12") == 107
    assert snafu_to_decimal("12") == 7
    assert snafu_to_decimal("1=") == 3
    assert snafu_to_decimal("122") == 37

    assert decimal_to_snafu(1747) == "1=-0-2"
    assert decimal_to_snafu(906) == "12111"
    assert decimal_to_snafu(198) == "2=0="
    assert decimal_to_snafu(11) == "21"
    assert decimal_to_snafu(201) == "2=01"
    assert decimal_to_snafu(31) == "111"
    assert decimal_to_snafu(1257) == "20012"
    assert decimal_to_snafu(32) == "112"
    assert decimal_to_snafu(353) == "1=-1="
    assert decimal_to_snafu(107) == "1-12"
    assert decimal_to_snafu(7) == "12"
    assert decimal_to_snafu(3) == "1="
    assert decimal_to_snafu(37) == "122"

    assert part_one(TEST) == "2=-1=0"

    print(part_one(open("input").read()))
    print("DONE")
