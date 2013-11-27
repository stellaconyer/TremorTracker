import pusher as pusher_client
"""
This is so that users don't accidentally `from flask.ext.pusher import pusher` and
get the wrong thing.
"""


class Pusher(object):
    def __init__(self, app=None, config=None):
        self.config = None
        self.pusher = None
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app, config=None):
        if config is not None:
            self.config = config
        elif self.config is None:
            self.config = app.config

        self.config.setdefault('PUSHERAPP_ID', '')
        self.config.setdefault('PUSHERAPP_KEY', '')
        self.config.setdefault('PUSHERAPP_SECRET', '')

        self.app = app

        self.pusher = pusher_client.Pusher(
            app_id=self.config['PUSHERAPP_ID'],
            key=self.config['PUSHERAPP_KEY'],
            secret=self.config['PUSHERAPP_SECRET'])

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions['pusher'] = self.pusher