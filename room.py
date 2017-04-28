import os.path
import string
import random



class RoomGenerator:

    def __init__(self):
        self.room_path = 'rooms/'

    def id_generator(self, size=6, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def id_sanitize(self, id):
        return id[:6]

    def check_room_id(self, id):
        full_path = "{}{}".format(self.room_path, id)
        return os.path.isfile(full_path)

    def generate_room(self, id=None):
        if id is None:
            room = self.id_generator()
            file = open(room, "w+")
            file.close()
            return room
        elif id:
            room = self.id_sanitize(id)
            file = open(room, "w+")
            file.close()
            return room

