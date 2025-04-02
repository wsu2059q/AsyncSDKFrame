class Trigger:
    def __init__(self, sdk, logger):
        self.logger = logger
        self.on = "message.receive.normal"
        self.handles: list[object] = []

    def AddHandle(self, handle):
        self.logger.info(f"Add Handler {handle.__name__}")
        self.handles.append(handle)

    def OnRecv(self, data):
        for handle in self.handles:
            handle(data)
