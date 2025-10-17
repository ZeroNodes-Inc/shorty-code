# shorty-code

`shorty` is a lightweight utility that removes comments and redundant blank lines from source files.  
It is designed to work with common programming languages such as C, C++, C#, Java, JavaScript, PHP, Python and HTML.

## Installation

```bash
pip install .
```

## Usage

Read from a file and write to stdout:

```bash
shorty path/to/file.py
```

Specify the language explicitly:

```bash
shorty path/to/file.cpp --language cpp
```

Write the result to a file:

```bash
shorty path/to/file.php --language php --output path/to/minified.php
```

You can also pipe data through the tool:

```bash
cat index.html | shorty --language html
```
