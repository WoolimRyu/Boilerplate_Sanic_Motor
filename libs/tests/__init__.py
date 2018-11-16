import unittest
import mock


class AsyncMock(mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class AppTestCaseBase(unittest.TestCase):
    def __init__(self, app, *args, **kwargs):
        super(AppTestCaseBase, self).__init__(*args, **kwargs)
        self.app = app

    def setUp(self):
        # patch app.stop
        # this is because app should keep looping
        # until added task is done
        old_stop = self.app.stop
        def lazy_stop():
            self.app.loop.call_later(0.1, old_stop)
        self.app.stop = lazy_stop
