# sundial-calculator

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

A Python script to aid in calculating hour angles and offsets for building a horizontal sundial.  Simply feed the script your latitude and longitude and allow it to do the rest, including both an informational data sheet and a template image file.

Note that this project is *only* designed for the creation of horizontal sundials; other types of sundials may or may not produce accurate calculations.

## Getting Started <a name = "getting_started"></a>

Clone the repo:

```bash
git clone https://github.com/notoriouslogank/sundial-calculator.git
```

Inside the directory, install the requirements.txt (virtual environment recommended):

```bash
cd sundial-calculator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage <a name = "usage"></a>

Simply run the main function and input latitude and longitude data when prompted:

```bash
python3 main.py
```
