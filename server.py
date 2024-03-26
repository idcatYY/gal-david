import asyncio
import websockets

# List to store connected clients
clients = set()

async def handle_client(websocket, path):
    # Add client to the set of clients
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            # Create a list of tasks for sending messages to clients
            tasks = [client.send(message) for client in clients]
            # Run the tasks concurrently
            await asyncio.gather(*tasks)
    finally:
        # Remove the client when the connection is closed
        clients.remove(websocket)

async def start_server():
    async with websockets.serve(handle_client, "localhost", 8080):
        print("Server started on ws://localhost:8080")
        await asyncio.Future()  # Run forever

asyncio.run(start_server())
