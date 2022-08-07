import timeit
from statistics import fmean, pstdev, median


def center_text(text: str, width: int) -> str:
    delta = (width - len(text)) // 2
    return " " * delta + text


def num_from_format(raw_format: str) -> int:
    time_format = raw_format.lower()

    if time_format == "s":
        return 1
    elif time_format == "ms":
        return 1_000
    elif time_format == "us":
        return 1_000_000
    elif time_format == "ns":
        return 1_000_000_000
    else:
        raise ValueError("Invalid format")


def yes_no(val: bool) -> str:
    return "Yes" if val else "No"


class TestGroup:
    def __init__(
        self,
        name: str,
        tests: list[tuple[str, str]],
        globs: dict,
        time_format: str,
        precision: int,
        num: int,
        repeat_num: int,
        show_total: bool = True,
        show_mean: bool = True,
        show_std: bool = True,
    ):
        self.name = name
        self.tests = tests
        self.tests_number = len(tests)
        self.globs = globs
        self.results = []
        self.time_format = time_format
        self.precision = precision
        self.num = num
        self.repeat_num = repeat_num
        self.show_total = show_total
        self.show_mean = show_mean
        self.show_std = show_std
        self.data_format = self.calculate_data_order()

    def print_name(self):
        print("\n====||" + self.name.upper() + "||====")
        print(self.data_format + "\n")

    def test(self) -> None:
        self.print_name()
        for test_name, func in self.tests:
            self.results.append(self.test_pair(test_name, func))
        self.print_results()

    def test_pair(self, test_name: str, func: str) -> float:

        lst = timeit.repeat(
            func, globals=self.globs, number=self.num, repeat=self.repeat_num
        )
        self.print_single_test_results(test_name, lst)
        return fmean(lst)

    def print_results(self):
        print("-----------------")
        print(f"Group Mean: {self.adjust(fmean(self.results))}")
        print(f"Group Total: {self.adjust(sum(self.results) * self.repeat_num)}")
        print(f"Group Standard Deviation: {self.adjust(pstdev(self.results))}")
        print(f"Group Median: {self.adjust(median(sorted(self.results)))}")
        print("-----------------")

    def print_single_test_results(self, test_name: str, data: list[float]) -> None:
        final_string = "-) " + test_name + ": "
        if self.show_total:
            final_string += f"{self.adjust(sum(data))} | "
        if self.show_mean:
            final_string += f"{self.adjust(fmean(data))} | "
        if self.show_std:
            final_string += f"{self.adjust(pstdev(data))} | "
        print(final_string[:-3])

    def adjust(self, val: float) -> float:
        return round(val * num_from_format(self.time_format), self.precision)

    def calculate_data_order(self) -> str:
        final_str = "Current data order: "
        if self.show_total:
            final_str += "TOTAL, "
        if self.show_mean:
            final_str += "MEAN, "
        if self.show_std:
            final_str += "STD, "
        return final_str[:-2]


class TestSuite:
    def __init__(
        self,
        title: str,
        groups: list[tuple[str, list[tuple[str, str]]]],
        globs: dict,
        num: int = 1_000_000,
        repeat_num: int = 5,
        time_format="s",
        precision=5,
        show_total: bool = True,
        show_mean: bool = True,
        show_std: bool = True,
    ) -> None:
        self.title = title
        self.groups = [
            TestGroup(
                group[0],
                group[1],
                globs,
                time_format,
                precision,
                num,
                repeat_num,
                show_total,
                show_mean,
                show_std,
            )
            for group in groups
        ]
        self.num = num
        self.repeat_num = repeat_num
        self.results = []
        self.title_fac = int(len(self.title) * 1.5)
        self.time_format = time_format
        self.precision = precision
        self.show_total = show_total
        self.show_mean = show_mean
        self.show_std = show_std
        self.print_info()

    def run_suite(self) -> None:
        for group in self.groups:
            group.test()
            self.results.append(group.results)
        self.output_results()

    def print_info(self) -> None:
        self.print_title()
        self.print_settings()

    def output_results(self) -> None:
        self.repeat_char("_")

        accum = 0
        for g_results in self.results:
            accum += sum(g_results)
        print(
            f"\nTest suite total time: {self.adjust(accum * self.repeat_num)} "
            + self.time_format
        )

    def print_title(self) -> None:
        self.repeat_char("=")
        print(center_text(self.title.upper(), self.title_fac))
        self.repeat_char("=")

    def print_settings(self) -> None:
        print("Test suite settings:")
        strs = [
            f"Tests Number: {self.num}",
            f"Repeat Number: {self.repeat_num}",
            f"Time Format: '{self.time_format}'  (available 's', 'ms', 'us', 'ns')",
            f"Precision: {self.precision}",
            "Single test total: " + yes_no(self.show_total),
            "Single test mean: " + yes_no(self.show_mean),
            "Single test standard dev: " + yes_no(self.show_std),
        ]
        for st in strs:
            print("- " + st)
        self.repeat_char("=")

    def repeat_char(self, char: str, length: int = None) -> None:
        if length is None:
            print(char * self.title_fac)
        else:
            print(char * length)

    def adjust(self, val: float) -> float:
        return round(val * num_from_format(self.time_format), self.precision)
