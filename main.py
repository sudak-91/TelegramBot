import webbrowser

import telebot
import cherrypy
import tweepy
from pip._vendor.distlib.compat import raw_input
import config
import DataBase
import requests
import threading

auth = tweepy.OAuthHandler(config.ApiKey, config.ApiSecret)
WEBHOOK_HOST = '18.188.44.19'
WEBHOOK_PORT = 88  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = '/telegram_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = '/telegram_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % config.Token

bot = telebot.TeleBot(config.Token)

class TestArduino(object):
        @cherrypy.expose
        def index(self):
            print("Достучалось")


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])

            return ''
        else:
            raise cherrypy.HTTPError(403)


if __name__ == '__main__':

    @bot.message_handler(commands=['command'])
    def new_command(message):
        bot.send_message(message.chat.id,"Укажите keyApi")
        bot.register_next_step_handler(message, new_command_key)

    def new_command_key(message):
        apiKey = message.text
        bot.send_message(message.chat.id, "Укажите порт управления")
        bot.register_next_step_handler(message, check_key_querry, apiKey)

    def check_key_querry(message, apiKey):
        key = message.text
        r = requests.post("http://18.188.44.19:9090/check_querry_length/", json={'apiKey': apiKey, 'key': message.text})
        bot.send_message(message.chat.id, r)
        if (r == 0):
            bot.send_message(message.chat.id, "Укажите состояние")
            bot.register_next_step_handler(message, post_comman_func, apiKey, key)
        else:
            bot.send_message(message.chat.id,"На указанный порт данного устройства уже есть комманда. Дождитесь ее выполнения")


    @bot.message_handler(commands=['register'])
    def register_device(message):
        bot.send_message(message.chat.id, "Укажите keyApi прибора")
        bot.register_next_step_handler(message, sendregdata)

    @bot.message_handler(commands=['signin'])
    def help_func(message):
        bot.send_message(message.chat.id, "Окееей. Давай сюда свой логин")
        #auth_url = auth.get_authorization_url()
        #bot.send_message(message.chat.id, auth_url)
        bot.register_next_step_handler(message, login_twitter)

    @bot.message_handler(commands=['show'])
    def help_func(message):
        try:
            con = DataBase.sql_connection()
            ghu = DataBase.sql_getRow(con)
            bot.send_message(message.chat.id, "yhhhh")
           ## requests.get("http://18.188.44.19:9090/?login=gghsdsa")


        except:
            bot.send_message(message.chat.id, "херня какая-то")
    @bot.message_handler(commands=['adddevice'])
    def adddev_func(message):
        bot.send_message(message.chat.id,"Ключ прибора")
        bot.register_next_step_handler(message, addkey_func)

    def addkey_func(message):
        apiKey = message.text
        bot.send_message(message.chat.id, "Ключ для учета")
        bot.register_next_step_handler(message, checkkey_func, apiKey)


    def checkkey_func(message, apiKey):
        key = message.text
        bot.send_message(message.chat.id, f"Код прибора {apiKey} а имя ключа {key}")
        r = requests.post("http://18.188.44.19:9090/postKey/", json={'apiKey':apiKey, 'key':key})



    def post_comman_func(message, apiKey, key):
        requests.post("http://18.188.44.19:9090/add_command/", json={'apiKey': apiKey, 'Key': key, 'value': message.text})

    def login_twitter(message):
        if(message.text == config.Login):
            bot.send_message(message.chat.id, "Окей. Теперь давай пароль")
            bot.register_next_step_handler(message, pass_twitter)
        else:
            bot.send_message(message.chat.id, "Не прокатило")


    def pass_twitter(message):
        if(message.text == config.Pass):
            bot.send_message(message.chat.id, "Пароль верен")
            auth_url = auth.get_authorization_url()
            bot.send_message(message.chat.id, auth_url)
            bot.register_next_step_handler(message, next_twitter_step)
        else:
            bot.send_message(message.chat.id, "Не угадал")


    def next_twitter_step(message):
        try:
            auth.get_access_token(message.text)
            con = DataBase.sql_connection()
            DataBase.create_twitter_table(con)
            entetys = (message.chat.id, auth.access_token, auth.access_token_secret)
            DataBase.sql_insert_twitter(con, entetys)
            con.close()

        except:
            print("Error")

        #auth.set_access_token(auth.access_token, auth.access_token_secret)
        api = tweepy.API(auth)
        try:
            api.verify_credentials()
            print("Authentication OK")
            bot.send_message(message.chat.id, "Zer gud")
            # api.update_status("Кажись я все сломал")
        except:
            print("Error during authentication")


    @bot.message_handler(content_types=['text'])
    def echo_message(message):
        bot.reply_to(message, message.text)
        print(message.text)
        entetys = (message.text, message.chat.id)
        con = DataBase.sql_connection()
        DataBase.sql_table(con)
        DataBase.sql_insert(con, entetys)
        con.close()




    def sendregdata(message):
        r = requests.post("http://18.188.44.19:9090/registeruser/", json={'apiKey': message.text, 'chatid': message.chat.id})
        bot.send_message(message.chat.id, r)



bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.tree.mount(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
cherrypy.tree.mount(TestArduino(), '/Temp/', {'/': {}})

cherrypy.engine.start()
cherrypy.engine.block()



