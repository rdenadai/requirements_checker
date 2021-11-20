from __future__ import annotations

import asyncio
import json
import re

from httpx import AsyncClient

try:
    from pypi.search_pypi import search_pypi
    from pypi.version_pypi import PyPiVersion
    from requirements.load_requirements import load_requirements
except ModuleNotFoundError as mnfe:
    from .pypi.search_pypi import search_pypi
    from .pypi.version_pypi import PyPiVersion
    from .requirements.load_requirements import load_requirements


async def main() -> str:
    # Load requirements.txt from path
    requirements = load_requirements("/home/rdenadai/Projetos/test_python/requirements.txt")
    # Async client to search pypi api
    async with AsyncClient() as async_client:
        results = []
        for requirement in requirements:
            package, *version = requirement
            latest_version = await search_pypi(async_client, package)
            out_of_date = False
            if version:
                version = PyPiVersion(version[0])
                if latest_version > version:
                    out_of_date = True
            else:
                out_of_date = True
            results.append(
                {
                    "packageName": package,
                    "currentVersion": str(version) if version else "",
                    "latestVersion": str(latest_version),
                    "outOfDate": out_of_date,
                }
            )
    return json.dumps(results)


if __name__ == "__main__":
    print(asyncio.run(main()))
