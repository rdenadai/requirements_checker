import pytest
from httpx import AsyncClient

try:
    from test_python.pypi.search_pypi import search_pypi
    from test_python.pypi.version_pypi import PyPiVersion
except ModuleNotFoundError as mnfe:
    from ..test_python.pypi.search_pypi import search_pypi
    from ..test_python.pypi.version_pypi import PyPiVersion


@pytest.mark.asyncio
async def test_regular_connection():
    async with AsyncClient() as client:
        version = await search_pypi(client, "httpx")
        assert version > PyPiVersion("0.0.1")


@pytest.mark.asyncio
async def test_unknown_package():
    async with AsyncClient() as client:
        version = await search_pypi(client, "rodolfo")
        assert version == PyPiVersion("0.0.0")
