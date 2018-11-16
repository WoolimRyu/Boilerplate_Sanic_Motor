from utils.jsend import JSendResponse


async def handler_bot_tasks(request, id):
    return JSendResponse(200).success()
