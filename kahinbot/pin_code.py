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


def downgrade_number(number: int) -> int:
    """
    Reduces a number to a single digit by repeatedly summing its digits.

    This function takes an integer `number` and applies the digit-summing
    process until the number is less than 10. For example, if the input is
    38, it will be reduced as follows: 3 + 8 = 11, and then 1 + 1 = 2.

    Args:
        number (int): The number to be reduced to a single digit.

    Returns:
        int: A single-digit integer derived from the input number.

    Example:
        >>> downgrade_number(38)
        2
    """

    while number >= 10:
        number = sum(map(int, str(number)))

    return number


def get_pin_code(birthdate: datetime) -> list[int]:
    """
    Generates a pin code based on the given birthdate.

    This function calculates a pin code using the day, month, and year
    components of a provided `birthdate`. It also incorporates additional
    calculations using the derived single-digit values to generate
    a complete pin code consisting of eight digits.

    Args:
        birthdate (datetime): A datetime object representing the birthdate
                              from which the pin code will be generated.

    Returns:
        list[int]: A list of integers representing the pin code.

    Example:
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
    """
    Retrieves content based on the pin code from specified markdown files.

    This function takes a list of pin code integers and reads content
    from markdown files named according to the pin code digits. The files
    are expected to be located in the specified `content_dir`.

    Args:
        pin_code (list[int]): A list of integers representing the pin code.
        content_dir (Path): A Path object representing the directory
                            containing the markdown files.

    Returns:
        list[str]: A list of strings containing the content from the
                    corresponding markdown files.

    Raises:
        FileNotFoundError: If a specified markdown file does not exist.

    Example:
        >>> pin_code_to_contents([4, 3, 4, 2, 6, 7, 7, 5, 2], Path('./data/forbes/MDs/'))
        ['Content from 1_4.md', 'Content from 2_3.md', ...]
    """

    contents: list[str] = []

    for i, pin in enumerate(pin_code, start=1):
        with open(content_dir / f"{i}_{pin}.md", "r", encoding="UTF-8") as f:
            contents.append(f.read().strip())

    return contents


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Processes the given birthdate(s) according to the "
        "Douglas Forbes' `Human Pin Code` book.",
        epilog="Contact: @Seymapro",
    )

    # Define command-line arguments
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
        default="./data/forbes/MDs/",
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
            input(
                "Please input a birthdate in the DAY.MONTH.YEAR format "
                "(e.g. 22.12.2002, 31.07.2002): "
            )
        )

    # Validate and parse birthdates
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

    # Generate reports for each birthdate
    for birthdate in birthdates:
        pin_code = get_pin_code(birthdate)

        print(
            f"Pin code for birthdate {birthdate.strftime('%d.%m.%Y')} "
            f"is {''.join(map(str, pin_code))}"
        )

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

        print(
            f"Report for the birthdate {birthdate_str} has been generated "
            f"and written to file {report_path}"
        )
