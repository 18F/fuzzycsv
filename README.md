# reheader

[![PyPI Status](https://img.shields.io/pypi/v/reheader.svg)](https://pypi.python.org/pypi/reheader)
[![Build Status](https://img.shields.io/travis/18F/reheader.svg?branch=master)](https://travis-ci.org/18F/reheader)
[![Coverage Status](https://coveralls.io/repos/github/18F/reheader.svg?branch=master)](https://coveralls.io/github/18f/reheader?branch=master)
[![Code Climate](https://codeclimate.com/github/18F/reheader.svg)](https://codeclimate.com/github/18F/reheader)

Forces data's headers to match an expected template, using fuzzy column
name matching and/or regular expressions to recognize columns.

Designed for import of CSVs from uncontrolled sources.

* Documentation: https://reheader.readthedocs.io.


## Features

* Process lists of dictionaries or lists of lists, including those
  generated from CSVs

## Using

### Fuzzily matching header names

If `headers` is a `list`, reheader uses a fuzzy match between desired and
actual header values to identify columns.

    $ head -2 data.csv
    name,mail,profession,zip
    Nellie Newsock,nellie@sox.com,Adventuress,45309
    $ python
    >>> import csv
    >>> from reheader.reheader import reheadered
    >>> infile = open('data.csv')
    >>> data_source = csv.DictReader(infile)
    >>> for row in reheadered(data_source, ['email', 'zipcode', 'name']):
    ...     print(row)
    {'email': 'nellie@sox.com', 'name': 'Nellie Newsock', 'zipcode': '45309'}


### Identifying columns by regex

If `headers` is a `dict`, the values are used as regular expression matches
against the data values.

    >>> from commonregex import email
    >>> headers = {'Full Name': None, 'addr': email, 'postal_code': r'^[0-9-+]$'}
    >>> for row in reheadered(data_source, ['email', 'zip_code', 'name']):
    ...     print(row)

The values may be either strings (which will be compiled to regexes) or
compiled regexes (to include regex compilation flags of your choice).
In this instance, we have used a compiled regex supplied by the
separate `commonregex` package.

For a regex of `None`, reheader falls back on a fuzzy match of header name.

### Optional arguments

* `keep_extra` (default `False`): Columns missing from `headers` should
  be included in results

* `minimum_score` (default 60): Fuzzy header match must meet this score
  (of 100) to be considered a hit

* `prefer_fuzzy` (default `False`): Even if a header has a regex, prefer
  a fuzzy match of header name where possible

* `header_present` (default `None`): For a list of lists only, `True`
  indicates that the first non-empty row contains headers.  `False`
  indicates that there is no header row, and regexes must be used to
  identify columns.  An integer indicates multi-row headers.
  By default (`None`), reheader guesses whether the first row is a
  header based on its rough similarity in form to subsequent rows.


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter)
and the [18F/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.

## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
