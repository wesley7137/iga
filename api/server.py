from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from Web_Voyager import Web_Voyager
import threading
import asyncio
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

web_voyager = None

def run_web_voyager(initial_task=""):
    global web_voyager
    web_voyager = Web_Voyager(initial_task=initial_task, initial_tools={
            'useSelenium': { 'file': 'useSelenium.py', 'desc': 'Use Selenium to programmatically interact with a web browser'}, 
            'useBeautifulSoup':{ 'file': 'useBeautifulSoup.py', 'desc': 'Use BeautifulSoup to scrape web content'},
        })
    while web_voyager.iteration < web_voyager.max_iterations and not web_voyager.done:
        web_voyager.step()
        if web_voyager.should_stop():
            break
        web_voyager.increment_iter()

# Store all connected clients
connected_clients = set()

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
            await websocket.send_text(str(data)) # Using send_text here
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
    await emit_to_clients(message)
    return {"status": "Message sent to all connected clients"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001, log_level="info")
