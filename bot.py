import logging
import time
import math
import os
import asyncio

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.constants import ChatAction
from telegram.ext import (Application, CommandHandler, MessageHandler, filters,
                          ConversationHandler, CallbackContext)

# --------------------------------------------
# ----------------- Constants ----------------
# --------------------------------------------

INITIAL_HELLO, COOORDINATES_TEST_MONONO, COORDINATES_TEST_CASITA, COORDINATES_TEST_AYTO = range(4)

LOCATIONS = [
    {"id": 1, "visited": False, "latlng": (40.171221, -3.901681)},  # Monono's house
    {"id": 2, "visited": False, "latlng": (40.170233, -3.899829)},  # Chuches
    {"id": 3, "visited": False, "latlng": (40.169760, -3.898916)},  # Ayuntamiento
]

PORT = int(os.environ.get("PORT", 8443))
TOKEN = os.environ["TOKEN"]

# --------------------------------------------
# ------------------ Logger ------------------
# --------------------------------------------

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# --------------------------------------------
# ------------------- Utils ------------------
# --------------------------------------------

async def real_writing(update: Update, messages) -> None:
    for message in messages:
        await update.effective_chat.send_action(action=ChatAction.TYPING)
        await asyncio.sleep(len(message) * 0.07)  # Simula la escritura
        await update.message.reply_text(message)

def location_inside_area(diameter: int, checkPoint, centerPoint) -> bool:
    km = diameter / 1000
    ky = 40000 / 360
    kx = math.cos(math.pi * centerPoint[0] / 180) * ky
    dx = math.fabs(centerPoint[1] - checkPoint[1]) * kx
    dy = math.fabs(centerPoint[0] - checkPoint[0]) * ky
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)) <= km

def process_location(update: Update) -> dict:
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude)
    tuple_checkpoint = (user_location.latitude, user_location.longitude)
    for location in LOCATIONS:
        if location_inside_area(25, tuple_checkpoint, location["latlng"]):
            logger.info("User location inside of %s", location["id"])
            location["visited"] = True
            return location
    return None
            
# --------------------------------------------
# ----------------- Handlers -----------------
# --------------------------------------------

async def start(update: Update, context: CallbackContext) -> int:

    messages = [
        'Hola '+update.message.from_user.first_name+'. ¡Felicidades! (Aunque realmente tu cumple fuese ayer)',
        'Te preguntarás quien soy... Bueno, es un secreto y solo te pido que confíes en mi y hagas lo que te diga. (Prometo que no será nada peligroso)',
        'El caso es que me han encargado que te guíe en un pequeño juego para mantenerte entretenida un ratito y que te diviertas',
        '¿Te apetece que empecemos?'
    ]

    await real_writing(update, messages)

    return INITIAL_HELLO

async def evaluate_ok(update: Update, context: CallbackContext) -> int:

    messages = [
        '¡Me gusta tu actitud!',
        'El juego es sencillo. Te voy a ir dando pistas para que vayas a determinados lugares y revivir algunos recuerdos de cosas que han pasado a lo largo de estos años',
        'Cuando estés en el lugar correcto, pulsa el botón de enviar ubicación para que pueda saber que has llegado',
        'Una vez que hayas visitado todos los lugares, ¡estarás preparada para descubrir la sorpresa final!',
        'Asi que... Sin más dilación, ¡Vamos a empezar!',
        'Aquí tienes la primera pista:',
        'En Septiembre la juerga empezaba\nCon rosa en el pecho, la fiesta estallaba\nBailes y copas, un gran festival\nAllí celebramos un rito anual\nSi el primer destino quieres hallar\nVe al lugar que hubo que limpiar'
    ]

    await real_writing(update, messages)

    return COOORDINATES_TEST_MONONO

async def evaluate_ko(update: Update, context: CallbackContext) -> int:

    messages = [
        'Bueno, aunque no te apetezca lo vamos a hacer igualmente así que...',
        'El juego es sencillo. Te voy a ir dando pistas para que vayas a determinados lugares y revivir algunos recuerdos de cosas que han pasado a lo largo de estos años',
        'Cuando estés en el lugar correcto, pulsa el botón de enviar ubicación para que pueda saber que has llegado',
        'Una vez que hayas visitado todos los lugares, ¡estarás preparada para descubrir la sorpresa final!',
        'Asi que... Sin más dilación, ¡Vamos a empezar!',
        'Aquí tienes la primera pista:',
        'En Septiembre la juerga empezaba\nCon rosa en el pecho, la fiesta estallaba\nBailes y copas, un gran festival\nAllí celebramos un rito anual\nSi el primer destino quieres hallar\nVe al lugar que hubo que limpiar'
    ]

    await real_writing(update, messages)

    return COOORDINATES_TEST_MONONO

async def monono_location(update: Update, context: CallbackContext) -> int:
    
    user = update.message.from_user
    location_selected = process_location(update)

    if location_selected != None and location_selected['id'] == 1:
        messages = [
            'Eso es... ¡Has encontrado el primer lugar!',
            'Seguro que te acuerdas de los buenos momentos que pasaste en esta casa. ¡Qué tiempos aquellos!',
            'Pero bueno, no te pongas nostálgica que todavía te quedan visitar algunos lugares',
            'Muy bien '+user.first_name+'... Ahora que has encontrado la casa de moñoño, te voy a dar la siguiente pista:',
            'Un punto de encuentro, un viejo ritual\nDonde las charlas eran lo habitual\nFrente al dulce que ya se esfumó\nQueda el asiento que todo esperó\nSi quieres seguir y no fracasar\nVe allí donde solíais quedar'
        ]

        await real_writing(update, messages)

        return COORDINATES_TEST_CASITA

    else:
        messages = [
            user.first_name+'Pues parece que no has encontrado el lugar correcto...',
            'Vuelve a intentarlo y si no lo encuentras, no te preocupes, tus amigos te ayudarán'
        ]

        await real_writing(update, messages)

        return COOORDINATES_TEST_MONONO

async def casita_location(update: Update, context: CallbackContext) -> int:

    user = update.message.from_user
    location_selected = process_location(update)

    if location_selected != None and location_selected['id'] == 2:
        messages = [
            '¡Bien hecho '+user.first_name+'!',
            'Has encontrado el segundo lugar',
            'Una pena que cerrasen la casita ¿verdad? Con la de chuches que has comprado allí...',
            'Aunque peor fue que pusieran el banco mirando a la pared... ¡Qué desastre!',
            'Hasta ahora lo estás haciendo genial, así que vamos a por el último lugar:',
            'Hubo campanas, hubo emoción\nUn día que hizo historia en la región\nDos almas unidas, un gran festival\nMedio pueblo vino, fue algo especial\nSi quieres saber dónde ocurrió\nBusca el rincón donde el amor triunfó.'
        ]

        await real_writing(update, messages)

        return COORDINATES_TEST_AYTO

    else:
        messages = [
            'Pues parece que no has encontrado el lugar correcto...',
            'Vuelve a intentarlo y si no lo encuentras, no te preocupes, tus amigos te ayudarán'
        ]

        await real_writing(update, messages)

        return COORDINATES_TEST_CASITA

async def ayto_location(update: Update, context: CallbackContext) -> int:

    user = update.message.from_user
    location_selected = process_location(update)

    if location_selected != None and location_selected['id'] == 3:
        
        messages = [
            '¡Enhorabuena '+user.first_name+'!',
            'Has encontrado el último lugar',
            '¡Qué recuerdos! ¿Te acuerdas de ese día? Eras bastante más pequeña que ahora...',
            'Es que treinta palos no se cumplen todos los días',
            'Y... aunque ya no estén, estoy convencido de que se sienten orgullosas de la persona en la que te has convertido',
            '¡Pero vamos a dejarnos de dramas! ¡Que todavía te queda la sorpresa final!',
            'Vuelve a casa y confía en tus amigos para que te guíen en el último paso',
            'Espero que te haya gustado el juego y que hayas disfrutado recordando esos momentos',
            '¡Hasta pronto!'
        ]

        await real_writing(update, messages)

        return ConversationHandler.END

    else:
        messages = [
            'Pues parece que no has encontrado el lugar correcto...',
            'Vuelve a intentarlo y si no lo encuentras, no te preocupes, tus amigos te ayudarán'
        ]

        await real_writing(update, messages)

        return COORDINATES_TEST_AYTO

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INITIAL_HELLO: [
                MessageHandler(filters.Regex("^(SI|Si|si)$"), evaluate_ok),
                MessageHandler(filters.Regex("^(NO|No|no)$"), evaluate_ko),
            ],
            COOORDINATES_TEST_MONONO: [MessageHandler(filters.LOCATION, monono_location)],
            COORDINATES_TEST_CASITA: [MessageHandler(filters.LOCATION, casita_location)],
            COORDINATES_TEST_AYTO: [MessageHandler(filters.LOCATION, ayto_location)],
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()