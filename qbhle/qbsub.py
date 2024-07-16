
class QBSub:
    def __init__(self, name, arg_types):
        if not isinstance(name, str):
            raise TypeError("Expected str, got {}({})"
                            .format(name, type(name).__name__))
        if not isinstance(arg_types, list):
            raise TypeError("Expected list, got {}({})"
                            .format(arg_types, type(arg_types).__name__))
        self.name = name
        self.arg_types = arg_types
