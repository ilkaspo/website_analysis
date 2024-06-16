# Definizione delle costanti per l'API
AUTHORIZATION_KEY = 'LA TUA CHIAVE OpenAI'  
# La chiave di autorizzazione è una stringa che identifica l'utente o l'applicazione che sta effettuando la richiesta all'API.

MODEL = 'gpt-3.5-turbo'
# Questo è il nome del modello di linguaggio utilizzato dall'API OpenAI per generare il testo. 
# In questo caso, stiamo usando il modello gpt-3.5-turbo.

TEMPERATURE = 0.8
# La temperatura è un valore compreso tra 0 e 1 che controlla la casualità delle risposte generate dal modello. 
# Un valore più alto produce risposte più casuali e imprevedibili, mentre un valore più basso produce risposte più deterministiche e coerenti.

MAX_TOKENS = 500
# Questo parametro imposta il numero massimo di token (parole o parti di parole) che il modello può generare nella sua risposta.

TOP_P = 1
# Top_p è un parametro che controlla la diversità delle parole generate dal modello. 
# Un valore più alto produce risposte più diverse, mentre un valore più basso produce risposte più coerenti.

FREQUENCY_PENALTY = 0.5
# La penalità di frequenza è un valore compreso tra 0 e 1 che penalizza il modello per l'uso eccessivo delle stesse parole o frasi nella risposta.

PRESENCE_PENALTY = 0.5
# La penalità di presenza è un valore compreso tra 0 e 1 che penalizza il modello per l'uso di parole o frasi già presenti nel prompt di input.

import requests
import tkinter as tk
from bs4 import BeautifulSoup
from tkinter import messagebox, scrolledtext, ttk
from textblob import TextBlob
from tkinter import ttk, scrolledtext

# Funzione per l'estrazione delle informazioni da una pagina HTML
def extract_information_from_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Solleva un'eccezione per codici di stato HTTP errati
    except requests.RequestException as e:
        print(f"Errore nel recupero del contenuto del sito web: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Estrazione dei titoli
    titles = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    titles_text = [title.get_text() for title in titles]
    
    # Estrazione dei paragrafi
    paragraphs = soup.find_all('p')
    paragraphs_text = [p.get_text() for p in paragraphs]

    # Combinazione dei titoli e dei paragrafi
    content = titles_text + paragraphs_text
    return " ".join(content)

# Funzione per l'invio del messaggio al chatbot
def send_message_to_chatbot(messages):
    payload = {
    'model': MODEL,
    'messages': messages,
    'temperature': TEMPERATURE,
    'max_tokens': MAX_TOKENS,
    'top_p': TOP_P,
    'frequency_penalty': FREQUENCY_PENALTY,
    'presence_penalty': PRESENCE_PENALTY,
    }

    headers = {
    'Authorization': f'Bearer {AUTHORIZATION_KEY}',  # Utilizzo della chiave definita precedentemente
    'Content-Type': 'application/json'
    }   

    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)
        response.raise_for_status()  # Solleva un'eccezione per codici di stato HTTP errati
    except requests.RequestException as e:
        print(f"Errore nella connessione con OpenAI API: {e}")
        return 'Errore nella connessione con OpenAI API'

    data = response.json()
    reply = data['choices'][0]['message']['content'] if 'choices' in data else 'Risposta non disponibile.'
    return reply

# Funzione per generare domande pertinenti in base al tipo di sito
def get_questions_for_site_type(site_type):
    questions = {
        "1": [
            "Quali argomenti tratta principalmente il sito?",
            "Chi sono gli autori principali dei contenuti?",
            "Esiste una sezione dedicata alle ultime notizie?"
        ],
        "2": [
            "Quali sono i principali prodotti venduti?",
            "Quali metodi di pagamento sono accettati?",
            "Esistono offerte o sconti speciali attualmente disponibili?"
        ],
        "3": [
            "Quali argomenti vengono trattati nel blog?",
            "Con quale frequenza vengono pubblicati nuovi post?",
            "È possibile iscriversi a una newsletter?"
        ],
        "4": [
            "Qual è lo scopo principale del sito?",
            "Quali sono le funzionalità principali del sito?",
            "Esistono sezioni interattive o forum sul sito?"
        ]
    }
    return questions.get(site_type, [])

# Funzione per determinare il tipo di sito in base alla risposta iniziale
def determine_site_type(response):
    site_types = ["1", "2", "3", "4"]
    for site_type in site_types:
        if site_type in response:
            return site_type
    return "4"  # Restituisci "4" (Altro) se nessun tipo di sito è trovato nella risposta

# Funzione per il controllo e la correzione dell'URL
def check_and_correct_url(website_url):
    if website_url.startswith("www."):
        website_url = "https://" + website_url
    elif not website_url.startswith("http://") and not website_url.startswith("https://"):
        website_url = "https://www." + website_url
    return website_url

# Funzione per estrarre i link ai profili social
def extract_social_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Errore nel recupero del contenuto del sito web: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    social_links = []

    # Cerca i link ai profili social comuni
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            if 'facebook.com' in href:
                social_links.append(('Facebook', href))
            elif 'twitter.com' in href:
                social_links.append(('X', href))
            elif 'instagram.com' in href:
                social_links.append(('Instagram', href))

    return social_links

# Funzione per l'interazione con l'utente tramite interfaccia grafica
def on_submit():
    website_url = url_entry.get()

    # Controllo e correzione del formato dell'URL
    website_url = check_and_correct_url(website_url)

    website_content = extract_information_from_html(website_url)
    if not website_content:
        messagebox.showerror("Errore", "Non è stato possibile estrarre il contenuto dal sito web.")
        return

    global messages, site_type_determined
    site_type_determined = False
    initial_prompt = f"Ho estratto le seguenti informazioni dal sito: {website_content}. Che tipo di sito è questo? (1: News, 2: E-commerce, 3: Blog, 4: Altro)"
    messages = [
        {"role": "system", "content": "Rispondi solo con un numero e niente altro"},
        {"role": "user", "content": initial_prompt}
    ]

    initial_response = send_message_to_chatbot(messages)

    # Determina il tipo di sito in base alla risposta iniziale
    site_type = determine_site_type(initial_response)

    # Ottieni le domande pertinenti per il tipo di sito
    predefined_questions = get_questions_for_site_type(site_type)

    # Invia una domanda nascosta al chatbot per ottenere una descrizione del sito
    description_prompt = f"Descrivi il sito web in base alle informazioni estratte: {website_content}"
    messages = [
        {"role": "system", "content": "Rispondi come un chatbot del sito internet di cui ti ho inviato il contenuto"},
        {"role": "user", "content": description_prompt}
    ]
    description_response = send_message_to_chatbot(messages)

    # Pubblica la descrizione del sito nella finestra di chat
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, f"Bot: {description_response}\n", 'bot')
    chat_text.config(state=tk.DISABLED)
    chat_text.yview(tk.END)

    # Rimuovi i vecchi pulsanti delle domande predefinite
    for widget in question_frame.winfo_children():
        widget.destroy()

    # Genera nuovi pulsanti per le domande predefinite
    for question in predefined_questions:
        question_button = ttk.Button(question_frame, text=question, command=lambda q=question: on_question_click(q))
        question_button.pack(anchor='w', padx=10, pady=5)

    site_type_determined = True

def on_question_click(question):
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, f"Tu: {question}\n", 'user')
    chat_text.config(state=tk.DISABLED)
    chat_text.yview(tk.END)

    # Aggiungi la domanda selezionata ai messaggi
    messages.append({"role": "user", "content": question})
    
    # Invia i messaggi aggiornati al chatbot
    reply = send_message_to_chatbot(messages)

    # Aggiungi la risposta alla lista dei messaggi
    messages.append({"role": "assistant", "content": reply})

    # Visualizza la risposta nella finestra di chat
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, f"Bot: {reply}\n", 'bot')
    chat_text.config(state=tk.DISABLED)
    chat_text.yview(tk.END)

#funzione che gestisce l'invio di una domanda predefinita al chatbot, visualizza la domanda e la risposta nell'interfaccia grafica e aggiorna la lista dei messaggi di conversazione.
def on_ask():
    user_question = question_entry.get()
    if user_question.strip() == "":
        return

    global messages, site_type_determined

    if site_type_determined:
        # Aggiungi solo la domanda dell'utente, non ripetere il prompt iniziale
        messages.append({"role": "user", "content": user_question})
        
        # Invia i messaggi aggiornati al chatbot
        reply = send_message_to_chatbot(messages)

        # Aggiungi la risposta alla lista dei messaggi
        messages.append({"role": "assistant", "content": reply})

        # Visualizza la domanda e la risposta nella finestra di chat
        chat_text.config(state=tk.NORMAL)
        chat_text.insert(tk.END, f"Tu: {user_question}\n", 'user')
        chat_text.insert(tk.END, f"Bot: {reply}\n", 'bot')
        chat_text.config(state=tk.DISABLED)
        chat_text.yview(tk.END)

    question_entry.delete(0, tk.END)

#Funzione che analizza la pagina web e restituisce la sentiment analysis
def on_sentiment():
    website_url = url_entry.get()

    # Controllo e correzione del formato dell'URL
    website_url = check_and_correct_url(website_url)

    website_content = extract_information_from_html(website_url)
    if not website_content:
        messagebox.showerror("Errore", "Non è stato possibile estrarre il contenuto dal sito web.")
        return

    # Analisi del sentiment del contenuto del sito web
    sentiment = TextBlob(website_content).sentiment
    polarity = sentiment.polarity
    subjectivity = sentiment.subjectivity

    # Interpreta il punteggio di polarità
    if polarity > 0:
        sentiment_label = "Positivo"
    elif polarity < 0:
        sentiment_label = "Negativo"
    else:
        sentiment_label = "Neutrale"

    # Visualizza il risultato dell'analisi del sentiment nella finestra di chat
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, f"Analisi del Sentiment:\n", 'sentiment')
    chat_text.insert(tk.END, f"Polarità: {polarity:.2f}\n", 'sentiment')
    chat_text.insert(tk.END, f"Soggettività: {subjectivity:.2f}\n", 'sentiment')
    chat_text.insert(tk.END, f"Sentiment complessivo: {sentiment_label}\n", 'sentiment')
    chat_text.config(state=tk.DISABLED)
    chat_text.yview(tk.END)

#Funzione che restituisce i social presenti sulla pagina web
def on_social_links():
    website_url = url_entry.get()
    website_url = check_and_correct_url(website_url)

    social_links = extract_social_links(website_url)

    if social_links:
        chat_text.config(state=tk.NORMAL)
        chat_text.insert(tk.END, "Link ai profili social trovati:\n", 'social')
        for platform, link in social_links:
            chat_text.insert(tk.END, f"{platform}: {link}\n", 'social')
        chat_text.config(state=tk.DISABLED)
        chat_text.yview(tk.END)
    else:
        chat_text.config(state=tk.NORMAL)
        chat_text.insert(tk.END, "Nessun link ai profili social trovato.\n", 'social')
        chat_text.config(state=tk.DISABLED)
        chat_text.yview(tk.END)

# Creazione dell'interfaccia grafica
root = tk.Tk()
root.title("Generatore di domande per siti web")
root.geometry('1000x1000+100+100')  # Imposta le dimensioni della finestra principale

style = ttk.Style()
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Arial', 14))
style.configure('TButton', font=('Arial', 14), padding=8)
style.configure('Custom.TEntry', font=('Arial', 14), padding=(10, 10, 10, 10))

frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0, sticky='nsew')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

url_label = ttk.Label(frame, text="Inserisci l'URL del sito web:")
url_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)

url_entry = ttk.Entry(frame, width=50, style='Custom.TEntry')
url_entry.grid(row=1, column=0, sticky='w', padx=10, pady=5)

button_frame = ttk.Frame(frame)
button_frame.grid(row=2, column=0, sticky='w', padx=10, pady=10)

submit_button = ttk.Button(button_frame, text="Analizza sito", command=on_submit)
submit_button.pack(side='left', padx=5)

sentiment_button = ttk.Button(button_frame, text="Analizza sentiment", command=on_sentiment)
sentiment_button.pack(side='left', padx=5)

social_button = ttk.Button(button_frame, text="Estrai social", command=on_social_links)
social_button.pack(side='left', padx=5)

chat_frame = ttk.Frame(frame)
chat_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
frame.rowconfigure(3, weight=1)

chat_text = scrolledtext.ScrolledText(chat_frame, width=60, height=20, wrap=tk.WORD, font=('Arial', 14))
chat_text.pack(expand=True, fill='both')

# Aggiunge tag per il testo dell'utente e del bot
chat_text.tag_configure('user', foreground='blue')
chat_text.tag_configure('bot', foreground='green')
chat_text.tag_configure('sentiment', foreground='purple')
chat_text.tag_configure('social', foreground='blue')

# Aggiunge il nuovo frame per i pulsanti delle domande predefinite
question_frame = ttk.Frame(frame)
question_frame.grid(row=4, column=0, sticky='w', padx=10, pady=10)

question_label = ttk.Label(frame, text="Fai una domanda:")
question_label.grid(row=5, column=0, sticky='w', padx=10, pady=10)

question_entry = ttk.Entry(frame, width=60, style='Custom.TEntry')
question_entry.grid(row=6, column=0, sticky='w', padx=10, pady=5)

ask_button = ttk.Button(frame, text="Chiedi", command=on_ask)
ask_button.grid(row=7, column=0, sticky='w', padx=10, pady=10)

# Variabili globali per tenere traccia delle conversazioni e del tipo di sito
messages = []
site_type_determined = False

root.mainloop()
