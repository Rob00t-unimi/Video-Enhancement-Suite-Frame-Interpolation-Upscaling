from classes.filtersValidator import Filters

class BlurFilter(Filters):
# REQUIRES: blur_k_dim is a positive odd integer or None
        #   blur_sigma_x is a positive numeric value or None
    def __init__(self, blur_k_dim=5, blur_sigma_x=1, execution_position=1):
        self._filter_name = "Blurring"
        self._blur_k_dim = self._validate_positive_odd_integer(blur_k_dim)
        self._blur_sigma_x = self._validate_positive_numeric(blur_sigma_x)
        self._execution_position = execution_position

    # Setters
    def set_blur_k_dim(self, value):
        self._blur_k_dim = self._validate_positive_odd_integer(value)
        print("blur_k_: ", self._blur_k_dim)

    def set_blur_sigma_x(self, value):
        self._blur_sigma_x = self._validate_positive_numeric(value)
        print("blur_sigma_x: ", self._blur_sigma_x)

    def set_execution_position(self, value):
        self._execution_position = value
        print("execution_position: ", self._execution_position)

class SharpenFilter(Filters):
# REQUIRES: sharp_k_center is a positive odd integer or None
    def __init__(self, sharp_k_center=7, execution_position=2):
        self._filter_name = "Sharpening"
        self._sharp_k_center = self._validate_positive_odd_integer(sharp_k_center)
        self._execution_position = execution_position

    # Setters
    def set_sharp_k_center(self, value):
        self._sharp_k_center = self._validate_positive_odd_integer(value)
        print("sharp_k_center: ", self._sharp_k_center)

    def set_execution_position(self, value):
        self._execution_position = value
        print("execution_position: ", self._execution_position)

class EdgeDetectorFilter(Filters):
# REQUIRES: Laplacian_k_size is a positive odd integer or None
        #   showEdges is a boolean
    def __init__(self, Laplacian_k_size=3, show_edges=False, execution_position=3):
        self._filter_name = "Edge Detector"
        self._Laplacian_k_size = self._validate_positive_odd_integer(Laplacian_k_size)
        self._show_edges = self._validate_boolean(show_edges)
        self._execution_position = execution_position
        
    # Setters
    def set_Laplacian_k_size(self, value):
        self._Laplacian_k_size = self._validate_positive_odd_integer(value)
        print("Laplacian_k_size: ", self._Laplacian_k_size)

    def set_show_edges(self, value):
        self._show_edges = self._validate_boolean(value)
        print("show_edges: ", self._show_edges)

    def set_execution_position(self, value):
        self._execution_position = value
        print("execution_position: ", self.set_execution_position)

class BinarizationFilter(Filters):
# REQUIRES: threshold_value is a numeric value or None
    def __init__(self, threshold_value=30, execution_position=4):
        self._filter_name = "Binarization"
        self._threshold_value = self._validate_numeric(threshold_value)
        self._execution_position = execution_position

    # Setters
    def set_threshold_value(self, value):
        self._threshold_value = self._validate_numeric(value)
        print("threshold_value: ", self._threshold_value)

    def set_execution_position(self, value):
        self._execution_position = value
        print("execution_position: ", self._execution_position)

    
class MedianDenoisingFilter(Filters):
# REQUIRES: blur_k_dim_2 is a positive odd integer or None
    def __init__(self, blur_k_dim_2=3, execution_position=5):
        self._filter_name = "Final Blur"
        self._blur_k_dim_2 = self._validate_positive_odd_integer(blur_k_dim_2)
        self._execution_position = execution_position

    # Setters
    def set_blur_k_dim_2(self, value):
        self._blur_k_dim_2 = self._validate_positive_odd_integer(value)
        print("blur_k_dim_2: ", self._blur_k_dim_2)

    def set_execution_position(self, value):
        self._execution_position = value
        print("execution_position: ", self._execution_position)

class ActiveFilters:
    def __init__(self, blurParams=None, sharpParams=None, edgeParams=None, binarizationParams=None, medianDenoisingParams=None):
        self.blurParams = blurParams or BlurFilter()
        self.sharpParams = sharpParams or SharpenFilter()
        self.edgeParams = edgeParams or EdgeDetectorFilter()
        self.binarizationParams = binarizationParams or BinarizationFilter()
        self.medianDenoisingParams = medianDenoisingParams or MedianDenoisingFilter()



