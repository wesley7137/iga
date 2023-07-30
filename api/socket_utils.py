from flask_socketio import SocketIO

# Create the SocketIO object
socketio = SocketIO()

def emit_event(event_name, data):
    """Emit an event to connected clients"""
    socketio.emit(event_name, data)
