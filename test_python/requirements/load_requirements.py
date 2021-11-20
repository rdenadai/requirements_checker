import re
from pathlib import Path

import pkg_resources

try:
    from exceptions import RequirementsDoesntExists
except ModuleNotFoundError as mnfe:
    from ..exceptions import RequirementsDoesntExists


def load_requirements(path: str) -> list:
    """Support function to load and parse a requirements.txt file

    Args:
        path (str): The path to the requirements.txt

    Raises:
        RequirementsDoesntExists: Requirements not found

    Returns:
        list: List with each requirement as a tuple of package name and version number
    """
    file_path = Path(path)
    # Path must exist
    if file_path.exists():
        # Open file
        with file_path.open() as requirements_txt:
            # Regex pattern to use in split
            pattern = re.compile(r"(==)|(>=)|(<=)")
            requirements = []
            for requirement in pkg_resources.parse_requirements(requirements_txt):
                # Filter None values of splitted regex
                requirement = filter(None, pattern.split(str(requirement)))
                # Remove eq, gt, lt from list
                requirement = map(lambda dep: re.sub(pattern, "", dep), requirement)
                # Filter None values
                requirement = list(filter(None, requirement))
                # Remove any info extra to package name
                requirement[0] = requirement[0].split("[")[0]
                requirement[1] = requirement[1].split(";")[0]
                # Append to final list
                requirements.append(requirement)
            # Inplace sort the requirements
            requirements.sort()
            return requirements
    else:
        raise RequirementsDoesntExists(f"{path} not found.")
