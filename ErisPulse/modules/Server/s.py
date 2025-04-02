import flask


class Server:
    def __init__(self, sdk, logger):
        self.logger = logger
        self.triggers: dict[str, list[object]] = {}
        self.serv = sdk.env.SERVER
        self.app = flask.Flask(__name__)

    def AddTrigger(self, trigger: object):
        t_name = trigger.on
        self.logger.info(f"Add Trigger {t_name}")
        if t_name not in self.triggers:
            self.triggers[t_name] = []
        self.triggers[t_name].append(trigger)

    def Start(self):
        @self.app.route("/", methods=["POST"])
        def Handle():
            data = flask.request.json
            t_name = data["header"]["eventType"]
            if t_name not in self.triggers or len(self.triggers[t_name]) == 0:
                return "IGNORE"
            for h in self.triggers[t_name]:
                h.OnRecv(data)
            return "OK"

        self.logger.info(f"Start Server With {self.serv}")
        self.app.run(**self.serv)
