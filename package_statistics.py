#!/usr/bin/env python3

"""Script utility for showing statistics of deb index files"""

import argparse
from collections import defaultdict
import gzip
import requests


MIRROR_URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"
TOP_N_PACKAGES = 10


def download_contents_file(architecture):
    """
    Download and decompress the Contents file for the given architecture from the Debian mirror.
    """
    url = f"{MIRROR_URL}Contents-{architecture}.gz"
    response = requests.get(url, timeout=20)
    if response.status_code != 200:
        # pylint: disable=broad-exception-raised
        raise Exception(
            f"Failed to download Contents file for architecture: \
                {architecture}\nResponse code: {response.status_code}"
        )
    return gzip.decompress(response.content).decode("utf-8")


def parse_contents(contents):
    """
    Parse the contents of the index file and count the number of files associated with each package.
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
        if filename.startswith("."):
            continue

        # Split package(s) based on comma and count up in dictionary
        packages = packages.split(",")
        for package in packages:
            package_file_count[package] += 1

    # Return a dictionary where keys are package names and
    # values are counts of files associated with those packages
    return package_file_count


def get_top_package_occurence(package_file_count):
    """
    Get the top N packages with the most files.
    """

    # Convert dictionary into a list of tuples and sort this list based
    # on the second element of each tuple, representing file count
    sorted_packages = sorted(
        package_file_count.items(), key=lambda x: x[1], reverse=True
    )

    # Return only the top N occuring packages and their file count
    return sorted_packages[:TOP_N_PACKAGES]


def main():
    """
    Main script function.
    """
    parser = argparse.ArgumentParser(
        description="Tool for Debian package file statistics"
    )
    parser.add_argument(
        "architecture", help="Architecture (e.g. amd64, arm64, i386 etc.)"
    )
    args = parser.parse_args()

    try:
        contents = download_contents_file(args.architecture)
        package_file_count = parse_contents(contents)
        top_packages = get_top_package_occurence(package_file_count)

        for package, file_count in top_packages:
            print(f"{package}\t{file_count}")

    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
