import asyncio
import ssl
import pathlib
import websockets

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.load_verify_locations(pathlib.Path(__file__).with_name('cert.pem'))

async def test_wss():
    try:
        # async with websockets.connect("wss://localhost:11181/ws/general",ssl=ssl_context) as websocket:
        async with websockets.connect("wss://192.168.3.19:11181/ws/general",ssl=ssl_context) as websocket:
            print("Connection established")
            # await websocket.send("Hello!")
            # response = await websocket.recv()
            # print("Response:", response)
    except Exception as e:
    # except try:
        print("Connection failed:", type(e), e)

asyncio.run(test_wss())