# Analizzatore di siti web

Questo progetto consiste in un'applicazione Python con un'interfaccia grafica basata su Tkinter. L'applicazione consente di analizzare un sito web inserendo il suo URL e genera domande pertinenti in base al tipo di sito (news, e-commerce, blog o altro). Inoltre, l'applicazione offre funzionalità aggiuntive come l'analisi del sentiment e l'estrazione dei link ai profili social presenti sul sito.

## Requisiti

- Python 3.x
- Librerie Python:
  - requests
  - beautifulsoup4
  - textblob
  - tkinter

## Installazione

1. Clona o scarica il repository sul tuo computer.
2. Installa le librerie Python richieste utilizzando il gestore di pacchetti `pip`:

```
pip install requests beautifulsoup4 textblob
```

Le librerie `tkinter` e `scrolledtext` sono incluse nella distribuzione standard di Python, quindi non è necessario installarle separatamente.

## Utilizzo

1. Inserisci la tua chiave API di OpenAI.
2. Esegui il file `website_analysis.py` per avviare l'applicazione.
3. Nell'interfaccia grafica, inserisci l'URL del sito web da analizzare nel campo di testo.
4. Fai clic sul pulsante "Analizza sito" per avviare l'analisi del sito web.
5. L'applicazione determinerà il tipo di sito (news, e-commerce, blog o altro) e genererà delle domande pertinenti nell'interfaccia.
6. Puoi fare clic sui pulsanti delle domande predefinite per visualizzare le risposte generate dal chatbot basato sull'intelligenza artificiale.
7. Puoi anche inserire manualmente una domanda sul sito internet per ottenere una risposta dal chatbot.
8. L'applicazione offre anche le funzionalità di analisi del sentiment e di estrazione dei link ai profili social presenti sul sito web.

## Funzionalità chiave

- Analisi del contenuto di un sito web tramite web scraping
- Determinazione del tipo di sito (news, e-commerce, blog o altro)
- Generazione di domande pertinenti in base al tipo di sito
- Chatbot basato su ChatGPT per rispondere alle domande
- Analisi del sentiment del contenuto del sito web
- Estrazione dei link ai profili social presenti sul sito

## Licenza

Questo progetto è rilasciato sotto la licenza [GPL](https://www.gnu.org/licenses/gpl-3.0.html).

## Crediti

Questo progetto utilizza le seguenti librerie di terze parti:

- [requests](https://requests.readthedocs.io/en/latest/) per effettuare richieste HTTP
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) per il parsing HTML
- [textblob](https://textblob.readthedocs.io/en/dev/) per l'analisi del sentiment
- [tkinter](https://docs.python.org/3/library/tk.html) per l'interfaccia grafica
