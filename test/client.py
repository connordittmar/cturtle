from Cturtle import ClientHandler

def main():
    url = 'http://127.0.0.1:8000'
    client = ClientHandler(url)
    while True:
        client.nav_loop()

if __name__ == '__main__':
    main()
