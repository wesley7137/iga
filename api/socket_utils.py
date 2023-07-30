import json

async def emit_data_via_sockets(clients, data):
    message = json.dumps(data)
    for client in clients:
        await client.send_text(message)
