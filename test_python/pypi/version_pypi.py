from __future__ import annotations

import re
from functools import total_ordering


@total_ordering
class PyPiVersion:
    """Class build based on PEP 440 (https://www.python.org/dev/peps/pep-0440/)"""

    # There are some crazy versions numbers that uses - (slash) to separate
    suffix_pattern = re.compile(
        r"(a[0-9]+)|(b[0-9]*)|(c[0-9]*)|(rc[0-9]*)|(\.dev[0-9]*)|(\.post[0-9]*)|(-[0-9]*)"
    )
    suffix_pattern_number = re.compile(r"(a)|(b)|(c)|(rc)|(\.dev)|(\.post)|(-)")

    def __init__(self, version: str) -> None:
        self.__version_str = version
        self.__version = [0, 0, 0]
        self.__suffix = ["", ""]
        self.__compress_suffix = ""
        self.__pypi_version_parser()

    def __pypi_version_parser(self) -> None:
        """Internal method that parses the version number and suffix of a package"""
        version_number, *suffixes = list(
            filter(None, re.split(PyPiVersion.suffix_pattern, self.__version_str))
        )
        self.__version = list(map(int, version_number.split(".")))
        if suffixes:
            self.__suffix = list(
                filter(None, re.split(PyPiVersion.suffix_pattern_number, suffixes[0]))
            )
            self.__compress_suffix = "".join(self.__suffix)

    @property
    def version(self) -> list:
        return self.__version

    @property
    def suffix(self) -> list:
        return self.__suffix

    @property
    def compress_suffix(self) -> str:
        return self.__compress_suffix

    def __eq__(self, __o: PyPiVersion) -> bool:
        if self.version == __o.version and self.compress_suffix == __o.compress_suffix:
            return True
        return False

    def __lt__(self, __o: PyPiVersion) -> bool:
        if (
            self.version < __o.version
            and len(self.compress_suffix) == 0
            and len(__o.compress_suffix) == 0
        ):
            return True
        elif (
            self.version == __o.version
            and len(self.compress_suffix) > 0
            and len(__o.compress_suffix) == 0
        ):
            return True
        elif (
            self.version == __o.version
            and len(self.compress_suffix) > 0
            and len(__o.compress_suffix) > 0
        ):
            if (
                (self.suffix[0] == ".dev" and __o.suffix[0] == "a")
                or (self.suffix[0] == ".dev" and __o.suffix[0] == "b")
                or (self.suffix[0] == ".dev" and __o.suffix[0] == "c")
                or (self.suffix[0] == ".dev" and __o.suffix[0] == "rc")
                or (self.suffix[0] == ".dev" and __o.suffix[0] == ".post")
                or (self.suffix[0] == "a" and __o.suffix[0] == "b")
                or (self.suffix[0] == "a" and __o.suffix[0] == "c")
                or (self.suffix[0] == "a" and __o.suffix[0] == "rc")
                or (self.suffix[0] == "a" and __o.suffix[0] == ".post")
                or (self.suffix[0] == "b" and __o.suffix[0] == "c")
                or (self.suffix[0] == "b" and __o.suffix[0] == "rc")
                or (self.suffix[0] == "b" and __o.suffix[0] == ".post")
                or (self.suffix[0] == "c" and __o.suffix[0] == "rc")
                or (self.suffix[0] == "c" and __o.suffix[0] == ".post")
                or (self.suffix[0] == "rc" and __o.suffix[0] == ".post")
            ):
                return True
            elif self.suffix[0] == __o.suffix[0]:
                if self.suffix[1] < __o.suffix[1]:
                    return True
        return False

    def __repr__(self) -> str:
        fversion = ".".join([str(version) for version in self.version])
        fsuffix = "".join([str(suffix) for suffix in self.suffix])
        return f"{fversion}{fsuffix}"
