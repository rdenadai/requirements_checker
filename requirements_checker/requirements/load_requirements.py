import json
import re
from pathlib import Path

import pkg_resources
from httpx import AsyncClient
from requirements_checker.exceptions import RequirementsDoesntExists
from requirements_checker.pypi.search_pypi import search_pypi
from requirements_checker.pypi.version_pypi import PyPiVersion


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
                if len(requirement) > 1:
                    requirement[1] = requirement[1].split(";")[0]
                # Append to final list
                requirements.append(requirement)
            # Inplace sort the requirements
            requirements.sort()
            return requirements
    else:
        raise RequirementsDoesntExists(f"{path} not found.")


async def get_main_requirements_checked(path: str) -> str:
    """The main function that glues all functionality

    Args:
        path (str): The full system path of the requirements.txt to be analyze

    Returns:
        str: A json string with package_name, currentVersion, latestVersion, outOfDate
    """
    # Load requirements.txt from path
    requirements = load_requirements(path)
    # Async client to search pypi api
    async with AsyncClient() as async_client:
        results = []
        for requirement in requirements:
            package, *version = requirement
            latest_version = await search_pypi(async_client, package)
            out_of_date = False
            if version:  # if there is a version pinned on the requirements.txt
                version = PyPiVersion(version[0])
                # Compare versions!
                if latest_version > version:
                    out_of_date = True
            else:  # since we don't know if the project is already in use or not, lets mark to update
                out_of_date = True
            # Add to the return
            results.append(
                {
                    "packageName": package,
                    "currentVersion": str(version) if version else "",
                    "latestVersion": str(latest_version),
                    "outOfDate": out_of_date,
                }
            )
    return json.dumps(results, indent=4)
