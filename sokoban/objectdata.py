SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
UNIT_SIZE = 50


class ObjectData:
    def __init__(self, points, defaults):
        self.data = {k: v for k, v in dict(zip(points, defaults)).items()}

    def __getitem__(self, item):
        if item not in self.data:
            raise LookupError(f'No such data point as {item}')
        return self.data[item]

    def __setitem__(self, key, value):
        if key not in self.data:
            raise LookupError(f'No such data point as {key}')
        self.data[key] = value

    def __repr__(self):
        return str(self.data)
