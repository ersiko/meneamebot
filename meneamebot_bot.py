import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space, include_callback_query_chat_id
import sys
import shelve

BOT_TOKEN = sys.argv[1]


class MeneameBot(telepot.helper.ChatHandler):
    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
            if msg['text'] == '/start':
                message = """
¡Hola!\nEste bot te reenviará las noticias que aparezcan en portada de menéame e irá actualizando el número de comentarios, clicks, negativos, etc
Puedes hacer dos cosas con él: suscribirte (/subscribe) y des-suscribirte (/unsubscribe). Solo cuando estés suscrito recibirás mensajes nuevos.

Todo es código abierto, ya que es una prueba de concepto sobre los bots de telegram y python.
Si quieres ver el código está en https://github.com/ersiko/meneamebot
Muchas gracias por tu interés!
"""
                self.sender.sendMessage(message)
            if msg['text'] == '/subscribe':
                data = shelve.open("meneamebot_data", writeback=True)
                if msg['from']['id'] not in data['subscribed_users']:
                    data['subscribed_users'].append(msg['from']['id'])
                    self.sender.sendMessage("¡Te suscribiste a la portada de meneame! Ahora recibirás los nuevos envíos que lleguen a portada.")
                else:
                    self.sender.sendMessage("¡Ya estás suscrito! ¿Acaso quieres recibir los mensajes por duplicado?")
                data.close()
            if msg['text'] == '/unsubscribe':
                data = shelve.open("meneamebot_data", writeback=True)
                if msg['from']['id'] in data['subscribed_users']:
                    data['subscribed_users'].remove(msg['from']['id'])
                    self.sender.sendMessage("Te acabas de des-suscribir, así que ya no recibirás más mensajes nuevos por mi parte.")
                else:
                    self.sender.sendMessage("Si no estás suscrito... ¿Por qué quieres des-suscribirte?")
                data.close()


bot = telepot.DelegatorBot(BOT_TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(), create_open, MeneameBot, timeout=15
    ),
])

bot.message_loop(run_forever='Listening ...')
