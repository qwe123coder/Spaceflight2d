class starrange(object):
    __slots__ = ("min", "max", "pos")

    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.pos = min - 1

    def __iter__(self):
        self.pos = self.min - 1
        return self

    def __next__(self):
        if self.pos > self.max:
            raise StopIteration
        else:
            self.pos += 1
            if self.pos == 0:
                self.pos += 1
            return self.pos
