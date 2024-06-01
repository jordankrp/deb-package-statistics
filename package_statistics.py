#!/usr/bin/env python3

import argparse
import requests
import gzip
from collections import defaultdict

MIRROR_URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"
TOP_N_PACKAGES = 10

def download_contents_file(architecture):
    """
    Download and decompress the Contents file for the given architecture from the Debian mirror.
    """
    url = f"{MIRROR_URL}Contents-{architecture}.gz"
    response = requests.get(url)
    if response.status_code == 200:
        return gzip.decompress(response.content).decode('utf-8')
    else:
        raise Exception(f"Failed to download Contents file for architecture: {architecture}\nResponse code: {response.status_code}")

def parse_contents(contents):
    """
    Parse the Contents file and count the number of files associated with each package.
    """
    package_file_count = defaultdict(int)

    # Split the file contents based on new lines.
    for line in contents.splitlines():

        # Get the file path (including any whitespace characters) and the package(s).
        # We expect 2 values to unpack due to 2 columns, otherwise ignore line.
        try:
            filename, packages = line.rsplit(maxsplit=1)
        except ValueError:
            continue

        # Ignore leading dot in filename
        if filename.startswith('.'):
            continue

        # Split package(s) based on comma and count up in dictionary
        packages = packages.split(',')
        for package in packages:
            package_file_count[package] += 1

    # Return a dictionary where keys are package names and
    # values are counts of files associated with those packages
    return package_file_count

def get_top_packages(package_file_count):
    """
    Get the top N packages with the most files.
    """

    # Convert dictionary into a list of tuples and sort this list based
    # on the second element of each tuple, representing file count
    sorted_packages = sorted(package_file_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_packages[:TOP_N_PACKAGES]

def main():
    parser = argparse.ArgumentParser(description='Tool for Debian package file statistics')
    parser.add_argument('architecture', help='Architecture (e.g. amd64, arm64, i386 etc.)')
    args = parser.parse_args()
    
    try:
        contents = download_contents_file(args.architecture)
        package_file_count = parse_contents(contents)
        top_packages = get_top_packages(package_file_count)

        for package, file_count in top_packages:
            print(f"{package}\t{file_count}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()