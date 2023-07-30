from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from Web_Voyager import Web_Voyager
import threading
import asyncio
from environment.manage_skills import initialize_skills
from starlette.websockets import WebSocketDisconnect
import json
from socket_utils import emit_data_via_sockets

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

web_voyager = None
web_voyager_thread = None
stop_web_voyager = False

def run_web_voyager(initial_task=""):
    global web_voyager, stop_web_voyager
    stop_web_voyager = False
    skills = initialize_skills()
    web_voyager = Web_Voyager(initial_task=initial_task, tools=skills)
    while web_voyager.iteration < web_voyager.max_iterations and not web_voyager.done and not stop_web_voyager: 
        web_voyager.step()
        if web_voyager.should_stop():
            break
        web_voyager.increment_iter()

# Store all connected clients
connected_clients = set()

async def start_web_voyager(initial_task=""):
    global web_voyager_thread
    web_voyager_thread = threading.Thread(target=run_web_voyager, args=(initial_task,))
    web_voyager_thread.start()

async def stop_web_voyager():
    global web_voyager_thread, stop_web_voyager
    print("Stop has been called")
    stop_web_voyager = True
    if web_voyager_thread:
        web_voyager_thread.join()
        web_voyager_thread = None

@app.websocket("/connect")
async def websocket_connected(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print("client has connected")

@app.websocket("/disconnect")
async def websocket_disconnected(websocket: WebSocket):
    connected_clients.remove(websocket)
    await websocket.close()
    print("user disconnected")

@app.websocket("/start")
async def websocket_start(websocket: WebSocket):
    print("Start has been called")
    await websocket.accept()

@app.websocket("/stop")
async def websocket_stop(websocket: WebSocket):
    print("Stop has been called")
    await websocket.accept()

@app.websocket("/data")
async def websocket_data(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket) # Add the client to the list
    try:
        while True:
            data = await websocket.receive_text()
            print("data from the front end: ", str(data))

    except WebSocketDisconnect:
        connected_clients.remove(websocket) # Remove the client from the list
        print("A client has disconnected")

# This function can be called to emit messages to all connected clients
async def emit_to_clients(message: str):
    for client in connected_clients:
        # Since we're outside an async function, you'll need to ensure this is run in an event loop
        await client.send_text(message)

# You can create a route that triggers the emit_to_clients function to test it.
@app.get("/emit")
async def emit_message(message: str = "Test message"):
    await emit_data_via_sockets(connected_clients, message)
    return {"status": "Message sent to all connected clients"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001, log_level="info")
