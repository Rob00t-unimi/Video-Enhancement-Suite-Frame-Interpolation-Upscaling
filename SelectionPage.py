def SelectVideo(input_string):

    match input_string:      

        case "Waves":
            return "materials/input/stockVideos/waves/waves-720p-25fps.mp4"
        case "Tunnel":
            return "materials/input/stockVideos/tunnel/abstract_-_27726 (720p).mp4" 
        case "Rallye":
            return "materials/input/stockVideos/rallye/export_720p_25fps.mp4"
        case "Smoke": 
            return "materials/input/stockVideos/smoke/smoke_-_65435 (720p).mp4"
        case "Monochrome":
            return "materials/input/stockVideos/monochrome/monochrome_-_27806 (720p).mp4"
        case "Lights":
            return "materials/input/stockVideos/lights/particles_-_10848 (720p).mp4"
        case "Bees":
            return "materials/input/stockVideos/bees/bee_-_39121 (720p).mp4"
        





# # Filtri applicati durante l'upscaling (se filtro = None non viene applicato)
    # bilateral --> fa smoothing preservando più dettagli possibile, quindi ridure il rumore
    # sharpening --> fa il miglioramento della nitidezza enfatizzando i bordi
    # increaseContrast --> aumenta il miglioramento della nitidezza
    # EDSR darebbe un miglior risultato nel miglioramento dell'immagine ma necessita di rete neurale preaddestrata e noi volevamo invece soffermarci su un sistema di algoritmi

def SelectFilters(input_string):

    bilateralFilter, sharpening, increaseContrast = None, None, None

    match input_string:
        case "None":
            return None, None, None
        
        case "Waves":
            bilateralFilter = {
                "d": 19,
                "sigmaColor": 75,
                "sigmaSpace": 75
            }
            sharpening = {
                "weight_upscaled_image": 1.2,
                "weight_current_image": -0.3
            }
            increaseContrast = {
                "alpha": 1.05,
                "beta": 1
            }

        case "Tunnel":
            bilateralFilter = None
            sharpening = {
            "weight_upscaled_image": 1.5,
            "weight_current_image": -0.5
            }
            increaseContrast = {
                "alpha": 1.05,
                "beta": 1
            }
            
        case "Rallye":
            bilateralFilter = {
                "d": 9,
                "sigmaColor": 150,
                "sigmaSpace": 150
            }
            sharpening = {
                "weight_upscaled_image": 0.7,
                "weight_current_image": 0.3
            }
            increaseContrast = {
                "alpha": 1.01,
                "beta": 0
            }

        case "Default":
            bilateralFilter = {
                "d": 9,
                "sigmaColor": 75,
                "sigmaSpace": 75
            }
            sharpening = {
                "weight_upscaled_image": 1.5,
                "weight_current_image": -0.5
            }
            increaseContrast = None

    return bilateralFilter, sharpening, increaseContrast



