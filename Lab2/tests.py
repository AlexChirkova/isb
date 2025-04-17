import math

from scipy.special import gammainc

import constants as c
from Random import random_sequence as rs


def frequency_bitwise_test(seq: str) -> float:
    """
    Frequency bitwise test
    :param seq: bitwise sequence for test
    :return: the probability that the value is close to the benchmark
    """

    n = len(seq)
    s = abs(1 / (math.sqrt(n)) * (seq.count("1") - seq.count("0")))
    return math.erfc(s / math.sqrt(2))


def consecutive_bits_test(seq: str) -> float:
    """
    A test for identical consecutive bits
    :param seq: bitwise sequence for test
    :return: the probability that the value is close to the benchmark
    """
    n = len(seq)
    p = seq.count("1") / n
    if abs(p - 0.5) >= 2 / math.sqrt(n):
        return 0

    v = sum(seq[i] != seq[i + 1] for i in range(n - 1))
    return math.erfc(
        abs(v - 2 * n * p * (1 - p)) / (2 * math.sqrt(2 * n) * p * (1 - p))
    )


def longest_seq_of_units_test(seq: str) -> float:
    """
    Test for the longest sequence of units in the block
    :param seq: bitwise sequence for test
    :return: the probability that the value is close to the benchmark
    """
    n = len(seq)
    v = [0, 0, 0, 0]
    for i in range(0, n, 8):
        max_len = 0
        current_len = 0
        for j in seq[i : i + 8]:
            if j == "1":
                current_len += 1
                max_len = max(max_len, current_len)
            else:
                current_len = 0

        match max_len:
            case 0:
                v[0] += 1
            case 1:
                v[0] += 1
            case 2:
                v[1] += 1
            case 3:
                v[2] += 1
            case _:
                v[3] += 1

    he2 = sum(((v[i] - 16 * c.PI[i]) ** 2) / 16 * c.PI[i] for i in range(4))
    return gammainc(3 / 2, he2 / 2)


def save_res_to_file(fr: float, cb: float, ls: float, path: str) -> None:
    with open(path, "a") as file:
        print(f"Pvalue of Frequency bitwise test: {fr}", file=file)
        print(f"Pvalue of Test for identical consecutive bits: {cb}", file=file)
        print(
            f"Pvalue of Test for the longest sequence of units in a block: {ls}",
            file=file,
        )
        print("", file=file)


def main():
    fr_cpp = frequency_bitwise_test(rs.CPP)
    cb_cpp = consecutive_bits_test(rs.CPP)
    ls_cpp = longest_seq_of_units_test(rs.CPP)
    save_res_to_file(fr_cpp, cb_cpp, ls_cpp, c.INPUT)

    fr_java = frequency_bitwise_test(rs.JAVA)
    cb_java = consecutive_bits_test(rs.JAVA)
    ls_java = longest_seq_of_units_test(rs.JAVA)
    save_res_to_file(fr_java, cb_java, ls_java, c.INPUT)

    fr_py = frequency_bitwise_test(rs.PY)
    cb_py = consecutive_bits_test(rs.PY)
    ls_py = longest_seq_of_units_test(rs.PY)
    save_res_to_file(fr_py, cb_py, ls_py, c.INPUT)


if __name__ == "__main__":
    main()
