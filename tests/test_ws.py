import asyncio
import websockets
import json

async def test_connection():
    uri = "ws://localhost:9001/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to server")
            
            # The server sends a list of packets. 
            # Upon connection, we expect a ConnectedPacket (ID 0).
            try:
                # Wait for the first message from the server
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                packets = json.loads(message)
                print(f"Received: {packets}")
                
                # The server sends packets as a list of serialized packets: [[id, data], ...]
                # ConnectedPacket is [0, None]
                found_connected = False
                for packet in packets:
                    if isinstance(packet, list) and packet[0] == 0:
                        found_connected = True
                        break
                
                if found_connected:
                    print("SUCCESS: Received ConnectedPacket from server.")
                else:
                    print("FAILURE: ConnectedPacket not found in the received message.")
                
            except asyncio.TimeoutError:
                print("FAILURE: Timeout waiting for ConnectedPacket from server.")
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed by server: {e.code} {e.reason}")
            except Exception as e:
                print(f"Error while receiving: {e}")
                
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    # This test expects the server to be running on localhost:8000
    # Run the server in a separate terminal: python main.py
    # Then run this test.
    asyncio.run(test_connection())
