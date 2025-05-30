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

"""Life Path Number Calculator based on Dan Millman's Teachings.

This module provides functionality to calculate and interpret Life Path Numbers
based on numerology principles from Dan Millman's 'The Life You Were Born to Live'.
It processes birthdates to compute numerological values and generates detailed
reports with interpretations.

Key Features:
    - Calculates Life Path Numbers from birthdates
    - Generates personalized reports based on numerological calculations
    - Supports batch processing of multiple birthdates
    - Handles file I/O for data and report generation

Example:
    >>> from datetime import datetime
    >>> from pathlib import Path
    >>> birthdate = datetime(1990, 1, 1)
    >>> life_path = birthdate_to_life_path(birthdate)
    >>> content = life_path_to_content(life_path, Path("./data"))
"""

from datetime import datetime
from pathlib import Path

__author__ = "Seymapro"
__version__ = "1.0.1"


def birthdate_to_life_path(birthdate: datetime) -> tuple[int, int]:
    """Calculate the life path number based on numerology principles.

    Takes a birthdate and computes both the initial sum of all digits and the final
    life path number according to numerological reduction. For example, if the birthdate
    is 22.12.2002, it first sums 2+2+1+2+2+0+0+2=11, then reduces to 1+1=2.

    Args:
        birthdate (datetime): A datetime object representing the birth date.
            The date should be a valid Gregorian calendar date.

    Returns:
        tuple[int, int]: A tuple containing:
            - first number (int): The initial sum of all digits in the birthdate
            - second number (int): The final life path number (reduced to a single digit
              if the first sum is greater than 9)

    Examples:
        >>> from datetime import datetime
        >>> birthdate = datetime(2002, 12, 22)
        >>> birthdate_to_life_path(birthdate)
        (11, 2)
    """
    first_sum = sum(map(lambda char: int(char), birthdate.strftime("%d%m%Y")))
    last_sum = sum(int(char) for char in str(first_sum)) if first_sum > 9 else first_sum

    return first_sum, last_sum


def life_path_to_content(life_path: tuple[int, int], data_directory: Path) -> str:
    """Retrieves content associated with a life path number from corresponding data file.

    Reads and returns the content from a markdown file that corresponds to the given
    life path number. The file name is expected to be in the format "{first_sum}_{final_number}.md".

    Args:
        life_path (tuple[int, int]): A tuple containing two integers:
            - first element: The initial sum of the birthdate digits
            - second element: The reduced (final) life path number
        data_directory (Path): Directory path where the life path data files are stored.
            Must contain markdown files named in the format "{first_sum}_{final_number}.md"

    Returns:
        str: The complete content of the corresponding life path data file.

    Raises:
        FileNotFoundError: If the data file for the given life path number doesn't exist.
        PermissionError: If the program lacks permission to read the data file.
        UnicodeDecodeError: If the file content cannot be decoded as UTF-8.

    Examples:
        >>> from pathlib import Path
        >>> data_dir = Path("./data")
        >>> content = life_path_to_content((11, 2), data_dir)
        >>> print(content[:50])  # Print first 50 characters
        'Description for life path 11/2: Creative expression...'
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
