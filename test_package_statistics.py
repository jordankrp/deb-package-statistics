import pytest
from collections import defaultdict
from package_statistics import parse_contents, get_top_package_occurence

@pytest.fixture
def sample_contents():
    return """
usr/bin/foo packageA,packageB
usr/bin/bar packageB
usr/lib/bar packageB
usr/sbin/baz packageC,packageA
./usr/local/bin/foobar packageA
file/without/package
"""

@pytest.fixture
def expected_statistics():
    return defaultdict(int, {
        'packageA': 2,
        'packageB': 3,
        'packageC': 1
    })

def test_parse_contents(sample_contents, expected_statistics):
    result = parse_contents(sample_contents)
    assert result == expected_statistics


def test_get_top_packages(expected_statistics):
    result = get_top_package_occurence(expected_statistics)
    sorted_statistics = [('packageB', 3),('packageA', 2),('packageC', 1)]
    assert result == sorted_statistics