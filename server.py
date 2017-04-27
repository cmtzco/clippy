from flask import Flask, render_template
from flask_socketio import SocketIO, Namespace, emit

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<namespace>')
def workspace(namespace):
    socketio.on_namespace(CustomNamespace(namespace))
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': ''})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

class CustomNamespace(Namespace):

    def test_message(self, message):
        emit('my response', {'data': message['data']})


    def test_message(self, message):
        emit('my response', {'data': message['data']}, broadcast=True)


    def test_connect(self):
        emit('my response', {'data': 'Connected'})


    def test_disconnect(self):
        print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, port=5555, host='0.0.0.0', debug='True')