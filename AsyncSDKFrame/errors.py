class CycleDependencyError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidDependencyError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidModuleError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
