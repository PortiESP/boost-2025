import csv
from google import genai

API_KEY = "AIzaSyCdtgsqzO9CaYqPSNiUDBMvgPePNQ-OomA"
client = genai.Client(api_key=API_KEY)
chat   = client.chats.create(model="gemini-2.0-flash")

def get_csv_data(file_path, condition=None):
    data = []
    # Usa utf-8-sig para eliminar BOM en la cabecera
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Ahora row['productId'] existe sin '\ufeff'
            row['total_demand'] = int(row['total_demand'])
            row['total_stock']  = float(row['total_stock'])
            row['gap']          = float(row['gap'])
            if condition is None or condition(row):
                data.append(row)
    return data

# Carga TODO el CSV
csv_file      = 'brecha_stock_vs_demanda.csv'
relevant_data = get_csv_data(csv_file)

# Construye un texto de contexto legible
context_lines = [
    f"• {r['productId']} | talla: {r['size']} | demanda: {r['total_demand']} "
    f"| stock: {r['total_stock']} | gap: {r['gap']}"
    for r in relevant_data
]
context_string = "Aquí tienes los datos de stock vs demanda:\n" + "\n".join(context_lines)

# Bucle interactivo
print("PREGÚNTAME LO QUE QUIERAS (o 'salir'):")
while True:
    pregunta = input("> ")
    if pregunta.strip().lower() in ('salir','exit','quit'):
        print("¡Hasta luego!")
        break

    # Prepara prompt con contexto + pregunta
    prompt = f"{context_string}\n\nPregunta: {pregunta}"

    # Envía a Gemini
    respuesta = chat.send_message(prompt)
    print("\n--- Gemini responde ---")
    print(respuesta.text)
    print("\n(Escribe otra pregunta o 'salir')\n")
