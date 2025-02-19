from objectdata import ObjectData


class GameObject:
    objects = []

    def __init__(self, objtype, index=0, dont_destroy=False):
        self.__type = objtype
        self.__data = ObjectData(objtype.data_points, objtype.data_defaults)
        self.dont_destroy = dont_destroy

        GameObject.objects.insert(index, self)

    def get_type(self):
        return self.__type

    def get_data(self):
        return self.__data

    def __getitem__(self, item):
        return self.__data[item]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def draw(self, sur, ui_surface):
        self.__type.draw(sur, (self['x'], self['y']), ui_surface, self.__data)

    def on_key_pressed(self, key):
        try:
            self.__data = self.__type.on_key_pressed(key, self.__data)
        except NotImplementedError:
            pass

    def on_mouse_button_down(self):
        try:
            self.__data = self.__type.on_mouse_button_down(self.__data)
        except NotImplementedError:
            pass

    def on_update(self):
        try:
            self.__data = self.__type.on_update(self.__data)
        except NotImplementedError:
            pass

    def setup(self):
        try:
            self.__data = self.__type.setup(self.__data)
        except NotImplementedError:
            pass

    @classmethod
    def get_solid_object_by_position(cls, x, y):
        for obj in cls.objects:
            if obj['x'] == x and obj['y'] == y and obj.get_type().solid:
                return obj
        return None

    @staticmethod
    def compare_type(obj_a, obj_b):
        if obj_a is not None and obj_b is not None:
            if obj_a.type == obj_b.type:
                return True
        return False

    @staticmethod
    def is_type(obj, type):
        if obj is None:
            if type is None:
                return True
        else:
            if obj.type == type:
                return True
        return False


def create_object_at(objtype, x, y, index=0, dont_destroy=False):
    obj = GameObject(objtype, index, dont_destroy)
    obj['x'] = x
    obj['y'] = y
    return obj


def clear_gameobjects():
    GameObject.objects = [i for i in GameObject.objects if i.dont_destroy]
