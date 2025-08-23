import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import time
from whatsapp_business_api_sdk import WhatsAppBusinessApi
import pathlib # <- Agrega esta línea

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configurar la API de OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_menu_from_json():
    """Carga el menú desde un archivo JSON."""
    try:
        current_dir = pathlib.Path(__file__).parent # <- Agrega esta línea
        with open(current_dir / 'menu.json', 'r', encoding='utf-8') as file: # <- Reemplaza la línea existente
            menu = json.load(file)
        return menu
    except Exception as e:
        print(f"Error al cargar el menú desde el archivo JSON: {e}")
        return None

# Cargar el menú al iniciar la aplicación
MENU = get_menu_from_json()

# Variable para mantener el historial de la conversación
if MENU:
    conversation_history = [
        {"role": "system", "content": "Eres una asistente de pedidos para un restaurante llamado La Central Bogotá. Tu nombre es Sofía y tienes acento paisa de Medellín. Usas un tono muy amable, cálido y servicial. Siempre respondes de manera natural y cercana, como si estuvieras hablando con un amigo. Tu objetivo es ayudar a los clientes a hacer su pedido, ofrecerles recomendaciones basadas en el menú y responder a sus preguntas. Cuando un cliente te pida el menú, en lugar de listarlo, envíale el siguiente enlace: https://drive.google.com/file/d/1rvMCav7g9ucUAQTj3uVUPN_FFzjkah4O/view?usp=sharing. Cuando el cliente confirme el pedido y te dé su información (nombre, teléfono, dirección y método de pago), generas una confirmación final con toda la información y la siguiente plantilla: '📦 ¡Gracias por pedir con La Central! Te compartimos nuestros medios de pago para domicilios: 💳 Llave Bancolombia (desde cualquier banco): 📧 isabellatineo0404@gmail.com 📱 Nequi o Daviplata: 📞 302 305 6171 👤 Titular: Isabella Tineo Arango 🆔 C.C. 1034294197 📍 Calle 170A #54C-28 – Bogotá 📲 Por favor, envíanos el comprobante aquí mismo 💬 🚨 Recuerda: La Central solo recibe pagos por estos canales. Evita estafas y apóyanos comprando directo 💛'. No te salgas de este rol. Los pagos en efectivo solo están disponibles si el cliente recoge el pedido en el local. Si el cliente pide un domicilio, solo puedes ofrecerle las opciones de pago digital. Todas tus recomendaciones deben ser de los elementos exactos que están en el menú, no inventes nombres de platos. El menú es: " + str(MENU) + " Los métodos de pago disponibles son: Efectivo (solo para recoger en el local), Tarjeta de crédito, Nequi y Daviplata."}
    ]
else:
    conversation_history = [
        {"role": "system", "content": "Lo siento, hubo un problema para cargar el menú. Por favor, inténtalo de nuevo más tarde."}
    ]

@app.route("/")
def home():
    """Ruta principal que renderiza la interfaz de chat."""
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """Ruta API para procesar los mensajes del cliente y generar respuestas de la IA."""
    user_message = request.json.get("message")
    
    # Agregar el mensaje del usuario al historial
    conversation_history.append({"role": "user", "content": user_message})

    try:
        # Enviar la conversación completa a la API de OpenAI (limitado a los últimos 10 mensajes)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history[-10:],
            temperature=0.7,
        )
        
        # Extraer el mensaje de la IA de la respuesta
        ai_message = response.choices[0].message.content
        
        # Agregar la respuesta de la IA al historial
        conversation_history.append({"role": "assistant", "content": ai_message})
        
        # Simular que el asistente está escribiendo
        time.sleep(1.5)

        # Devolver la respuesta al cliente
        return jsonify({"response": ai_message})

    except Exception as e:
        print(f"Error con la API de OpenAI: {e}")
        return jsonify({"response": "Lo siento, hubo un error. Por favor, inténtalo de nuevo más tarde."}), 500

if __name__ == "__main__":
    app.run(debug=True)
