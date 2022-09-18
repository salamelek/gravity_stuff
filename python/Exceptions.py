class IncorrectoPointCoordsError(Exception):
    def __init__(self, wrong_point):
        error_message = f"'{wrong_point}' is a {type(wrong_point)} instead of being a tuple or Point object"
        super().__init__(error_message)
