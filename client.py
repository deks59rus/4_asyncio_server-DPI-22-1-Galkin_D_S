import asyncio

async def main():
    HOST = '127.0.0.1'  # или 'localhost'
    PORT = 8888

    reader, writer = await asyncio.open_connection(HOST, PORT)

    print(f'Connected to server at {HOST}:{PORT}')

    while True:
        message = input("Введите сообщение (или 'exit' для выхода): ")
        if message.lower() == 'exit':
            break

        writer.write(message.encode())
        await writer.drain()

    print('Closing connection...')
    writer.close()
    await writer.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
