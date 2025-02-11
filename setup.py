import os
import sys
from codecs import open
from setuptools import setup, find_packages

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 11)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
This version of KahinBot requires at least Python {}.{}, but
you're trying to install it on Python {}.{}. 

To resolve this, consider upgrading to a supported Python version.
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()

requires = [
    'python-telegram-bot>=13.0',
        'python-dotenv>=0.19.0',   
]

# TODO add test requirements

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "kahinbot"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

setup(
    name=about["__kahinbot__"],
    version=about["__0.1__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__seymapro__"],
    author_email=about["__seymayardim@ogr.iu.edu.tr__"],
    packages=find_packages(include=["kahinbot", "kahinbot.*"]),
    package_data={"": ["LICENSE"]},
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=requires,
    license=about["__LICENSE__"],
    zip_safe=False,
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.11', 
    ],
    },
    project_urls={
        "Documentation": "https://github.com/Seymapro/Kahinbot/",
    },
)
