import asyncio
import pytz
from datetime import datetime
import telegram
from googleapiclient.discovery import build
import time
import logging
import os

# Configurar el nivel de registro del logger
logging.basicConfig(level=logging.DEBUG)

# DATOS GLOBALES
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.environ.get('DEVELOPER_KEY')
youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
# Token de acceso telegram
TOKEN = os.environ.get('TLG_TOKEN')
# Crea un objeto de tipo Bot
bot = telegram.Bot(token=TOKEN)
# Define el chat ID del user al que queres enviar el mensaje
chat_id = os.environ.get('CHAT_ID')
# Zona horaria
local_timezone = pytz.timezone('America/Buenos_Aires')
# Crear un objeto logger
logger = logging.getLogger('plm_logger')
# Configurar el nivel de registro
logger.setLevel(logging.INFO)
# Crear un objeto Formatter para personalizar el formato
formatter = logging.Formatter('[%(levelname)s] %(asctime)s PLM/(%(process)d:%(thread)d): %(message)s')
# Crear un objeto FileHandler para guardar los registros en un archivo
handler = logging.FileHandler('plm_bot.log')
handler.setFormatter(formatter)
# Agregar el controlador al logger
logger.addHandler(handler)
# Datos que quiero buscar
channel_name = 'Vorterix'
channel_id = 'UCvCTWHCbBC0b9UIeLeNs8ug'
video_text = '#ParenLaMano'
video_text2 = 'COMPLETO'
cfg_dir = 'plm_id.cfg'


def buscar_video(id_actual):
    playlist_response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()

    playlist_id = playlist_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    playlist_items_response = youtube.playlistItems().list(
        part='id,snippet',
        playlistId=playlist_id,
        maxResults=7
    ).execute()

    video_id = id_actual

    for playlist_item in playlist_items_response['items']:
        video_title = playlist_item['snippet']['title']
        if (video_text.lower() in video_title.lower()) and (video_text2.lower() in video_title.lower()):
            video_id = playlist_item['snippet']['resourceId']['videoId']
            break

    return video_id


def datos_video(id_video):
    video_result = youtube.videos().list(
        id=id_video,
        part='snippet'
    ).execute()

    video_title = video_result['items'][0]['snippet']['title']
    video_published_at = video_result['items'][0]['snippet']['publishedAt']
    # Convertir la fecha y hora de publicación a objeto datetime
    video_published_datetime = datetime.strptime(video_published_at, '%Y-%m-%dT%H:%M:%SZ')
    # Ajustar la zona horaria del objeto datetime a la zona horaria local
    video_published_local = video_published_datetime.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    # Extraer la fecha y hora local como cadenas de texto formateadas
    video_date = video_published_local.strftime('%d/%m/%Y')
    video_hour = video_published_local.strftime('%H:%M')
    video_url = 'https://www.youtube.com/watch?v=' + id_video

    datos_del_video = [video_title, video_date, video_hour, video_url]

    return datos_del_video


def leer_ultimo_id():
    # abrir el archivo de configuración en modo lectura
    with open('plm_id.cfg', 'r') as f:
        # leer el contenido del archivo
        ultimo_id = f.read().strip()
        # devolver el último id leído
        return ultimo_id


def escribir_ultimo_id(nuevo_id):
    # abrir el archivo de configuración en modo escritura
    with open(cfg_dir, 'w') as f:
        # escribir el nuevo id en el archivo
        f.write(nuevo_id)


async def enviar_mensaje(datos):
    # Define el mensaje que deseas enviar
    message = '🎥 Se encontró el video: ' + datos[0] + '\n📅 Fue subido el dia: ' + datos[1] + '\n🕘 A las: ' + datos[
        2] + '\n🔗 La URL es: ' + datos[3]

    # Envía el mensaje usando el método send_message()
    await bot.send_message(chat_id=chat_id, text=message)


async def main():
    while True:

        # me fijo que no sea fin de semana
        dia_actual = datetime.today().astimezone(local_timezone).weekday()
        if dia_actual == 5 or dia_actual == 6:
            if dia_actual == 5:
                logger.info('Es sábado hoy no se sube PLM')
            else:
                logger.info('Es domingo hoy no se sube PLM')

        #     break

         # Leo y almaceno último id de video
        id_actual = leer_ultimo_id()

        video_id = buscar_video(id_actual)
        datos = datos_video(video_id)

        fecha_actual = datetime.now().astimezone(local_timezone).strftime("%d/%m/%Y")
        hora_actual = datetime.now().astimezone(local_timezone).strftime('%H:%M')

        # me fijo si el id es nuevo
        if video_id != id_actual:
            await enviar_mensaje(datos)
            logger.info('Se encontro NUEVO video: ' + datos[0] + ', subido el dia: ' + datos[1] + ' a las: ' + datos[
                2] + ', la URL es: ' + datos[3] + ' y el id es: ' + video_id)
            escribir_ultimo_id(video_id)
            break
        else:
            if fecha_actual == datos[1] and datos[2] >= '03:00':
                logger.info('Ya se encontro el video de hoy')
                break
            else:
                # si ya son la 1 am corto el programa
                if hora_actual == '01':
                    logger.info('No se encontro programa nuevo')
                    break

        time.sleep(30)


asyncio.run(main())
