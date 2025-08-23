import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import time

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configurar la API de OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Aquí está tu menú en formato JSON, directamente en el código
MENU = {
  "Entradas": [
    {
      "nombre": "Tequeños x5",
      "descripcion": "Deditos de queso con salsa de la casa",
      "precio": 17500
    },
    {
      "nombre": "Tequeños x7",
      "descripcion": "Deditos de queso con salsa de la casa",
      "precio": 22700
    },
    {
      "nombre": "Tiradito de Salmón",
      "descripcion": "Láminas de salmón en leche de tigre con plátano, aguacate y totopos",
      "precio": 34000
    },
    {
      "nombre": "Ceviche Peruano",
      "descripcion": "Camarones y pescado blanco en leche de tigre con maíz, aguacate y verduras",
      "precio": 34000,
      "variantes": ["Camarón", "Vegetales"]
    },
    {
      "nombre": "Gyozas x6",
      "descripcion": "Masa rellena salteada en ajonjoli",
      "precio": 22500,
      "variantes": ["Cerdo"]
    },
    {
      "nombre": "Gyozas x9",
      "descripcion": "Masa rellena salteada en ajonjoli",
      "precio": 29400,
      "variantes": ["Camarón", "Vegetales", "Cerdo"]
    },
    {
      "nombre": "Mini empanadas x3",
      "descripcion": "Empanadas pequeñas con relleno a elección",
      "precio": 7500,
      "variantes": ["Ranchera", "Carne", "Pollo"]
    },
    {
      "nombre": "Mini empanadas x5",
      "descripcion": "Empanadas pequeñas con relleno a elección",
      "precio": 11500,
      "variantes": ["Ranchera", "Carne", "Pollo"]
    },
    {
      "nombre": "Mini empanadas x7",
      "descripcion": "Empanadas pequeñas con relleno a elección",
      "precio": 15500,
      "variantes": ["Ranchera", "Carne", "Pollo"]
    },
    {
      "nombre": "Nori Taco",
      "descripcion": "Nori con arroz de sushi y proteina a elección",
      "precio": 35000,
      "variantes": ["Salmón curado", "Atún"]
    },
    {
      "nombre": "Edamames",
      "descripcion": "Vainas de soya salteadas",
      "precio": 28000
    },
    {
      "nombre": "Sprint Rolls",
      "descripcion": "Rollos de vegetales salteados",
      "precio": 30000
    }
  ],
  "Sushi Rolls": [
    {
      "nombre": "Veggie",
      "descripcion": "Vegetales tempura, aguacate, plátano maduro, queso Philadelphia",
      "precio": 25100
    },
    {
      "nombre": "Dani Roll 2023",
      "descripcion": "Palmito de cangrejo, salsa dinamita, mango, queso Philadelphia, masago arare, langostino",
      "precio": 39100
    },
    {
      "nombre": "Spicy Tuna",
      "descripcion": "Atún, queso Philadelphia, aguacate, langostino tempura, toque picante",
      "precio": 31900
    },
    {
      "nombre": "Hiroshima",
      "descripcion": "Pescado blanco, queso Philadelphia, langostino tempura, topping aguacate",
      "precio": 30800
    },
    {
      "nombre": "Calimeño Roll",
      "descripcion": "Tartar de salmón, chips crocante, aguacate, plátano, salsa teriyaki flameada",
      "precio": 29100
    },
    {
      "nombre": "Acevichado",
      "descripcion": "Langostino, tempura mix, tilapia, cebolla roja, ajo, salsa rocoto, plátano verde",
      "precio": 33100
    },
    {
      "nombre": "Fantástico",
      "descripcion": "Langostino, tempura mix, queso Philadelphia, tartar de salmón, salsas teriyaki y dinamita dulce",
      "precio": 35100
    },
    {
      "nombre": "Furay Frosty",
      "descripcion": "Langostino, palmito de cangrejo, salsa dinamita dulce, salsa Ho Chu Han, aguacate",
      "precio": 33100
    },
    {
      "nombre": "Monster",
      "descripcion": "Pescado blanco crujiente, aguacate, palmito de cangrejo, salsa dinamita, cebollin",
      "precio": 28100
    },
    {
      "nombre": "Ebi Crunch",
      "descripcion": "Langostino crispy, aguacate, mayonesa",
      "precio": 28100
    },
    {
      "nombre": "Golden Filadelfia",
      "descripcion": "Salmón curado, aguacate, queso Philadelphia",
      "precio": 32800
    },
    {
      "nombre": "Volcano Roll",
      "descripcion": "Langostino tempura, queso mozzarella, tartar de salmón en salsa dinamita",
      "precio": 31900
    },
    {
      "nombre": "Honey Lemon Spicy",
      "descripcion": "Langostino crispy, aguacate, queso Philadelphia, salmón curado, limón, miel picante",
      "precio": 39900
    },
    {
      "nombre": "Isa Roll 2022",
      "descripcion": "Langostino, queso Philadelphia, salmón fresco, chips crocantes, salsa de maracuyá",
      "precio": 39100
    },
    {
      "nombre": "Noah Roll 2024",
      "descripcion": "Kanikama, aguacate, vegetales tempura, queso Philadelphia, salmón flameado, uchuva",
      "precio": 39100
    },
    {
      "nombre": "Filadelfia Tradicional",
      "descripcion": "Salmón curado, aguacate, queso Philadelphia",
      "precio": 29200
    },
    {
      "nombre": "Rainbow",
      "descripcion": "Kanikama, aguacate, pepino, topping de atún, salmón, pescado blanco",
      "precio": 31900
    },
    {
      "nombre": "Salmon Skin",
      "descripcion": "Piel de salmón, aguacate, queso Philadelphia, masago, ajonjoli",
      "precio": 25100
    },
    {
      "nombre": "Ojo de Tigre",
      "descripcion": "Salmón, aguacate, atún, kanikama, masago, salsa dinamita",
      "precio": 40200
    },
    {
      "nombre": "California Roll",
      "descripcion": "Kanikama, pepino, aguacate, masago, ajonjoli",
      "precio": 25100
    },
    {
      "nombre": "Avocado Roll",
      "descripcion": "Langostino tempura, aguacate fresco",
      "precio": 25100
    }
  ],
  "All You Can Eat": [
    {
      "nombre": "Samurai",
      "descripcion": "Langostino crispy, aguacate, queso Philadelphia, salmón curado, salsa dinamita",
      "precio": 35500,
      "notas": "Solo consumo en mesa"
    },
    {
      "nombre": "Tentación",
      "descripcion": "Salmón crispy, aguacate, plátano maduro, queso Philadelphia, palmito de cangrejo, salsa tentación",
      "precio": 31900,
      "notas": "Solo consumo en mesa"
    },
    {
      "nombre": "Sensación",
      "descripcion": "Salmón, queso Philadelphia, plátano, queso flameado",
      "precio": 31900,
      "notas": "Solo consumo en mesa"
    },
    {
      "nombre": "Tsunami",
      "descripcion": "Salmón curado, aguacate, masago, topping de sriracha",
      "precio": 31900,
      "notas": "Solo consumo en mesa"
    },
    {
      "nombre": "Mango Roll",
      "descripcion": "Salmón, queso Philadelphia, mango, salsa de jengibre",
      "precio": 31900,
      "notas": "Solo consumo en mesa"
    },
    {
      "nombre": "Kany Roll",
      "descripcion": "Palmito de cangrejo, queso Philadelphia, mango, salsa cítrica",
      "precio": 31900,
      "notas": "Solo consumo en mesa"
    },
    {
      "nombre": "Combo Clásico",
      "descripcion": "5 bocados Kany Roll, 5 Mango Roll, 5 Filadelfia Tradicional, 5 Veggie",
      "precio": 40900,
      "notas": "Solo consumo en mesa"
    },
    {
      "nombre": "Combo Especial",
      "descripcion": "5 bocados Dani Roll, 5 Tentación, 5 Sensación, 5 Monster, 5 Honey Lemon Spicy",
      "precio": 75900,
      "notas": "Solo consumo en mesa"
    }
  ],
  "Hamburguesas": [
    {
      "nombre": "Veggie Lenteja",
      "descripcion": "Pan brioche, proteína de lenteja, cebolla caramelizada, salsa pesto, vegetales rostizados",
      "precio": 19900
    },
    {
      "nombre": "La Oculta",
      "descripcion": "Carne res madurada, pulled pork, chicharrón ahumado, mozzarella, cheddar, cebolla caramelizada, papas chips",
      "precio": 49500
    },
    {
      "nombre": "Bacon",
      "descripcion": "Carne res madurada, mozzarella, doble tocineta, cogollo, cebolla, tomate, salsas",
      "precio": 30200
    },
    {
      "nombre": "Maracucha",
      "descripcion": "Carne res madurada, mozzarella, tocineta, plátano maduro, cogollo, cebolla, tomate, salsa de la casa",
      "precio": 29500
    },
    {
      "nombre": "CrackChicken",
      "descripcion": "Pechuga pollo apanada en panko, ensalada de col, salsa HOT BBQ",
      "precio": 28800
    },
    {
      "nombre": "Criolla",
      "descripcion": "Carne res madurada, mozzarella, huevo frito, cogollo, hogao",
      "precio": 29500
    },
    {
      "nombre": "Bañada en queso",
      "descripcion": "Carne res madurada, fondue de la casa, cogollo, cebolla, tomate, salsas",
      "precio": 32600
    },
    {
      "nombre": "Hamburguesa Clásica",
      "descripcion": "Carne res madurada, cogollo, cebolla, tomate, salsas",
      "precio": 26300
    },
    {
      "nombre": "Mexicana",
      "descripcion": "Carne res madurada, pico de gallo, guacamole, salsa picante, totopos",
      "precio": 27400
    },
    {
      "nombre": "Smash Doble",
      "descripcion": "Doble carne res madurada, doble tocineta, cogollo, cebolla, tomate, salsas",
      "precio": 40500
    },
    {
      "nombre": "Smash",
      "descripcion": "Carne res madurada, cebolla caramelizada, tocineta, pepinillo, queso amarillo",
      "precio": 26400
    }
  ],
  "Perros Calientes": [
    {
      "nombre": "Perro Mexicano",
      "descripcion": "Pan brioche, salchicha tradicional, guacamole, pico de gallo, salsa picante, totopos",
      "precio": 18200
    },
    {
      "nombre": "Perra",
      "descripcion": "Pan brioche, tocineta, ensalada de repollo, queso mozzarella",
      "precio": 18200
    },
    {
      "nombre": "Perro Americano",
      "descripcion": "Pan brioche, salchicha tradicional, tocineta ahumada, mozzarella, pepinillo, cebolla caramelizada, papa chamizo, salsa BBQ, mostaza",
      "precio": 23400
    },
    {
      "nombre": "Perro Granjero",
      "descripcion": "Pan brioche, salchicha tradicional, papa chamizo, maíz tierno, tocineta",
      "precio": 18200
    },
    {
      "nombre": "Perro Centralísimo",
      "descripcion": "Pan brioche, salchicha tradicional, papa chamizo, pulled pork, queso amarillo",
      "precio": 23400
    },
    {
      "nombre": "Perro Clásico",
      "descripcion": "Pan brioche, salchicha tradicional, salsas, papa chamizo, mozzarella",
      "precio": 15500
    }
  ],
  "Pepitos": [
    {
      "nombre": "Pepito Carne",
      "descripcion": "Pan de pepito, carne de res, maíz tierno, lechuga, tomate, salsas de la casa",
      "precio": 35900,
      "variantes": ["Entero"]
    },
    {
      "nombre": "Medio Pepito Carne",
      "descripcion": "Pan de pepito, carne de res, maíz tierno, lechuga, tomate, salsas de la casa",
      "precio": 19000,
      "variantes": ["Medio"]
    },
    {
      "nombre": "Pepito Pollo",
      "descripcion": "Pan de pepito, pechuga de pollo, maiz tierno, lechuga, tomate, salsas de la casa",
      "precio": 31900,
      "variantes": ["Entero"]
    },
    {
      "nombre": "Medio Pepito Pollo",
      "descripcion": "Pan de pepito, pechuga de pollo, maiz tierno, lechuga, tomate, salsas de la casa",
      "precio": 18000,
      "variantes": ["Medio"]
    },
    {
      "nombre": "Pepito Mixto",
      "descripcion": "Pan de pepito, carne mixta, maiz tierno, lechuga, tomate, salsas de la casa",
      "precio": 38900,
      "variantes": ["Entero"]
    },
    {
      "nombre": "Medio Pepito Mixto",
      "descripcion": "Pan de pepito, carne mixta, maíz tierno, lechuga, tomate, salsas de la casa",
      "precio": 20000,
      "variantes": ["Medio"]
    },
    {
      "nombre": "Cerdísimo",
      "descripcion": "Pan de pepito, pulled pork, chicharrón carnudo",
      "precio": 39600
    }
  ],
  "Arepas": [
    {
      "nombre": "Arepa Mixta",
      "descripcion": "Carne mechada, pollo mechado, pico de gallo, queso",
      "precio": 18500,
      "variantes": ["Harina pan", "Maíz peto"]
    },
    {
      "nombre": "Arepa Mantequilla",
      "descripcion": "Arepa sencilla con mantequilla",
      "precio": 3300,
      "variantes": ["Harina pan", "Maíz peto"]
    },
    {
      "nombre": "Arepa Jamón y Queso",
      "descripcion": "Arepa con jamón y queso",
      "precio": 6500,
      "variantes": ["Harina pan", "Maíz peto"]
    },
    {
      "nombre": "Arepa Carne Mechada",
      "descripcion": "Arepa rellena de carne mechada",
      "precio": 13800,
      "variantes": ["Harina pan", "Maíz peto"]
    },
    {
      "nombre": "Arepa Pollo Mechado",
      "descripcion": "Arepa rellena de pollo mechado",
      "precio": 10100,
      "variantes": ["Harina pan", "Maíz peto"]
    },
    {
      "nombre": "Arepa Reina Pepiada",
      "descripcion": "Pollo mechado, aguacate, queso",
      "precio": 16800,
      "variantes": ["Harina pan", "Maíz peto"]
    },
    {
      "nombre": "Arepa Pabellón",
      "descripcion": "Frijol negro, carne mechada, plátano maduro, queso costeño",
      "precio": 16800,
      "variantes": ["Harina pan", "Maíz peto"]
    }
  ],
  "Adiciones": [
    {
      "nombre": "Papa Francesa",
      "descripcion": "Papas fritas clásicas",
      "precio": 7000
    },
    {
      "nombre": "Carne de Hamburguesa",
      "descripcion": "Porción adicional de carne para hamburguesa",
      "precio": 15000
    },
    {
      "nombre": "Baño en Queso Cheddar",
      "descripcion": "Salsa de queso cheddar para bañar",
      "precio": 12000
    },
    {
      "nombre": "Pulled Pork",
      "descripcion": "Cerdo desmechado ahumado",
      "precio": 12000
    },
    {
      "nombre": "Carne Mechada",
      "descripcion": "Porción de carne mechada",
      "precio": 12000
    },
    {
      "nombre": "Pollo Mechado",
      "descripcion": "Porción de pollo mechado",
      "precio": 12000
    },
    {
      "nombre": "Porción de Arroz",
      "descripcion": "Arroz blanco sencillo",
      "precio": 5000
    },
    {
      "nombre": "Carne Mechada (otra presentación)",
      "descripcion": "Porción extra de carne mechada",
      "precio": 13000
    }
  ],
  "Bebidas Gaseos": [
    {
      "nombre": "Coca-Cola",
      "descripcion": "Botella plástica",
      "precio": 4400
    },
    {
      "nombre": "Coca-Cola en lata",
      "descripcion": "Presentación en lata",
      "precio": 6800
    },
    {
      "nombre": "Coca-Cola Zero",
      "descripcion": "Botella plástica",
      "precio": 4400
    },
    {
      "nombre": "Sprite",
      "descripcion": "Botella plástica",
      "precio": 4400
    },
    {
      "nombre": "Quatro",
      "descripcion": "Botella plástica",
      "precio": 4400
    },
    {
      "nombre": "Ginger",
      "descripcion": "Botella plástica",
      "precio": 4400
    },
    {
      "nombre": "Agua Manantial",
      "descripcion": "Botella plástica",
      "precio": 4400
    },
    {
      "nombre": "Agua con Gas",
      "descripcion": "Botella plástica",
      "precio": 4400
    },
    {
      "nombre": "Soda Hatsu",
      "descripcion": "Soda de la marca Hatsu",
      "precio": 4400
    }
  ],
  "Limonadas y Jugos": [
    {
      "nombre": "Jugos Naturales en Agua",
      "descripcion": "Jugos de frutas naturales preparados en agua",
      "precio": 8000
    },
    {
      "nombre": "Limonada Natural",
      "descripcion": "Limonada tradicional",
      "precio": 7200
    },
    {
      "nombre": "Limonada de Coco",
      "descripcion": "Limonada con leche de coco",
      "precio": 9900
    },
    {
      "nombre": "Cerezada",
      "descripcion": "Limonada sabor cereza",
      "precio": 9900
    },
    {
      "nombre": "Limonada Mango Biche",
      "descripcion": "Limonada con mango verde",
      "precio": 9900
    }
  ],
  "Cervezas": [
    {
      "nombre": "Miller Lite",
      "descripcion": "Cerveza Miller Lite",
      "precio": 8100
    },
    {
      "nombre": "Sol",
      "descripcion": "Cerveza Sol",
      "precio": 8100
    },
    {
      "nombre": "3 Cordilleras",
      "descripcion": "Cerveza 3 Cordilleras",
      "precio": 13100
    },
    {
      "nombre": "Heineken",
      "descripcion": "Cerveza Heineken",
      "precio": 12100
    }
  ],
  "Cocteles": [
    {
      "nombre": "Margarita Tradicional",
      "descripcion": "Tequila, licor de naranja, limón",
      "precio": 27000
    },
    {
      "nombre": "Margarita de Frutos Rojos",
      "descripcion": "Tequila, licor de naranja, limón, frutos rojos",
      "precio": 27000
    },
    {
      "nombre": "Margarita Mango Biche",
      "descripcion": "Tequila, licor de naranja, limón, mango biche",
      "precio": 27000
    },
    {
      "nombre": "Paloma",
      "descripcion": "Tequila, limón, soda de toronja",
      "precio": 27000
    },
    {
      "nombre": "Mojito Tradicional",
      "descripcion": "Ron blanco, limón, gaseosa, hierbabuena",
      "precio": 27000
    },
    {
      "nombre": "Mojito de Frutos Rojos",
      "descripcion": "Ron blanco, limón, hierbabuena, frutos rojos",
      "precio": 27000
    },
    {
      "nombre": "Mojito de Maracuyá",
      "descripcion": "Ron blanco, limón, maracuyá, gaseosa, hierbabuena",
      "precio": 27000
    },
    {
      "nombre": "Daiquiri Tradicional",
      "descripcion": "Ron blanco, limón, triple sec",
      "precio": 27000
    },
    {
      "nombre": "Tinto de Verano",
      "descripcion": "Vino tinto, limón, gaseosa, jarabe natural",
      "precio": 27000
    },
    {
      "nombre": "Gin Tonic Tradicional",
      "descripcion": "Ginebra, tónica, triple sec",
      "precio": 27000
    },
    {
      "nombre": "Gin Tonic de Frutos Rojos",
      "descripcion": "Ginebra, tónica, frutos rojos",
      "precio": 27000
    },
    {
      "nombre": "Gin Tonic Frutos Amarillos",
      "descripcion": "Ginebra, tónica, frutos amarillos",
      "precio": 27000
    },
    {
      "nombre": "Cosmopolitan",
      "descripcion": "Vodka, limón, granadina, licor de naranja",
      "precio": 27000
    },
    {
      "nombre": "Daiquiri Frutos Rojos",
      "descripcion": "Ron blanco, frutos rojos, triple sec",
      "precio": 27000
    },
    {
      "nombre": "Tequila Sunrise",
      "descripcion": "Tequila, granadina, jugo de naranja",
      "precio": 27000
    },
    {
      "nombre": "Chernobil",
      "descripcion": "Cuatro licores, granadina, jugo de naranja",
      "precio": 35000
    }
  ],
  "Mocteles": [
    {
      "nombre": "Michelada Sandía",
      "descripcion": "Limón, hierbabuena, jugo de cereza, soda Hatsu de sandía",
      "precio": 15000
    },
    {
      "nombre": "Raspberry Cherry",
      "descripcion": "Cerezas, granadina, soda Hatsu de frambuesa y fresa",
      "precio": 15000
    },
    {
      "nombre": "Mint Lemonade",
      "descripcion": "Limón, hierbabuena, soda Hatsu de limón hierbabuena",
      "precio": 15000
    }
  ],
  "Combo Master": [
    {
      "nombre": "Combo Master",
      "descripcion": "5 bocados Isa Roll, 5 bocados Dani Roll, 5 bocados Noah Roll",
      "precio": 53000
    }
  ],
  "Combo Clásico": [
    {
      "nombre": "Combo Clásico",
      "descripcion": "5 bocados Kany Roll, 5 Mango Roll, 5 Filadelfia Tradicional, 5 Veggie",
      "precio": 40900
    }
  ],
  "Combo Especial": [
    {
      "nombre": "Combo Especial",
      "descripcion": "5 bocados Dani Roll, 5 Tentación, 5 Sensación, 5 Monster, 5 Honey Lemon Spicy",
      "precio": 75900
    }
  ]
}

# Variable para mantener el historial de la conversación
conversation_history = [
    {"role": "system", "content": "Eres una asistente de pedidos para un restaurante llamado La Central Bogotá. Tu nombre es Sofía y tienes acento paisa de Medellín. Usas un tono muy amable, cálido y servicial. Siempre respondes de manera natural y cercana, como si estuvieras hablando con un amigo. Tu objetivo es ayudar a los clientes a hacer su pedido, ofrecerles recomendaciones basadas en el menú y responder a sus preguntas. Cuando un cliente te pida el menú, en lugar de listarlo, envíale el siguiente enlace: https://drive.google.com/file/d/1rvMCav7g9ucUAQTj3uVUPN_FFzjkah4O/view?usp=sharing. Cuando el cliente confirme el pedido y te dé su información (nombre, teléfono, dirección y método de pago), generas una confirmación final con toda la información y la siguiente plantilla: '📦 ¡Gracias por pedir con La Central! Te compartimos nuestros medios de pago para domicilios: 💳 Llave Bancolombia (desde cualquier banco): 📧 isabellatineo0404@gmail.com 📱 Nequi o Daviplata: 📞 302 305 6171 👤 Titular: Isabella Tineo Arango 🆔 C.C. 1034294197 📍 Calle 170A #54C-28 – Bogotá 📲 Por favor, envíanos el comprobante aquí mismo 💬 🚨 Recuerda: La Central solo recibe pagos por estos canales. Evita estafas y apóyanos comprando directo 💛'. No te salgas de este rol. Los pagos en efectivo solo están disponibles si el cliente recoge el pedido en el local. Si el cliente pide un domicilio, solo puedes ofrecerle las opciones de pago digital. Todas tus recomendaciones deben ser de los elementos exactos que están en el menú, no inventes nombres de platos. El menú es: " + str(MENU) + " Los métodos de pago disponibles son: Efectivo (solo para recoger en el local), Tarjeta de crédito, Nequi y Daviplata."}
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
