import asyncio
import websockets
import json
import sys
import os

# Add the project root to sys.path to import common and network
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.config import config
from network.packets import Packets

async def test_connection():
    uri = f"ws://{config.host}:{config.port}/"
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
                    if isinstance(packet, list) and packet[0] == Packets.Connected:
                        found_connected = True
                        break
                
                if not found_connected:
                    print("FAILURE: ConnectedPacket not found in the received message.")
                    return

                print("SUCCESS: Received ConnectedPacket from server.")

                # Send Handshake packet
                # Format: [packet_id, data]
                handshake_packet = [Packets.Handshake, {"gVer": config.gver}]
                await websocket.send(json.dumps(handshake_packet))
                print(f"Sent Handshake: {handshake_packet}")

                # Wait for Handshake response
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                packets = json.loads(message)
                print(f"Received response: {packets}")

                found_handshake = False
                for packet in packets:
                    if isinstance(packet, list) and packet[0] == Packets.Handshake:
                        data = packet[1]
                        if data.get("type") == "client" and "instance" in data:
                            found_handshake = True
                            print(f"SUCCESS: Received valid Handshake response: {data}")
                        break
                
                if not found_handshake:
                    print("FAILURE: Valid Handshake response not found.")

            except asyncio.TimeoutError:
                print("FAILURE: Timeout waiting for packets from server.")
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed by server: {e.code} {e.reason}")
            except Exception as e:
                print(f"Error while receiving: {e}")
                
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    # This test expects the server to be running.
    # Run the server in a separate terminal: python main.py
    # Then run this test.
    asyncio.run(test_connection())
