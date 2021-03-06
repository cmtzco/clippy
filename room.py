import os.path
import string
import random

# TODO
# ensure that the class can handle recreating new session ids so that the JS does not have to continually refresh
# till an ID is found.

class Room:

    def __init__(self):
        self.room_path = './rooms/'

    def id_generator(self, size=6, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def id_sanitize(self, id):
        return id[:6]

    def generate_room_path(self, id):
        return "{}{}".format(self.room_path, id)

    def check_room_id(self, id):
        full_path = "{}{}".format(self.room_path, id)
        return os.path.isfile(full_path)

    def generate_room(self, id=None):
        if id is None:
            room = self.id_generator()
            if self.check_room_id(room):
                return "This room already exists"
            else:
                full_path = self.generate_room_path(room)
                file = open(full_path, "w+")
                file.close()
                return room
        elif id:
            room = self.id_sanitize(id)
            full_path = self.generate_room_path(room)
            file = open(full_path, "w+")
            file.close()
            return room

    def write_room(self, room, message):
        file = open(self.generate_room_path(room), "w+")
        file.truncate()
        file.write(message)
        file.close()

