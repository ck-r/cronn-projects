class NotDrawnError(TypeError):
    def __init__(self, objecttype):
        super().__init__(f'object of type {objecttype} is not drawn.')


class KeyNotSupportedError(ValueError):
    def __init__(self, key):
        super().__init__(f'Keycode {key} not supported.')


class FunctionDoesNotExistsError(ValueError):
    def __init__(self, func_name):
        super().__init__(f'Function {func_name} does not exit.')
