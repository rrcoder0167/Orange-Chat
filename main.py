from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.emit('join_message', {'username': username}, room=room)

@socketio.on('message')
def handle_message(data):
    message = data['message']
    room = data['room']
    socketio.emit('message', {'message': message}, room=room)

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, port=8080)
