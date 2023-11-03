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
        case "Lights10":
            return "materials/input/stockVideos/lights/short-720p-10fps.mp4"
        case "Bees":
            return "materials/input/stockVideos/bees/bee_-_39121 (720p).mp4"
        case "Bees360p":
            return "materials/input/stockVideos/bees/bee_-_39121 (360p).mp4"
        


# # Filtri applicati durante l'upscaling (se filtro = None non viene applicato)
    # EDSR darebbe un miglior risultato nel miglioramento dell'immagine ma necessita di rete neurale preaddestrata e noi volevamo invece soffermarci su un sistema di algoritmi

def SelectFilters(input_string):

    filtersValues, increaseContrast = None, None

    match input_string:
        case "None":
            return None, None
        
        case "Bees":
            filtersValues = {
                "blur_k_dim": 5,            #dimensione kernel blurring iniziale
                "blur_sigma_x": 1.5,        #sigma blurring iniziale
                "sharp_k_center": 7,        #valore centrale del kernel di sharpening
                "Laplacian_k_size": 3,      #dimensione kernel laplaciano (più è basso più rileva edge sottili )
                "threshold_value": 9,       #valore threshold (precisione degli edge inclusi nella binarizzazione 0-255 più è bassa più edge include)
                "blur_k_dim_2": 5,          #dimensione kernel blurring finale
                "blur_sigma_x_2": 1,        #sigma blurring finale
                "showEdges": False          #tenere a false
            }

        case "Bees360p":
            filtersValues = {
                "blur_k_dim": 21,            #dimensione kernel blurring iniziale
                "blur_sigma_x": 2,          #sigma blurring iniziale
                "sharp_k_center": 21,        #valore centrale del kernel di sharpening
                "Laplacian_k_size": 3,      #dimensione kernel laplaciano (più è basso più rileva edge sottili )
                "threshold_value": 4,       #valore threshold (precisione degli edge inclusi nella binarizzazione 0-255 più è bassa più edge include)
                "blur_k_dim_2": 15,          #dimensione kernel blurring finale
                "blur_sigma_x_2": 1,        #sigma blurring finale
                "showEdges": False          #tenere a false
            }

        case "Lights10":
            filtersValues = {
                "blur_k_dim": 5,            #dimensione kernel blurring iniziale
                "blur_sigma_x": 1,          #sigma blurring iniziale
                "sharp_k_center": 3,        #valore centrale del kernel di sharpening
                "Laplacian_k_size": 1,      #dimensione kernel laplaciano (più è basso più rileva edge sottili )
                "threshold_value": 10,       #valore threshold (precisione degli edge inclusi nella binarizzazione 0-255 più è bassa più edge include)
                "blur_k_dim_2": 5,          #dimensione kernel blurring finale
                "blur_sigma_x_2": 0.5,      #sigma blurring finale
                "showEdges": False
            }

    return filtersValues, increaseContrast



