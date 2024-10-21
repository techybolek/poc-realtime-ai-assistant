import asyncio
import websockets

# Global variable to store the connected client
connected_client = None

async def init_ws_server():
    print("Initializing WebSocket server...")
    server = await websockets.serve(handle_client, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

async def handle_client(websocket, path):
    global connected_client
    print("Client connected")
    connected_client = websocket
    try:
        # Create a task to transmit the URL after 5 seconds
        #asyncio.create_task(delayed_transmit_url())
        # Keep the connection open
        await asyncio.Future()
    finally:
        connected_client = None
        print("Client disconnected")

async def delayed_transmit_url():
    await asyncio.sleep(5)
    await transmit_url_to_client("https://www.google.com")

async def transmit_url_to_client(url: str):
    global connected_client
    if connected_client:
        await connected_client.send(url)
        print(f"Transmitted URL to client: {url}")
    else:
        print("No client connected. Unable to transmit URL.")

# Run the WebSocket server
if __name__ == "__main__":
    asyncio.run(init_ws_server())
