# MIT License

# Copyright (c) 2024 Şeyma Yardım

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from pathlib import Path

__author__ = "Seymapro"
__version__ = "1.0.0"


def birthdate_to_life_path(birthdate: datetime) -> tuple[int, int]:
    first_sum = sum(map(lambda char: int(char), birthdate.strftime("%d%m%Y")))
    last_sum = sum(int(char) for char in str(first_sum)) if first_sum > 9 else first_sum

    return first_sum, last_sum


def life_path_to_content(life_path: tuple[int, int], data_directory: Path) -> str:
    file_path = data_directory / f"{life_path[0]}_{life_path[1]}.md"
    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            return f.read()
    except Exception as e:
        raise e


if __name__ == "__main__":
    import argparse

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Processes the given birthdate(s) according to the "
        "Dan Millman's `The Life You Were Born to Live` book.",
        epilog="Contact: @Seymapro",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-b",
        "--birthdate",
        "--birthdates",
        nargs="+",
        default=[],
        help="birthdates you want to process",
        dest="birthdates",
    )
    parser.add_argument(
        "-d",
        "--data-dir",
        "--data-directory",
        default="./data/",
        type=Path,
        help="path to the data directory",
        dest="data_directory",
    )
    parser.add_argument(
        "-r",
        "--reports-dir",
        "--reports-directory",
        default="./reports/",
        type=Path,
        help="path to the reports directory",
        dest="reports_directory",
    )

    args = parser.parse_args()

    birthdates_raw = args.birthdates
    if not birthdates_raw:
        birthdates_raw.append(
            input(
                "Please input a birthdate in the DAY.MONTH.YEAR format "
                "(e.g. 22.12.2002, 31.07.2002): "
            )
        )

    birthdates: list[datetime] = []
    for birthdate_raw in birthdates_raw:
        try:
            birthdates.append(datetime.strptime(birthdate_raw, "%d.%m.%Y"))
        except ValueError as err:
            err.add_note(
                f"ERROR: Given birthdate ({birthdate_raw}) is not in the required "
                "format (DAY.MONTH.YEAR)"
            )
            raise err

    DATA_DIRECTORY = args.data_directory
    REPORTS_DIRECTORY = args.reports_directory

    for birthdate in birthdates:
        life_path = birthdate_to_life_path(birthdate)
        content = life_path_to_content(life_path, DATA_DIRECTORY)

        birthdate_str = birthdate.strftime("%Y.%m.%d")
        report_path = REPORTS_DIRECTORY / f"{birthdate_str}.md"
        with open(
            report_path,
            "w",
            encoding="UTF-8",
        ) as f:
            f.write(content)

        print(
            f"Report for the birthdate {birthdate_str} has been generated "
            f"and written to file {report_path}"
        )
