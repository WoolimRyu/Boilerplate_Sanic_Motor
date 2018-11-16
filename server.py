import asyncio
import uvloop
from concurrent import futures

from sanic import Sanic, response
from motor.motor_asyncio import AsyncIOMotorClient

from libs.logging import get_tracer
import blueprints.api
import config


app = Sanic(log_config=config.LOGGING_CONFIG)
app.add_route(lambda _: response.json({}), '/healthcheck', methods=['GET'])

app.blueprint(blueprints.api.bp, url_prefix='/api/v1')


@app.listener('before_server_start')
async def init_db(app, loop):
    conf = config.MONGO_CONF_SONNY
    uri = config.mongo_uri(conf)
    app.db = AsyncIOMotorClient(uri)[conf['database']]


@app.listener('before_server_start')
async def init_executor(app, loop):
    async def execute_async(task, *args, **kwargs):
        executor = futures.ProcessPoolExecutor()
        return await loop.run_in_executor(executor, task, *args)
    app.execute_async = execute_async


@app.middleware('request')
async def inject_tracer(request):
    request.app.tracer = get_tracer(request)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app.run(host='0.0.0.0', port=8000, debug=True)
