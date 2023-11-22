class Factors:

    # REQUIRES: interpolationFirst is a boolean, zoom_factor is a positive number, numFrameInterpol is a positive integer
    # MODIFIES: None
    # EFFECTS: Initializes Factors object with the specified or default values.
    
    # CONSTRUSTOR
    def __init__(self, interpolationFirst=False, zoom_factor=1.5, numFrameInterpol=3, numIterations=1):
        self._interpolationFirst = interpolationFirst
        self._zoom_factor = zoom_factor
        self._numFrameInterpol = numFrameInterpol
        self._numIterations = numIterations

    # Setters
    def set_interpolationFirst(self, value):
        self._interpolationFirst = self._validate_boolean(value)
        print(f"Interpolation First: {self._interpolationFirst}")

    def set_zoom_factor(self, value):
        self._zoom_factor = self._validate_positive_numeric(value)
        print(f"Zoom Factor: {self._zoom_factor}")

    def set_numFrameInterpol(self, value):
        self._numFrameInterpol = self._validate_positive_integer(value)
        print(f"Number of Frame Interpolation: {self._numFrameInterpol}")

    def set_numIterations(self, value):
        self._numIterations = self._validate_positive_integer(value)
        print(f"Number of Iterations: {self._numIterations}")


    def _validate_positive_numeric(self, value):
        if not (isinstance(value, int) or isinstance(value, float)) or value <= 0:
            raise ValueError("Value must be a positive numeric value.")

    def _validate_positive_integer(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Value must be a positive integer.")

    def _validate_boolean(self, value):
        if not isinstance(value, bool):
            raise ValueError("Value must be a boolean.")