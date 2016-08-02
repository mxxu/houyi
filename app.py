import asyncio

async def handle(reader, writer):
    data = await reader.readline()
    if data == b"":
        print(reader, "EOF on request start")
        await writer.close()
        return

    data = data.decode()
    print(data)
    while True:
        data = await reader.readline()
        data = data.decode()
        print(data)
        if data == '\r\n':
            break

    writer.write("HTTP/1.1 200 NA\r\n".encode())
    writer.write("Content-Type: text/plain\r\n".encode())
    writer.write("\r\n".encode())
    writer.write("This is response body\r\n".encode())
    writer.write("This is response body line 2！！\r\n".encode())
    await writer.drain()
    writer.close()

loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(handle, '127.0.0.1', 8080))

loop.run_forever()

loop.close()
