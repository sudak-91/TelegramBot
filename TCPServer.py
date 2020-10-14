import random
import socket
import DataBase
import tweepy



api =""
class TCP_Server:


    def start_server(auth):
        sock = socket.socket()
        sock.bind(('', 9090))
        sock.listen(1)
        conn, addr = sock.accept()

        try:
            con = DataBase.sql_connection()
            token, secret = DataBase.sql_getTwitterKey(con)
            con.close()
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
            if not data:
                break
            print(data)
            con = DataBase.sql_connection()
            max = DataBase.sql_getRow(con)

            k = random.randint(0, max)
            try:
                api.update_status(DataBase.sql_select(con, k))
                con.close()
            except:
                print("что-то пошло не так" + k)
            try:
                conn.send(str(k).encode('ascii'))
            except:
                print("Ошибка" + k)
        conn.close()