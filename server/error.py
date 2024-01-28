__all__ = ["AppError", "missing_param"]

class AppError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def missing_param(message):
    return AppError({"code": "missing_param", "message": message}, 400)
