class Filters:

    @staticmethod
    def _validate_positive_odd_integer(value):
        if not isinstance(value, int) or value < 0 or value % 2 == 0 or None:
            raise ValueError("Value must be a positive odd integer.")
        return value

    @staticmethod
    def _validate_positive_numeric(value):
        if not isinstance(value, (int, float)) or value < 0 or None:
            raise ValueError("Value must be a positive numeric value.")
        return value

    @staticmethod   
    def _validate_numeric(value):
        if not isinstance(value, (int, float)) or None:
            raise ValueError("Value must be a numeric value.")
        return value
    
    @staticmethod
    def _validate_boolean(value):
        if not isinstance(value, bool) or None:
            raise ValueError("showEdges must be a boolean.")
        return value

