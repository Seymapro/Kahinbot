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

"""Generates and processes Human Pin Codes based on birthdates using numerology.

This module implements the Human Pin Code system as described in Douglas Forbes' book,
generating a unique 9-digit code from a person's birthdate. Each digit is calculated
using numerological principles and corresponds to specific personality traits or life
aspects.

Main Functions:
    downgrade_number: Reduces numbers to single digits through digital root calculation
    get_pin_code: Generates a 9-digit pin code from a birthdate
    pin_code_to_contents: Maps pin code digits to corresponding reading contents

The module can be used both as a library and as a command-line tool. When run as
a script, it processes birthdates and generates detailed reports with readings for
each pin code digit.

Example:
    >>> from datetime import datetime
    >>> from kahinbot.pin_code import get_pin_code
    >>> pin = get_pin_code(datetime(2002, 12, 22))
    >>> print(pin)  # Returns [4, 3, 4, 2, 6, 7, 7, 5, 2]
"""

from datetime import datetime
from pathlib import Path

__author__ = "Seymapro"
__version__ = "1.0.1"


def downgrade_number(number: int) -> int:
    """Reduces a number to a single digit through iterative digit summation.

    Performs repeated summation of individual digits in a number until a single
    digit is obtained. This process is also known as digital root calculation.

    Args:
        number: An integer to be reduced to a single digit.

    Returns:
        The digital root (single digit) obtained after repeated digit summation.

    Examples:
        >>> downgrade_number(38)  # 3 + 8 = 11, then 1 + 1 = 2
        2
        >>> downgrade_number(123)  # 1 + 2 + 3 = 6
        6
        >>> downgrade_number(999)  # 9 + 9 + 9 = 27, then 2 + 7 = 9
        9

    Note:
        - The function will return the input number if it's already a single digit
        - For negative numbers, the function processes their absolute value
    """

    while number >= 10:
        number = sum(map(int, str(number)))

    return number


def get_pin_code(birthdate: datetime) -> list[int]:
    """Generates a 9-digit pin code based on birthdate using numerological principles.

    Calculates a sequence of digits by applying the following rules:
    1. First digit: Digital root of birth day
    2. Second digit: Digital root of birth month
    3. Third digit: Digital root of birth year
    4. Fourth digit: Digital root of (1st + 2nd + 3rd) digits
    5. Fifth digit: Digital root of (1st + 4th) digits
    6. Sixth digit: Digital root of (1st + 2nd) digits
    7. Seventh digit: Digital root of (2nd + 3rd) digits
    8. Eighth digit: Digital root of (6th + 7th) digits
    9. Ninth digit: Digital root of sum of all previous digits

    Args:
        birthdate: A datetime object containing the target birth date.
            Expected to be a valid date with year, month and day components.

    Returns:
        A list of 9 integers (0-9), representing the calculated pin code sequence.
            Each digit is derived through numerological reduction of date components.

    Example:
        >>> from datetime import datetime
        >>> get_pin_code(datetime(2002, 12, 22))
        [4, 3, 4, 2, 6, 7, 7, 5, 2]
    """

    day = birthdate.day
    month = birthdate.month
    year = birthdate.year

    pin_code: list[int] = []

    first = downgrade_number(day)
    pin_code.append(first)

    second = downgrade_number(month)
    pin_code.append(second)

    third = downgrade_number(year)
    pin_code.append(third)

    fourth = downgrade_number(first + second + third)
    pin_code.append(fourth)

    fifth = downgrade_number(first + fourth)
    pin_code.append(fifth)

    sixth = downgrade_number(first + second)
    pin_code.append(sixth)

    seventh = downgrade_number(second + third)
    pin_code.append(seventh)

    eighth = downgrade_number(sixth + seventh)
    pin_code.append(eighth)

    sense_of_life = downgrade_number(sum(pin_code))
    pin_code.append(sense_of_life)

    return pin_code


def pin_code_to_contents(pin_code: list[int], content_dir: Path) -> list[str]:
    """Maps pin code digits to content from numbered markdown files.

    Each digit in the pin code corresponds to a markdown file named in the format
    "position_digit.md" (e.g., "1_4.md" for first position with digit 4). The
    function reads these files from the specified directory and returns their
    contents as a list.

    Args:
        pin_code: List of 9 integers (0-9) representing the numerological pin code.
            Each digit corresponds to a specific aspect of the reading.
        content_dir: Directory path containing the markdown files with readings.
            Files should be named in the format "position_digit.md".

    Returns:
        List of strings where each string contains the content of a markdown file
        corresponding to the pin code digits in order.

    Raises:
        FileNotFoundError: If any required markdown file is missing from content_dir.
        TypeError: If pin_code is not a list of integers or content_dir is not a Path.

    Example:
        >>> pin = [4, 3, 4, 2, 6, 7, 7, 5, 2]
        >>> contents = pin_code_to_contents(pin, Path("data/readings"))
        >>> len(contents)  # Returns 9 strings, one for each pin digit
        9
    """

    contents: list[str] = []

    for i, pin in enumerate(pin_code, start=1):
        with open(content_dir / f"{i}_{pin}.md", "r", encoding="UTF-8") as f:
            contents.append(f.read().strip())

    return contents


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Processes the given birthdate(s) according to the Douglas Forbes' `Human Pin Code` book.",
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
        default="./data/forbes/tr/MDs/",
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
        pin_code = get_pin_code(birthdate)

        print(f"Pin code for birthdate {birthdate.strftime('%d.%m.%Y')} is {''.join(map(str, pin_code))}")

        contents = pin_code_to_contents(pin_code, DATA_DIRECTORY)

        birthdate_str = birthdate.strftime("%Y.%m.%d")
        report_path = REPORTS_DIRECTORY / f"{birthdate_str}.md"
        with open(
            report_path,
            "w",
            encoding="UTF-8",
        ) as f:
            for content in contents:
                f.write(content + "\n\n")

        print(f"Report for the birthdate {birthdate_str} has been generated and written to file {report_path}")
