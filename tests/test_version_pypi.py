import pytest

try:
    from test_python.pypi.version_pypi import PyPiVersion
except ModuleNotFoundError as mnfe:
    from ..test_python.pypi.version_pypi import PyPiVersion


@pytest.mark.parametrize(
    "v1,v2,expected",
    [
        (PyPiVersion("0.6.0"), PyPiVersion("0.6.0"), True),
        (PyPiVersion("1.6.0"), PyPiVersion("1.6.0"), True),
        (PyPiVersion("0.1.1"), PyPiVersion("0.1.2"), False),
        (PyPiVersion("0.2"), PyPiVersion("0.2"), True),
        (PyPiVersion("5.2.1a1"), PyPiVersion("5.2.1a1"), True),
        (PyPiVersion("0.2.1b1"), PyPiVersion("0.2.1b1"), True),
        (PyPiVersion("0.5.1a3"), PyPiVersion("0.5.1a1"), False),
        (PyPiVersion("0.1a3"), PyPiVersion("0.1a1"), False),
    ],
)
def test_version_pypi_equal(v1, v2, expected):
    assert (v1 == v2) == expected


@pytest.mark.parametrize(
    "v1,v2,expected",
    [
        (PyPiVersion("0.6.0"), PyPiVersion("0.5.1"), True),
        (PyPiVersion("1.6.0"), PyPiVersion("0.5.0"), True),
        (PyPiVersion("0.1.1"), PyPiVersion("0.1.0"), True),
        (PyPiVersion("0.2"), PyPiVersion("0.1.0"), True),
        (PyPiVersion("5.2.1rc1"), PyPiVersion("5.2.1a1"), True),
        (PyPiVersion("0.2.1rc1"), PyPiVersion("0.2.1b5"), True),
        (PyPiVersion("0.5.1a1"), PyPiVersion("0.5.1a2"), False),
        (PyPiVersion("0.5.1.dev1"), PyPiVersion("0.5.1a2"), False),
        (PyPiVersion("0.1a1"), PyPiVersion("0.0.1a3"), True),
    ],
)
def test_version_pypi_lt_gt(v1, v2, expected):
    assert (v1 > v2) == expected
