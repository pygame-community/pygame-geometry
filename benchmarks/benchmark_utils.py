import timeit
from statistics import fmean

from itertools import accumulate


def center_text(text: str, width: int) -> str:
    delta = (width - len(text)) // 2
    return " " * delta + text


class TestGroup:
    def __init__(self, name: str, tests: list[tuple[str, str]], globs: dict):
        self.name = name
        self.tests = tests
        self.tests_number = len(tests)
        self.mode = "mean"
        self.globs = globs
        self.results = []

    def print_name(self):
        print("\n====||" + self.name.upper() + "||====")

    def test(self, num: int, repeat_num: int) -> None:
        self.print_name()
        for test_name, func in self.tests:
            self.results.append(self.test_pair(test_name, func, num, repeat_num))
        print("-----------------")
        print(f"Group Mean: {round(fmean(self.results), 8)}")

    def test_pair(self, test_name: str, func: str, num: int, repeat_num: int) -> float:
        lst = []
        if self.mode == "mean":
            lst = timeit.repeat(func, globals=self.globs, number=num, repeat=repeat_num)
        else:
            raise NotImplementedError("Incorrect test mode")
        print("-) " + test_name + f": {round(fmean(lst), 8)} s")
        return fmean(lst)

        # def test_group(
        #     self,
        #     group_name: str,
        #     include_tot: bool = False,
        #     include_mean: bool = True,
        #     test_mode: str = "mean",
        # ) -> float:
        #     print("\n====||" + group_name.upper() + "||====")
        #
        #     test_data = [
        #         self.test(
        #             tests_names[i] if tests_names else str(i + 1),
        #             test_obj,
        #             test_mode,
        #         )
        #         for i, test_obj in enumerate(sequence)
        #     ]
        #
        #     print("______________")
        #     if include_tot:
        #         print(f"-) Total time: {round(sum(test_data), 8)}")
        #         return sum(test_data)
        #
        #     if include_mean:
        #         print(f"-) Mean time: {round(fmean(test_data), 8)}")
        #         return fmean(test_data)
        #
        #     return fmean(test_data)


class TestSuite:
    def __init__(
        self,
        title: str,
        groups: list[tuple[str, list[tuple[str, str]]]],
        globs: dict,
        num: int = 1_000_000,
        repeat_num: int = 5,
        include_tot: bool = True,
        include_mean: bool = False,
    ):
        self.title = title
        self.groups = [TestGroup(group[0], group[1], globs) for group in groups]
        self.num = num
        self.repeat_num = repeat_num
        self.results = []
        self.include_tot = include_tot
        self.include_mean = include_mean
        self.title_fac = int(len(self.title) * 1.5)

    def run_suite(self) -> None:
        self.print_info()
        for group in self.groups:
            group.test(self.num, self.repeat_num)
            self.results.append(group.results)

        self.output_results()

    def print_info(self) -> None:
        self.print_title()
        self.print_settings()

    def output_results(self) -> None:
        self.repeat_char("_")
        if self.include_tot:
            accum = 0
            for g_results in self.results:
                accum += sum(g_results)
            print(f"\nTest suite total time: {accum * self.repeat_num}")

    def print_title(self) -> None:
        self.repeat_char("=")
        print(center_text(self.title.upper(), self.title_fac))
        self.repeat_char("=")

    def print_settings(self) -> None:
        print(f"Number of tests: {self.num} | Repeat: {self.repeat_num}")
        self.repeat_char("=")

    def repeat_char(self, char: str):
        print("=" * self.title_fac)
