import json
import os
import pandas as pd
from google import genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración de Gemini
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCdtgsqzO9CaYqPSNiUDBMvgPePNQ-OomA")
client = genai.Client(api_key=API_KEY)

# Directorio donde están todos los CSV
BASE_DIR = os.path.dirname("C:\\Users\\javir\\OneDrive\\Escritorio\\ZARA\\boost-2025\\backend")
DATA_DIR = os.path.join(BASE_DIR, 'data')

def list_csv_files():
    """Retorna la lista de archivos CSV disponibles en el directorio data."""
    return [f for f in os.listdir(DATA_DIR) if f.lower().endswith('.csv')]

def build_context_from_csv(file_path: str, max_rows: int = 10) -> str:
    """
    Genera contexto legible para cualquier CSV:
    - Columnas y tipos
    - Primeras `max_rows` filas
    - Indicación de cuántas filas quedan ocultas
    """
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    # Columnas y tipos
    cols_info = "\\n".join(f"- {col}: {dtype.name}" for col, dtype in df.dtypes.items())
    # Ejemplos de filas
    sample = df.head(max_rows).to_dict(orient='records')
    sample_text = "\\n".join(" | ".join(f"{k}={v}" for k, v in row.items()) for row in sample)
    more = f"\\n... y {len(df)-max_rows} filas más ..." if len(df) > max_rows else ""
    return (
        f"CSV '{os.path.basename(file_path)}' con {len(df)} filas:\\n"
        f"Columnas y tipos:\\n{cols_info}\\n\\n"
        f"Primeras {min(len(df), max_rows)} filas:\\n{sample_text}{more}"
    )

def generate_gemini_prompt(data_description):
    """Generates a prompt for the Gemini API based on the desired data."""
    prompt = f"""
    You are an expert in data analysis and relationships between stores and warehouses.
    Based on the available data, provide information about stores, warehouses, and their connections.
    The response should be a JSON object with the following structure:

    {{
      "stores": [
        {{"id": "store_id_1"}},
        {{"id": "store_id_2"}},
        ...
      ],
      "warehouses": [
        {{"id": "warehouse_id_1"}},
        {{"id": "warehouse_id_2"}},
        ...
      ],
      "edges": [
        {{"source": "store_id_1", "target": "warehouse_id_1"}},
        {{"source": "store_id_2", "target": "warehouse_id_2"}},
        ...
      ]
    }}

    Analyze the data and identify the stores, warehouses, and their connections.
    Return ONLY the JSON. No other text.
    The json only, without not code quotes or any other text.
    The json mustnt be formatted, just the json.
    """
    return prompt

@app.route('/get_store_warehouse_data', methods=['GET'])
def get_store_warehouse_data():
    # Lista de CSV disponibles
    files = list_csv_files()
    print(DATA_DIR)
    selected = [os.path.join(DATA_DIR, f) for f in files]

    # Construye contexto concatenando cada CSV
    contexts = [build_context_from_csv(fp) for fp in selected]
    full_context = "\\n\\n".join(contexts)

    # Generate the prompt
    prompt = generate_gemini_prompt("store and warehouse data")

    # Create chat
    chat = client.chats.create(model="gemini-2.0-flash")

    # Send the prompt to Gemini
    response = chat.send_message(full_context + "\\n\\n" + prompt)

    try:
        # Parse the JSON response
        response_text = response.text
        response_text=response_text.replace("```json", '')
        response_text=response_text.replace("```", '')  # Replace single quotes with double quotes
        response_dict = json.loads(response_text)
        data = json.dumps(response_dict, indent=4)
        print(response.text)
        return data

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# endpoint con query params
@app.route('/consulta', methods=['GET'])
def consulta():
    param_value = request.args.get('query', default='default_value', type=str)
    return jsonify({"received_param": param_value}), 200


if __name__ == "__main__":
    app.run(debug=True)
