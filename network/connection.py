import asyncio
import json
import time
from typing import Any, Callable, Optional
from fastapi import WebSocket, WebSocketDisconnect
from common.log import log

class Connection:
    """
    The Connection class wraps the FastAPI WebSocket to add safety and utility features.
    It acts as the bridge between the raw WebSocket and the game logic.
    """

    def __init__(self, instance: str, socket: WebSocket):
        self.instance = instance
        self.socket = socket
        self.address = socket.client.host if socket.client else "unknown"
        
        # Used for filtering duplicate messages.
        self.last_message = ""
        self.last_message_time = time.time() * 1000
        self.message_difference = 100 # Prevent duplicate messages coming in faster than 100ms.
        
        self.message_rate = 0 # The amount of messages received in the last second.
        self.timeout_duration = 10 * 60 # 10 minutes (in seconds for Python's asyncio)
        
        self.rate_task: Optional[asyncio.Task] = None
        self.verify_task: Optional[asyncio.Task] = None
        self.timeout_task: Optional[asyncio.Task] = None
        
        self.closed = False
        
        self.message_callback: Optional[Callable[[Any], None]] = None
        self.close_callback: Optional[Callable[[], None]] = None

        # Reset the messages per second every second.
        self.rate_task = asyncio.create_task(self._rate_limiter_loop())
        
        # Run the verification interval every 30 seconds to ensure the connection is still open.
        self.verify_task = asyncio.create_task(self._verify_loop())
        
        log.info(f"Received socket connection from: {self.address}.")

    async def _rate_limiter_loop(self):
        try:
            while not self.closed:
                await asyncio.sleep(1)
                self.message_rate = 0
        except asyncio.CancelledError:
            pass

    async def _verify_loop(self):
        try:
            while not self.closed:
                await asyncio.sleep(30)
                if self.closed:
                    log.warning(f"Connection {self.address} closed improperly.")
                    await self.handle_close()
        except asyncio.CancelledError:
            pass

    async def reject(self, reason: str):
        """
        Sends a message to the client for closing the connection,
        then closes the connection.
        """
        if self.closed:
            await self.handle_close(reason)
            return

        await self.close(reason)

    async def close(self, reason: Optional[str] = None, force: bool = False):
        """
        Closes a connection and takes an optional parameter for debugging purposes.
        """
        if not self.closed:
            try:
                # Close codes: 1000 is normal, 1010 is for server-initiated close with reason in some contexts.
                # WebSocket.close() in FastAPI/Starlette accepts code and reason.
                await self.socket.close(code=1000, reason=reason)
            except Exception as e:
                log.debug(f"Error while closing socket: {e}")
            finally:
                self.closed = True

        if reason:
            log.info(f"Connection {self.address} has closed, reason: {reason}.")

        if force:
            await self.handle_close()

    async def handle_close(self, reason: Optional[str] = None):
        """
        Receives the close signal and ends the connection with the socket.
        """
        if self.closed and not reason: # Already handled
            return

        log.info(f"Closing socket connection to: {self.address}.")
        if reason:
            log.info(f"Received reason: {reason}.")

        self.closed = True
        
        if self.close_callback:
            if asyncio.iscoroutinefunction(self.close_callback):
                await self.close_callback()
            else:
                self.close_callback()

        self.clear_timeout()
        self.clear_rate_task()
        self.clear_verify_task()

    def update_timeout(self, duration: int):
        """
        Updates the timeout duration for the player and refreshes the existing timeout.
        @param duration The new duration of the timeout in seconds.
        """
        self.timeout_duration = duration
        self.refresh_timeout()

    def refresh_timeout(self):
        """
        Resets the timeout every time an action is performed.
        """
        self.clear_timeout()
        self.timeout_task = asyncio.create_task(self._timeout_callback())

    async def _timeout_callback(self):
        try:
            await asyncio.sleep(self.timeout_duration)
            await self.reject("timeout")
        except asyncio.CancelledError:
            pass

    def clear_verify_task(self):
        if self.verify_task:
            self.verify_task.cancel()
            self.verify_task = None

    def clear_rate_task(self):
        if self.rate_task:
            self.rate_task.cancel()
            self.rate_task = None

    def clear_timeout(self):
        if self.timeout_task:
            self.timeout_task.cancel()
            self.timeout_task = None

    def is_duplicate(self, message: str) -> bool:
        """
        Ensures duplicate packets are only parsed once every message_difference milliseconds.
        """
        now = time.time() * 1000
        is_dup = (message == self.last_message and now - self.last_message_time < self.message_difference)
        
        if not is_dup:
            self.last_message = message
            self.last_message_time = now
            
        return is_dup

    async def send(self, message: Any):
        """
        Takes a JSON object and stringifies it. Sends it to the client.
        """
        await self.send_utf8(json.dumps(message))

    async def send_utf8(self, message: str):
        """
        Sends a simple UTF8 string to the socket.
        """
        if self.closed:
            log.warning("Attempted to send message to closed connection.")
            return

        try:
            await self.socket.send_text(message)
        except Exception as e:
            log.error(f"Failed to send message to {self.address}: {e}")
            await self.handle_close("send_failure")

    def on_message(self, callback: Callable[[Any], None]):
        self.message_callback = callback

    def on_close(self, callback: Callable[[], None]):
        self.close_callback = callback
