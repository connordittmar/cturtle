from Cturtle import ClientHandler

def main():
    heading_desired = raw_input('Set Heading>>> ')
    url = 'http://127.0.0.1:8000'
    client = ClientHandler(url)
    heading_desired = float(heading_desired)
    counter = 0
    while True:
        client.heading_demo(heading_desired)
        if counter % 1000 == 0:
            heading_desired - 180
            if heading_desired < 0:
                heading_desired += 90
        counter += 1

if __name__ == '__main__':
    main()
