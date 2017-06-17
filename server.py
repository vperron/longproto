import asyncio
import os


from aiohttp import web

q = asyncio.Queue()

async def push(request):
    await q.put('answer available')
    return web.Response()


async def crash(request):
    """Try crashing the server, useless as the Kernel closes the sockets anyway"""
    os._exit(1)


async def index(request):
    print("Connected, waiting")
    value = await q.get()
    print("Stopped waiting, returning response")
    return web.Response(text='Data: %s' % value)

app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/crash', crash)
app.router.add_get('/push', push)
web.run_app(app, host='127.0.0.1', port=8080)
