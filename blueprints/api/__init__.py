from sanic import Blueprint

from blueprints.api.handlers import tasks


bp = Blueprint('api')
bp.add_route(tasks.handler_bot_tasks, '/bots/<id>/tasks', methods=['GET'])
