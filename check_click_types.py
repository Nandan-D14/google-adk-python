import click
from typing import Callable, TypeVar, Any

F = TypeVar("F", bound=Callable[..., Any])

@click.option("--foo")
def my_func(foo: str) -> None:
    pass

reveal_type(click.option)
reveal_type(my_func)
