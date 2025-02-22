import os

from openai import OpenAI

open_ai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=open_ai_key)
model = "gpt-4o"


def summarize_info_sheet(logs):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Agisci come un assistente sociale e fai una relazione sulla base delle "
                        "informazioni ricevute. Assicurati che la risposta non sia in markdown ma "
                        "in un testo di piano organizzato in paragrafi"
                    ),
                },
                {"role": "user", "content": str(logs)},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Error generating summary."


def generate_report(logs):
    print("Inside generate_report")
    print("Logs received:", logs)  # Print the logs to see what we're sending
    try:
        print("OpenAI API Key:", client.api_key[:5] + "..." if client.api_key else "No API Key")  # Print first few chars of API key
        print("Using model:", model)
        
        messages = [
            {
                "role": "system",
                "content": (
                    "Scrivi una relazione su Operatore basata su alcune note e badgiature inserite "
                    "nel mansionario. Nella relazione, valuta la qualità della scrittura e se sono "
                    "stati rispettati gli orari di lavoro, senza soffermarti troppo sui dettagli "
                    "grammaticali o sugli errori specifici. Concentrati più sull'impressione generale "
                    "che si ricava dalle note, sia in termini di forma che di gestione del tempo. "
                    "Mantieni il tono professionale ma senza entrare in troppi dettagli tecnici."
                ),
            },
            {"role": "user", "content": str(logs)},
        ]
        print("Sending request to OpenAI with messages:", messages)
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        print("Received response from OpenAI:", response)
        return response.choices[0].message.content
    except Exception as e:
        print("Error generating report. Details:", str(e))
        print("Error type:", type(e).__name__)
        import traceback
        print("Full traceback:", traceback.format_exc())
        return f"Error generating report: {str(e)}"
