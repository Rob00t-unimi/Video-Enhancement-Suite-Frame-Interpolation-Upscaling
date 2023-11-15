class Factors:

    # REQUIRES: interpolationFirst is a boolean, zoom_factor is a positive number, numFrameInterpol is a positive integer
    # MODIFIES: None
    # EFFECTS: Initializes Factors object with the specified or default values.
    
    # CONSTRUSTOR
    def __init__(self, interpolationFirst=False, zoom_factor=1.5, numFrameInterpol=3):
        self._interpolationFirst = self._validate_boolean(interpolationFirst)
        self._zoom_factor = self._validate_positive_numeric(zoom_factor)
        self._numFrameInterpol = self._validate_positive_integer(numFrameInterpol)

    # Setters
    def set_interpolationFirst(self, value):
        self._interpolationFirst = self._validate_boolean(value)

    def set_zoom_factor(self, value):
        self._zoom_factor = self._validate_positive_numeric(value)

    def set_numFrameInterpol(self, value):
        self._numFrameInterpol = self._validate_positive_integer(value)


    def _validate_positive_numeric(self, value):
        if not (isinstance(value, int) or isinstance(value, float)) or value <= 0:
            raise ValueError("Value must be a positive numeric value.")

    def _validate_positive_integer(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Value must be a positive integer.")

    def _validate_boolean(self, value):
        if not isinstance(value, bool):
            raise ValueError("Value must be a boolean.")