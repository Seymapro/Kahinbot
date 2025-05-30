# MIT License
#
# Copyright (c) 2024 Şeyma Yardım
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This module provides functions for calculating life path numbers from birthdates and generating reports based on data files.
"""

from datetime import datetime
from pathlib import Path

__author__ = "Seymapro"
__version__ = "1.0.0"


def birthdate_to_life_path(birthdate: datetime) -> tuple[int, int]:
    """
    Calculates the life path number from a given birthdate.

    Args:
        birthdate: The birthdate in datetime format.

    Returns:
        A tuple containing the initial sum and the final life path number.
    """

    first_sum = sum(map(lambda char: int(char), birthdate.strftime("%d%m%Y")))
    last_sum = sum(int(char) for char in str(first_sum)) if first_sum > 9 else first_sum

    return first_sum, last_sum


def life_path_to_content(life_path: tuple[int, int], data_directory: Path) -> str:
    """
    Retrieves the content associated with a specific life path from data files.

    Args:
        life_path: The life path number tuple (initial sum, final number).
        data_directory: The path to the directory containing the data files.

    Returns:
        The content (string) read from the corresponding data file.

    Raises:
        Exception: If an error occurs while reading the file.
    """

    file_path = data_directory / f"{life_path[0]}_{life_path[1]}.md"
    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            return f.read()
    except Exception as e:
        raise e


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Processes the given birthdate(s) according to the "
        "Dan Millman's `The Life You Were Born to Live` book.",
        epilog="Contact: @Seymapro",
    )

    # Define command-line arguments
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
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

    # Get birthdates from arguments or user input
    birthdates_raw = args.birthdates
    if not birthdates_raw:
        birthdates_raw.append(
            input("Please input a birthdate in the DAY.MONTH.YEAR format (e.g. 22.12.2002, 31.07.2002): ")
        )

    # Validate and parse birthdates
    birthdates: list[datetime] = []
    for birthdate_raw in birthdates_raw:
        try:
            birthdates.append(datetime.strptime(birthdate_raw, "%d.%m.%Y"))
        except ValueError as err:
            err.add_note(f"ERROR: Given birthdate ({birthdate_raw}) is not in the required format (DAY.MONTH.YEAR)")
            raise err

    DATA_DIRECTORY = args.data_directory
    REPORTS_DIRECTORY = args.reports_directory

    # Generate reports for each birthdate
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

        print(f"Report for the birthdate {birthdate_str} has been generated and written to file {report_path}")
