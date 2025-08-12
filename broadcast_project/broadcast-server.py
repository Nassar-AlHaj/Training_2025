import asyncio
import websockets
import argparse
import sys
import signal

class BroadcastServer:
    def __init__(self, host="localhost", port=12345):
        self.host = host
        self.port = port
        self.clients = set()
        
    async def handle_client(self, websocket):
        client_address = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        self.clients.add(websocket)
        print(f"[+] Client connected: {client_address} (Total: {len(self.clients)})")
        
        try:
            await websocket.send(f"Welcome! You are {client_address}")
            if len(self.clients) > 1:
                await self.broadcast_message(f"[System] {client_address} joined", exclude=websocket)
            
            async for message in websocket:
                formatted_message = f"[{client_address}] {message}"
                print(formatted_message)
                await self.broadcast_message(formatted_message, exclude=websocket)
                
        except websockets.exceptions.ConnectionClosed:
            print(f"[-] Client disconnected: {client_address}")
        except Exception as e:
            print(f"[!] Error with client {client_address}: {e}")
        finally:
            self.clients.discard(websocket)
            if self.clients:
                await self.broadcast_message(f"[System] {client_address} left")
            print(f"[=] Total clients: {len(self.clients)}")
    
    async def broadcast_message(self, message, exclude=None):
        if not self.clients:
            return
        recipients = [client for client in self.clients if client != exclude]
        if recipients:
            results = await asyncio.gather(*[client.send(message) for client in recipients], return_exceptions=True)
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.clients.discard(recipients[i])
    
    async def start_server(self):
        print(f"Starting broadcast server on {self.host}:{self.port}")
        print("Press Ctrl+C to stop the server")
        
        def signal_handler(signum, frame):
            print("\nServer shutdown requested")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        try:
            async with websockets.serve(self.handle_client, self.host, self.port):
                print(f"Server is listening on ws://{self.host}:{self.port}")
                await asyncio.Future()
        except KeyboardInterrupt:
            print("\nServer stopped")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            print("Server shutdown complete")

class BroadcastClient:
    def __init__(self, host="localhost", port=12345):
        self.host = host
        self.port = port
        self.running = False
    
    async def connect_to_server(self):
        uri = f"ws://{self.host}:{self.port}"
        try:
            print(f"Connecting to {uri}...")
            async with websockets.connect(uri) as websocket:
                self.running = True
                print("Connected to broadcast server!")
                print("Type your messages and press Enter. Type 'exit' or 'quit' to leave.")
                
                receive_task = asyncio.create_task(self.receive_messages(websocket))
                
                try:
                    await self.handle_input(websocket)
                except KeyboardInterrupt:
                    print("\nDisconnecting...")
                finally:
                    self.running = False
                    receive_task.cancel()
                    
        except ConnectionRefusedError:
            print(f"Could not connect to server at {uri}")
            print("Make sure the server is running with: broadcast-server start")
        except Exception as e:
            print(f"Connection error: {e}")
    
    async def receive_messages(self, websocket):
        try:
            async for message in websocket:
                print(f"\r{message}")
                print("You: ", end="", flush=True)
        except websockets.exceptions.ConnectionClosed:
            if self.running:
                print("\nConnection closed by server")
        except Exception as e:
            if self.running:
                print(f"\nError receiving messages: {e}")
    
    async def handle_input(self, websocket):
        loop = asyncio.get_event_loop()
        while self.running:
            try:
                message = await loop.run_in_executor(None, input, "You: ")
                message = message.strip()
                if message.lower() in ['exit', 'quit']:
                    print("Disconnecting from server...")
                    break
                if message:
                    await websocket.send(message)
            except EOFError:
                break
            except Exception as e:
                print(f"Error sending message: {e}")
                break

def main():
    parser = argparse.ArgumentParser(description="Broadcast Server")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    server_parser = subparsers.add_parser('start', help='Start the broadcast server')
    server_parser.add_argument('--port', type=int, default=12345, help='Port (default: 12345)')
    
    client_parser = subparsers.add_parser('connect', help='Connect to the broadcast server')
    client_parser.add_argument('--host', default='localhost', help='Host (default: localhost)')  
    client_parser.add_argument('--port', type=int, default=12345, help='Port (default: 12345)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'start':
            server = BroadcastServer('localhost', args.port)  
            asyncio.run(server.start_server())
        elif args.command == 'connect':
            client = BroadcastClient(args.host, args.port)
            asyncio.run(client.connect_to_server())
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
