from __future__ import annotations

import json
import asyncpg
from typing import TYPE_CHECKING, Protocol, Any

if TYPE_CHECKING:
    from types import TracebackType


__all__: tuple[str, ...] = ("create_pool", "DatabaseProtocol")


async def create_pool(dsn: str, size: int = 20) -> asyncpg.Pool:
    """
    Create a pool of connections to the database.

    Parameters
    ----------
    dsn : str
        The database connection string.
    size : int, optional
        The size of the pool, by default 20

    Returns
    -------
    asyncpg.Pool
        The pool of connections to the database.
    """
    def _encode_jsonb(value):
        return json.dumps(value)

    def _decode_jsonb(value):
        return json.loads(value)

    async def init(con):
        await con.set_type_codec(
            "jsonb",
            schema="pg_catalog",
            encoder=_encode_jsonb,
            decoder=_decode_jsonb,
            format="text",
        )

    return await asyncpg.create_pool(
        dsn=dsn,
        init=init,
        command_timeout=300,
        max_size=size,
        min_size=size,
    )


class ConnectionContextManager(Protocol):
    """
    A protocol for a context manager to manage a connection to the database.
    """
    async def __aenter__(self) -> asyncpg.Connection: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...


class DatabaseProtocol(Protocol):
    """
    A protocol for the database.
    """
    async def execute(
        self, query: str, *args: Any, timeout: float | None = None
    ) -> str: ...

    async def fetch(
        self, query: str, *args: Any, timeout: float | None = None
    ) -> list[Any]: ...

    async def fetchrow(
        self, query: str, *args: Any, timeout: float | None = None
    ) -> Any | None: ...

    def acquire(self, *, timeout: float | None = None) -> ConnectionContextManager: ...

    def release(self, connection: asyncpg.Connection) -> None: ...
