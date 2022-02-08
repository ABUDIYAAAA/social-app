import websockets
import django
import asyncio
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitterclone.settings')
django.setup()
from sesame.utils import get_user
import contextvars
import functools

async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)


async def handler(websocket):
    sesame = await websocket.recv()
    user = await to_thread(get_user, sesame)
    if user is None:
        await websocket.close(1011, "authentication failed")
        return

    await websocket.send(f"Hello {user}!")


async def main():
    async with websockets.serve(handler, "localhost", 8888):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
