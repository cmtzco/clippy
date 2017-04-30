from flask import Flask, render_template, session
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from room import RoomGenerator


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# app.config['threaded'] = True
socketio = SocketIO(app, async_mode=async_mode) # , async_mode=async_mode
namespace = '/test'
rooms = Room()



@app.route('/')
def index():
    return render_template('index.html',  async_mode=socketio.async_mode)

# @app.route('/<namespace>')
# def workspace(namespace="/test"):
#     socketio.on_namespace(CustomNamespace(namespace))
#     return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/id/create')
def room_page():
    return rooms.generate_room()


@socketio.on('my event', namespace=namespace)
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace=namespace)
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)
    rooms.write_room(message['room'], message['data'])

@socketio.on('join', namespace=namespace)
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'],
          'count': session['receive_count']})

@socketio.on('connect', namespace=namespace)
def test_connect():
    emit('my response', {'data': ''})

@socketio.on('disconnect', namespace=namespace)
def test_disconnect():
    print('Client disconnected')

# class CustomNamespace(Namespace):
#
#     def broadcast(self, message):
#         emit('my response', {'data': message['data']}, broadcast=True)
#
#
#     def connect(self):
#         emit('my response', {'data': 'Connected'})
#
#
#     def disconnect(self):
#         print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, port=5555, host='0.0.0.0', debug='True')