import asyncio
import os
import logging

# Настройка логирования
log_dir = 'log'
os.makedirs(log_dir, exist_ok=True)  # Создаем папку log, если не существует
logging.basicConfig(filename=os.path.join(log_dir, 'server.log'),
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

clients = set()  # Множество для хранения подключенных клиентов

async def notify_clients(message):
    """Отправляет сообщение всем клиентам."""
    for client in clients:
        client.write(message.encode())
        await client.drain()

async def handle_client(reader, writer):
    # Добавляем нового клиента в множество
    clients.add(writer)
    addr = writer.get_extra_info('peername')
    print(f'New connection from {addr}')

    # Уведомляем всех клиентов о новом подключении
    join_message = f"{addr} присоединился к чату."
    await notify_clients(join_message)

    try:
        while True:
            data = await reader.read(100)  # Читаем данные от клиента
            if not data:
                break  # Если нет данных, клиент отключился

            message = data.decode()  # Декодируем сообщение
            logging.info(f'Received from {addr}: {message}')  # Логируем полученное сообщение
            print(f'Received from {addr}: {message}')  # Выводим полученное сообщение

            # Отправляем сообщение всем клиентам, кроме отправителя
            await notify_clients(f"{addr}: {message}")

    except Exception as e:
        print(f'Error with client {addr}: {e}')
    finally:
        # Удаляем клиента из множества при отключении
        clients.remove(writer)
        print(f'Connection closed from {addr}')

        # Уведомляем всех клиентов об отключении
        leave_message = f"{addr} покинул чат."
        await notify_clients(leave_message)

        writer.close()  # Закрываем соединение
        await writer.wait_closed()  # Ждем закрытия соединения

async def main():
    HOST = '127.0.0.1'
    PORT = 8888
    server = await asyncio.start_server(handle_client, HOST, PORT)

    addr = server.sockets[0].getsockname()  # Получаем адрес сервера
    print(f'Serving on {addr}')

    async with server:  # Асинхронный контекстный менеджер для сервера
        await server.serve_forever()  # Запускаем сервер

if __name__ == '__main__':
    asyncio.run(main())  # Для Python 3.7 и выше
