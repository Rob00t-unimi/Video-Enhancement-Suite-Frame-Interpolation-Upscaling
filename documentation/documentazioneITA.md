# Progetto Interpolazione dei Frame e Upscaling per Video

## Passaggi di Elaborazione:

### Interpolazione dei Frame:
1. `demo.py` passa il percorso del video alla funzione di interpolazione dei frame.
2. La funzione di interpolazione video aumenta il numero di frame calcolando prima il flusso ottico tra le coppie di frame sia in avanti che all'indietro, quindi interpolando n nuovi frame tra ciascuna coppia di frame.
3. I frame originali vengono scartati.
4. Il video viene salvato.

### Upscaling del Video:
5. `demo.py` chiama la funzione di upscaling del video, passando il percorso del video interpolato. Per ciascun frame, la funzione invoca la funzione di upscaling bilineare.
6. Una volta che un frame è stato ingrandito, vengono applicati filtri e il frame viene salvato nel nuovo video, fino al completamento.

## Fine del Sistema

## Legenda:

- `Attiva la prima interpolazione`: Permette di selezionare se effettuare prima l'interpolazione dei frame o l'upscaling. Per impostazione predefinita, l'interpolazione dei frame viene eseguita per prima. Dal punto di vista computazionale, eseguire prima l'upscaling e poi l'interpolazione del frame rate è più costoso.

- `Fattore di Zoom`: Numero decimale che definisce il fattore di upscaling.
- `Iterazioni di Upscaling`: Numero intero che indica il numero di iterazioni di upscaling da eseguire. La risoluzione dopo l'upscaling è data da risoluzione iniziale * (fattore di zoom ** iterazioni di upscaling).

- `Numero di Frame da Interpolare`: Numero intero che indica il numero di frame da interpolare tra ogni coppia di frame (i frame originali vengono scartati). Gli FPS finali dopo l'interpolazione sono dati da numero di frame da interpolare * (numero di frame iniziali - 1).

### Durante l'upscaling, vengono applicate ottimizzazioni dell'immagine basate su sfocatura, rilevamento dei bordi laplaciano e miglioramento della nitidezza. Tutti questi filtri sono considerati come un singolo filtro nell'interfaccia utente e vengono applicati in sequenza secondo un algoritmo ottimale. Tuttavia, è possibile personalizzare i parametri.

- `Seleziona un Filtro Preimpostato`: Consente di scegliere tra una serie di filtri preimpostati.
- `Personalizza il Filtro`: Consente di personalizzare i parametri dei filtri menzionati sopra.
- `Visualizza i Bordi`: Mantenere disattivato permette di abilitare o disabilitare la visualizzazione del rilevamento dei bordi sovrapposti all'immagine.

- Parametri dei Filtri:

    * `Dimensioni del Kernel della Prima Sfocatura Applicata`: Questo parametro rappresenta le dimensioni del kernel utilizzato per applicare il filtro di sfocatura alla prima fase dell'upscaling. Le dimensioni del kernel influenzano il grado di sfocatura applicato all'immagine. Valori più grandi generano una sfocatura più intensa.
    * `Sigma X della Prima Sfocatura Applicata`: Sigma X è un parametro del filtro di sfocatura che influenza la deviazione standard della gaussiana utilizzata per la sfocatura. Valori più alti di Sigma X generano una sfocatura più diffusa, mentre valori più bassi creano una sfocatura più localizzata.
    * `Valore Centrale del Kernel di Miglioramento della Nitidezza`: Questo parametro rappresenta il valore centrale del kernel utilizzato per migliorare la nitidezza dell'immagine durante l'upscaling. Aumentare o diminuire il valore centrale influenzerà l'intensità del miglioramento della nitidezza applicato all'immagine.
    * `Valore Centrale del Kernel Laplaciano`: Il valore centrale del kernel laplaciano influisce sulla nitidezza dell'immagine e può essere regolato per ottenere effetti di rilevamento dei bordi più o meno intensi. Aumentare il valore centrale può aumentare l'accentuazione dei bordi.
    * `Soglia di Binarizzazione`: Questo parametro controlla il valore di soglia utilizzato durante il processo di binarizzazione dell'immagine. La binarizzazione è un processo che converte l'immagine in una forma binaria in cui i pixel sopra la soglia sono considerati come bordi. Regolare il valore di soglia determina quanti bordi vengono inclusi nell'immagine finale.
    * `Dimensioni del Kernel della Seconda Sfocatura Applicata`: Questo parametro rappresenta le dimensioni del kernel utilizzato per applicare il filtro di sfocatura alla seconda fase dell'upscaling. Questa fase può essere utilizzata per applicare ulteriore sfocatura all'immagine, se necessario. Le dimensioni del kernel influenzano il grado di sfocatura applicato.
    * `Sigma X della Seconda Sfocatura Applicata`: Sigma X è il parametro del filtro di sfocatura utilizzato nella seconda fase dell'upscaling. Regolare questo valore influenzerà la deviazione standard della gaussiana utilizzata per la sfocatura nella seconda fase. Valori più alti generano una sfocatura più diffusa, mentre valori più bassi creano una sfocatura più localizzata.

Codificato da Roberto Tallarini
