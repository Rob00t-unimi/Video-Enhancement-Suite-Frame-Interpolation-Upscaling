# progetto-principi

- set dei path in SelectionPage
- set dei filtri e dei parametri in SelectionPage
- Set e esecuzione di demo.py

- demo.py richiama prima la funzione di upscaling video che cicla sui frame passandoli come immagini alla funzione di upscaling bilineare
- una volta eseguito completamente l'upscaling il nuovo video viene salvato

- premere invio per continuare

- demo.py richiama l'interpolazione di frame inviandogli il video upscalato
- la funzione di interpolazione video aumenta il numero di frame calcolando da prima l'optical flow tra le coppie di frame sia in avanti che indietro, poi interpola tra ogni coppia 3 nuovi frame
- i frame originali vengono scartati
- il video viene salvato