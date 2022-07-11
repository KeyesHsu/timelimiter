class Counter:
    __slots__ = ("_val",)

    def __init__(self, val=0):
        self._val = int(val)

    def inc(self, val=1):
        self._val = self._val + val

    def dec(self, val=1):
        self._val = self._val + -val

    def reset(self):
        self._val = 0

    @property
    def val(self):
        return self._val
