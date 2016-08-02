import asyncio

routes = {}

class Request:
    meth = 'GET'
    path = '/'
    heads = {}
    body = ''

class Response:
    status_code = 200
    content_type = "text/plain"
    body = []

def default_handler(request):
    response = Response()
    response.status_code = 404
    return response

def hello_handler(request):
    response = Response()
    response.body.append("hello: Mike!\r\n")
    return response

def register_route(meth, path, handler):
    routes[(meth, path)] = handler

def get_handler(meth, path):
    return routes.get((meth, path), default_handler)

register_route("GET", "/hello", hello_handler)

async def handle(reader, writer):
    data = await reader.readline()
    if data == b"":
        print(reader, "EOF on request start")
        await writer.close()
        return

    data = data.decode()
    print(data)
    meth, path, version = data.split()

    request = Request()
    request.meth = meth
    request.path = path
    while True:
        data = await reader.readline()
        data = data.decode()
        print(data)
        if data == '\r\n':
            break

        key, value = data.rstrip().split(': ')
        request.heads[key] = value

    # writer.write("HTTP/1.1 200 NA\r\n".encode())
    # writer.write("Content-Type: text/plain\r\n".encode())
    # writer.write("\r\n".encode())
    # writer.write("This is response body\r\n".encode())
    # writer.write("This is response body line 2！！\r\n".encode())

    handler = get_handler(meth, path)
    response = handler(request)
    writer.write("HTTP/1.1 {code} NA\r\n".format(code=response.status_code).encode())
    writer.write("Content-Type: {tp}\r\n".format(tp=response.content_type).encode())
    writer.write("\r\n".encode())
    for s in response.body:
        writer.write(s.encode())
    await writer.drain()
    writer.close()

loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(handle, '127.0.0.1', 8080))

loop.run_forever()

loop.close()
