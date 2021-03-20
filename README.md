# pytest-httpx-blockage

![](https://github.com/SlavaSkvortsov/pytest-httpx-blockage/workflows/test/badge.svg)
[![pypi](https://img.shields.io/pypi/v/pytest-httpx-blockage.svg)](https://pypi.python.org/pypi/pytest-httpx-blockage)
[![versions](https://img.shields.io/pypi/pyversions/pytest-httpx-blockage.svg)](https://github.com/SlavaSkvortsov/pytest-httpx-blockage)

Package disables requests during pytest execution for [HTTPX](https://www.python-httpx.org/) 

If request occurs, `RequestBlockageException` will be raised.

# Installation
- Install `pytest-httpx-blockage` ([or download from PyPI](https://pypi.org/project/pytest-httpx-blockage/)):
```shell script
pip install pytest-httpx-blockage
```

- Pass param `--blockage-httpx` to enable blockage.

# Configuration

By default, blockage will be disabled in tests marked as `integration`. 
You can override it using `--disable-blockage-mark=new_mark`.

All settings can be stored in your `.cfg` file, with the same variable names as
the argument names mentioned under usage:

    blockage-httpx=true
    disable-blockage-mark=new_mark
