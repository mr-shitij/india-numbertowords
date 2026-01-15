"""
India Number to Words
=====================

A Python library for converting numbers to words in Indian languages.

Features
--------
- Supports Hindi (more languages coming soon)
- Smart input detection (currency vs individual mode)
- Decimal number support
- Alphanumeric support
- Indian numbering system (Crore, Lakh, Thousand, Hundred)

Installation
------------
```bash
pip install -e .
```

Usage
-----
```python
from india_numbertowords import num2words

# Basic usage
print(num2words(42))  # "बयालीस"

# Large numbers
print(num2words(123456))  # "एक लाख तेईस हज़ार चार सौ छप्पन"

# Individual mode (for phone numbers, codes)
print(num2words("007"))  # "शून्य शून्य सात"

# Decimals
print(num2words("3.14"))  # "तीन दशमलव एक चार"
```

See ARCHITECTURE.md for detailed design documentation.
"""

from setuptools import setup, find_packages

setup(
    name="india-numbertowords",
    version="0.1.0",
    description="Convert numbers to words in Indian languages",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    author="Shitij Agrawal",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
