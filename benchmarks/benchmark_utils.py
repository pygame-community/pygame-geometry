import timeit
from statistics import fmean, pstdev, median

from tabulate import tabulate


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

    def print_name(self):

        print(self.name.upper())
        print("=" * 50)

    def test(self) -> None:
        self.print_name()
        table = [self.get_field_names()]

        for test_name, func in self.tests:
            self.results.append(self.test_pair(test_name, func, table))

        print(
            tabulate(
                table,
                headers="firstrow",
                tablefmt="github",
                numalign="center",
                stralign="center",
            )
        )
        self.print_results()
        print("\n\n")

    def test_pair(self, test_name: str, func: str, table: list) -> float:
        # ensure that the objects utilized in the tests are not modified by the tests
        item = func.split(".")[0]
        saved_item = None
        if item in self.globs.keys() and len(item) == 2:
            saved_item = self.globs[item]
            self.globs[item] = saved_item.copy()

        lst = timeit.repeat(
            func, globals=self.globs, number=self.num, repeat=self.repeat_num
        )
        if saved_item:
            self.globs[item] = saved_item
        table.append(self.get_row(test_name, lst))
        return fmean(lst)

    def print_results(self):
        print("\n" + "-" * 50)
        print(f"Group Mean: {self.adjust(fmean(self.results))}")
        print(f"Group Total: {self.adjust(sum(self.results) * self.repeat_num)}")
        print(f"Group Standard Deviation: {self.adjust(pstdev(self.results))}")
        print(f"Group Median: {self.adjust(median(sorted(self.results)))}")

    def adjust(self, val: float) -> float:
        return round(val * num_from_format(self.time_format), self.precision)

    def get_field_names(self) -> list[str]:
        field_names = ["Name"]
        if self.show_total:
            field_names.append("Total")
        if self.show_mean:
            field_names.append("Mean")
        if self.show_std:
            field_names.append("Std Dev")
        return field_names

    def get_row(self, test_name: str, lst: list[float]) -> list[str]:
        row = [test_name]
        if self.show_total:
            row.append(self.adjust(sum(lst)))
        if self.show_mean:
            row.append(self.adjust(fmean(lst)))
        if self.show_std:
            row.append(self.adjust(pstdev(lst)))
        return row


class TestSuite:
    def __init__(
        self,
        title: str,
        groups: list[tuple[str, list[tuple[str, str]]]],
        globs: dict,
        num: int = 1_000_000,
        repeat_num: int = 10,
        time_format="ms",
        precision=2,
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
            self.calculate_data_order(),
        ]
        for st in strs:
            print("- " + st)
        print()

    def calculate_data_order(self) -> str:
        final_str = "Current data order: "
        if self.show_total:
            final_str += "TOTAL, "
        if self.show_mean:
            final_str += "MEAN, "
        if self.show_std:
            final_str += "STD, "
        return final_str[:-2]

    def repeat_char(self, char: str, length: int = None) -> None:
        if length is None:
            print(char * self.title_fac)
        else:
            print(char * length)

    def adjust(self, val: float) -> float:
        return round(val * num_from_format(self.time_format), self.precision)
