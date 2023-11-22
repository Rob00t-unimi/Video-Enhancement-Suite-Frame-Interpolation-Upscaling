import json
import os

class Paths:
    
    # REQUIRES: all parameters are stings of paths, the JSON file must have valid paths

    def __init__(self, json_file_path= 'JSON/outputPath.json', input_video_path=None, output_path_1=None, output_path_2=None, output_path_3=None, output_path_4=None):
        self._load_paths_from_json(json_file_path)
        current_file_path = os.path.abspath(__file__)
        directory_path = os.path.dirname(current_file_path)
        parent_directory = os.path.dirname(directory_path)
        
        self._input_video_path = self._validate_and_set_path(input_video_path)
        self._output_path_1 = self._validate_and_set_path(output_path_1) or parent_directory + "/" + self.data.get("outputpath1")
        self._output_path_2 = self._validate_and_set_path(output_path_2) or parent_directory + "/" + self.data.get("outputPath2")
        self._output_path_3 = self._validate_and_set_path(output_path_3) or parent_directory + "/" + self.data.get("outputPath3")
        self._output_path_4 = self._validate_and_set_path(output_path_4) or parent_directory + "/" + self.data.get("outputPath4")

    # Setters
    def set_input_video_path(self, value):
        self._input_video_path = self._validate_and_set_path(value)

    def set_output_path_1(self, value):
        self._output_path_1 = self._validate_and_set_path(value) or self.data.get("outputpath1")

    def set_output_path_2(self, value):
        self._output_path_2 = self._validate_and_set_path(value) or self.data.get("outputPath2")

    def set_output_path_3(self, value):
        self._output_path_3 = self._validate_and_set_path(value) or self.data.get("outputPath3")

    def set_output_path_4(self, value):
        self._output_path_4 = self._validate_and_set_path(value) or self.data.get("outputPath4")


    # Metodi di validazione
    def _validate_string_path(self, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string.")
        # Verifica se il percorso è assoluto
        if not os.path.isabs(value):
            raise ValueError("Value must be a valid absolute or relative path.")

    def _validate_and_set_path(self, value):
        if value is not None:
            self._validate_string_path(value)
        return value

    def _load_paths_from_json(self, json_file_path):
        with open(json_file_path, 'r') as json_file:
            self.data = json.load(json_file)

