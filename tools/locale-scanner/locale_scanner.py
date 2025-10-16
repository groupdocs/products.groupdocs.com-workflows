#!/usr/bin/env python3
"""
Locale Scanner - A program to scan folders recursively and extract locale information from markdown files.

This program:
1. Accepts a folder path as input
2. Recursively scans all subfolders
3. Identifies product folders (top-level folders)
4. Finds .md files with locale information in their names
5. Extracts locale codes from filenames (e.g., _index.af.md -> af)
6. Outputs product names with their associated locales
"""

import os
import sys
import re
import argparse
from pathlib import Path
from collections import defaultdict


def extract_locale_from_filename(filename):
    """
    Extract locale code from markdown filename.
    
    Expected format: filename.locale.md or filename_locale.md
    Examples: _index.af.md -> af, content.en.md -> en
    
    Args:
        filename (str): The filename to extract locale from
        
    Returns:
        str or None: The locale code if found, None otherwise
    """
    # Remove .md extension first
    name_without_ext = filename.replace('.md', '')
    
    # Pattern to match locale codes (2-5 character codes)
    # Look for pattern like .locale or _locale at the end
    patterns = [
        r'\.([a-z]{2,5})$',  # .locale at end
        r'_([a-z]{2,5})$',   # _locale at end
        r'\.([a-z]{2,5})\.', # .locale. in middle
        r'_([a-z]{2,5})\.',  # _locale. in middle
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name_without_ext, re.IGNORECASE)
        if match:
            return match.group(1).lower()
    
    return None


def scan_directory(root_path):
    """
    Recursively scan directory for markdown files and extract locale information.
    
    Args:
        root_path (str): Path to the root directory to scan
        
    Returns:
        tuple: (product_locales_dict, root_locales_set)
    """
    if not os.path.exists(root_path):
        print(f"Error: Directory '{root_path}' does not exist.")
        return {}, set()
    
    if not os.path.isdir(root_path):
        print(f"Error: '{root_path}' is not a directory.")
        return {}, set()
    
    product_locales = defaultdict(set)
    root_locales = set()
    root_path = Path(root_path)
    
    # Get all markdown files recursively
    md_files = list(root_path.rglob('*.md'))
    
    if not md_files:
        print(f"No markdown files found in '{root_path}'")
        return {}, set()
    
    for md_file in md_files:
        # Get relative path from root
        relative_path = md_file.relative_to(root_path)
        path_parts = relative_path.parts
        
        # Skip if no path parts (shouldn't happen)
        if not path_parts:
            continue
        
        # Extract locale from filename
        locale = extract_locale_from_filename(md_file.name)
        
        if locale:
            # If file is directly in root (only one path part), add to root locales
            if len(path_parts) == 1:
                root_locales.add(locale)
            else:
                # First part should be the product name
                product_name = path_parts[0]
                product_locales[product_name].add(locale)
    
    return dict(product_locales), root_locales


def print_results(product_locales, root_locales):
    """
    Print the results in a formatted way.
    
    Args:
        product_locales (dict): Dictionary with product names and their locales
        root_locales (set): Set of locales found in root folder
    """
    total_products = len(product_locales)
    has_root_locales = len(root_locales) > 0
    
    if not product_locales and not root_locales:
        print("No locales found.")
        return
    
    # Print root folder locales first if any
    if has_root_locales:
        root_locales_list = sorted(root_locales)
        print(f"\nRoot folder locales ({len(root_locales_list)}): {', '.join(root_locales_list)}")
        if product_locales:
            print()
    
    # Print product locales
    if product_locales:
        print(f"Found {total_products} product(s) with locale information:")
        print("=" * 60)
        
        for product, locales in sorted(product_locales.items()):
            locales_list = sorted(locales)
            print(f"\nProduct: {product}")
            print(f"Locales ({len(locales_list)}): {', '.join(locales_list)}")
    elif not has_root_locales:
        print("No products with locales found.")


def main():
    """Main function to handle command line arguments and run the scanner."""
    parser = argparse.ArgumentParser(
        description="Scan folders recursively for locale information in markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python locale_scanner.py /path/to/products
  python locale_scanner.py C:\\Documents\\products
  python locale_scanner.py .  # Current directory
        """
    )
    
    parser.add_argument(
        'folder_path',
        help='Path to the folder containing product folders with markdown files'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output showing all scanned files'
    )
    
    args = parser.parse_args()
    
    # Convert to absolute path
    folder_path = os.path.abspath(args.folder_path)
    
    if args.verbose:
        print(f"Scanning directory: {folder_path}")
        print("Looking for markdown files with locale information...")
    
    # Scan the directory
    product_locales, root_locales = scan_directory(folder_path)
    
    # Print results
    print_results(product_locales, root_locales)


if __name__ == "__main__":
    main()
