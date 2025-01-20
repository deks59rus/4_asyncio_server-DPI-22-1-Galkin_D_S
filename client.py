import asyncio


async def tcp_echo_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)

    message = 'Hello, world'
    print(f'Sending: {message}')

    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()}')

    writer.close()
    await writer.wait_closed()


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 8888


    asyncio.run(tcp_echo_client(HOST, PORT))
