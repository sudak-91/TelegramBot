import random
import socket
import DataBase
import tweepy




class TCP_Server:
    api = ""

    def start_server(self, auth):
        sock = socket.socket()
        sock.bind(('', 9090))
        sock.listen(1)
        conn, addr = sock.accept()

        try:
            con = DataBase.sql_connection()
        except:
            print("no connect")
        try:
            token, secret = DataBase.sql_getTwitterKey(con)
            con.close()
        except:
            print("No data from db")
        try:
            auth.set_access_token(token, secret)
            self.api = tweepy.API(auth)
        except:
            print("TCP_server error connect")


        try:
            self.api.verify_credentials()
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
                self.api.update_status(DataBase.sql_select(con, k))
                con.close()
            except:
                print("что-то пошло не так" + k)
            try:
                conn.send(str(k).encode('ascii'))
            except:
                print("Ошибка" + k)
        conn.close()