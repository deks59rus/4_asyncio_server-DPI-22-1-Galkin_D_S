import asyncio

async def handle_echo(reader, writer):
    data = await reader.read(100)  # Читаем данные от клиента
    message = data.decode()  # Декодируем сообщение

    print(f'Received: {message}')  # Выводим полученное сообщение
    writer.write(data)  # Отправляем сообщение обратно клиенту
    await writer.drain()  # Ждем, пока данные будут отправлены

    writer.close()  # Закрываем соединение

async def main():
    HOST = '127.0.0.1'
    PORT = 8888
    server = await asyncio.start_server(handle_echo, HOST, PORT)

    addr = server.sockets[0].getsockname()  # Получаем адрес сервера
    print(f'Serving on {addr}')

    async with server:  # Асинхронный контекстный менеджер для сервера
        await server.serve_forever()  # Запускаем сервер

if __name__ == '__main__':
    asyncio.run(main())
