import functools


def to_sync(async_function):
    @functools.wraps(async_function)
    def wrapped():
        import asyncio

        return asyncio.run(async_function())

    return wrapped
