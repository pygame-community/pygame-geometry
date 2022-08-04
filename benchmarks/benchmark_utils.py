import timeit
from statistics import fmean
from typing import Sequence


def test(test_name: str, func: str, globs: dict, num: int, mode: str) -> float:
    value = 0
    if mode == "mean":
        value = fmean(timeit.repeat(func, globals=globs, number=num))
    elif mode == "cumulative":
        value = timeit.timeit(func, globals=globs, number=num)
    else:
        raise NotImplementedError("Incorrect test mode")
    print("-) " + test_name + f": {round(value, 8)} s")
    return value


def test_group(
    group_name: str,
    sequence: Sequence[str],
    globs: dict,
    tests_names: Sequence[str] = None,
    num: int = 10_000_000,
    include_tot: bool = False,
    include_mean: bool = True,
    test_mode: str = "mean",
) -> float:
    print("\n====||" + group_name.upper() + "||====")

    test_data = [
        test(
            tests_names[i] if tests_names else str(i + 1),
            test_obj,
            globs,
            num,
            test_mode,
        )
        for i, test_obj in enumerate(sequence)
    ]

    print("______________")
    if include_tot:
        print(f"-) Total time: {round(sum(test_data), 8)}")
        return sum(test_data)

    if include_mean:
        print(f"-) Mean time: {round(fmean(test_data), 8)}")
        return fmean(test_data)

    return fmean(test_data)
