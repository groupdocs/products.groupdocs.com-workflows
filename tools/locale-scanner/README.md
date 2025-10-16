# Locale Scanner

A Python program that recursively scans folders to extract locale information from markdown files.

## Features

- Recursively scans directories and subdirectories
- Identifies product folders (top-level folders)
- Extracts locale codes from markdown filenames
- Supports multiple filename patterns for locale detection
- Provides organized output by product with associated locales

## Usage

```bash
python locale_scanner.py <folder_path> [options]
```

### Arguments

- `folder_path`: Path to the folder containing product folders with markdown files

### Options

- `--verbose`, `-v`: Enable verbose output showing all scanned files

### Examples

```bash
# Scan a specific directory
python locale_scanner.py /path/to/products

# Scan current directory
python locale_scanner.py .

# Enable verbose output
python locale_scanner.py /path/to/products --verbose
```

## Expected Folder Structure

```
root_folder/
├── product1/
│   ├── _index.en.md
│   ├── _index.es.md
│   └── _index.fr.md
├── product2/
│   ├── content.de.md
│   ├── content.it.md
│   └── content.pt.md
└── product3/
    ├── readme_ja.md
    ├── readme_ko.md
    └── readme_zh.md
```

## Supported Locale Patterns

The program recognizes locale codes in markdown filenames using these patterns:

- `filename.locale.md` (e.g., `content.en.md`)
- `filename_locale.md` (e.g., `readme_ja.md`)
- `filename.locale.extension.md` (e.g., `index.en-US.md`)
- `filename_locale.extension.md` (e.g., `content_zh-CN.md`)

Locale codes are typically 2-5 characters long and are case-insensitive.

## Output Format

The program outputs:
- Number of products found
- Product name
- List of locales (sorted alphabetically)
- Count of locales per product

Example output:
```
Found 3 product(s) with locale information:
============================================================

Product: product1
Locales (3): en, es, fr

Product: product2
Locales (3): de, it, pt

Product: product3
Locales (3): ja, ko, zh
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

No installation required. Just run the script directly:

```bash
python locale_scanner.py <folder_path>
```
