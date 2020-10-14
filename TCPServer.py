import random
import socket
import DataBase
import tweepy
import config


auth = tweepy.OAuthHandler(config.ApiKey, config.ApiSecret)

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

try:
     con = DataBase.sql_connection()
except:
     print("no connect")
try:
    id, token, secret = DataBase.sql_getTwitterKey(con)
    con.close()
except:
    print("No data from db")
try:
    auth.set_access_token(token, secret)
    api = tweepy.API(auth)
except:
    print("TCP_server error connect")


try:
    api.verify_credentials()
    print("Twitter connected")
except:
    print("Twitter connecting error")


while True:
    data = conn.recv(1024)
    con = DataBase.sql_connection()
    if not data:
        break
    print(data)
    max = DataBase.sql_getRow(con)

    k = random.randint(1, max)
    print (k)
    try:
        twit = DataBase.sql_select(con, (k))
        print (twit)
        api.update_status(twit)

    except:
        print("что-то пошло не так" + k)
    try:
        conn.send(str(k).encode('ascii'))
    except:
        print("Ошибка" + k)
conn.close()


