from __future__ import annotations

import asyncio
from functools import wraps

import click

try:

    from requirements.load_requirements import get_main_requirements_checked
except ModuleNotFoundError as mnfe:
    from .requirements.load_requirements import get_main_requirements_checked


# Wrapper need it to run a async fn with click
def coro(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return asyncio.run(fn(*args, **kwargs))

    return wrapper


@click.command()
@click.option(
    "--path",
    default="requirements.txt",
    prompt="Path to requirements.txt",
    help="Set the full system path to the requirements.txt file to be analyse.",
)
@coro
async def main(path: str) -> None:
    """Main function to run

    Args:
        path (str): The full system path to the requirements.txt to be analyze
    """
    print(await get_main_requirements_checked(path))


if __name__ == "__main__":
    main()
