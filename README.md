# EnableSysadminRSSReader

![](mazinger-z.png)

This is a simple script to show the headlines from the RedHat Enable sysadmin website RSS feed.

![Articles for the day](https://raw.githubusercontent.com/josevnz/EnableSysadminRssReader/main/rssenablesysadminreader.png)

## Author

Jose Vicente Nunez (kodegeek.com@protonmail.com)

# Set your virtual environment

```shell
python3 -m venv ~/virtualenv/EnableSysadminRssReader/
. ~/virtualenv/EnableSysadminRssReader/bin/activate
python -m pip install --upgrade pip
```

Get the sources:

```shell
git clone git@github.com:josevnz/EnableSysadminRssReader.git
cd EnableSysadminRssReader
```

Rest of the commands explained on this file assume you have the virtual environment enabled.

# Running in editable mode

```shell
pip install --editable .
```

# Running unit tests

```shell
(EnableSysadminRssReader) [josevnz@dmaf5 EnableSysadminRssReader]$ python -m unittest tests/test_reader.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.125s

OK
```

# Building and installing the package

Using build:

```shell
python -m build 
pip install dist/EnableSysadminRssReader-*-py3-none-any.whl
```

If build is not installed (you will get a deprecation warning but it will work):

```shell
python setup.py bdist_wheel
pip install dist/EnableSysadminRssReader-*-py3-none-any.whl
```

## Don't miss the tutorial that comes with the code

[The Tutorial](Scanning%20your%20Python%20code%20for%20third%20party%20vulnerabilities.md)
