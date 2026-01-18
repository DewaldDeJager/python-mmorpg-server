import asyncio
import websockets
import json

async def test_connection():
    uri = "ws://localhost:9001/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to server")
            
            # Send a test message
            test_msg = {"type": "ping"}
            await websocket.send(json.dumps(test_msg))
            print(f"Sent: {test_msg}")
            
            # Since the server doesn't have Player logic yet, it won't echo back
            # but we can check if it stays open or closes
            try:
                # Wait a bit to see if we get disconnected for some reason
                await asyncio.wait_for(websocket.recv(), timeout=2.0)
            except asyncio.TimeoutError:
                print("No message received (expected since Player logic is missing)")
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed by server: {e.code} {e.reason}")
                
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    # This test expects the server to be running on localhost:8000
    # Run the server in a separate terminal: python main.py
    # Then run this test.
    asyncio.run(test_connection())
