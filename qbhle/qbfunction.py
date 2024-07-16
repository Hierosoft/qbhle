from qbhle.qbsub import QBSub

class QBFunction(QBSub):
    def __init__(self, name, arg_types, return_types):
        QBSub.__init__(self, name, arg_types)
        if not isinstance(return_types, list):
            raise TypeError("Expected list, got {}({})"
                            .format(return_types, type(return_types).__name__))
        self.return_types = return_types