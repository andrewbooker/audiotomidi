#!/usr/bin/env python

class MovingAvg():
    def __init__(self, size):
        self.size = size
        self.clear()

    def clear(self):
        self.values = []
        self.avg = 0.0

    def add(self, v):
        self.avg += (v * 1.0 / self.size)
        self.values.append(v)
        if (len(self.values) > self.size):
            p = self.values.pop(0)
            self.avg -= (p * 1.0 / self.size)

    def first(self):
        return self.values[0]

    def value(self):
        return self.avg if (len(self.values) == self.size) else (self.avg * self.size / len(self.values))


class AbsMovingAvg(MovingAvg):
    def __init__(self, size):
        MovingAvg.__init__(self, size)

    def add(self, v):
        self.avg += (abs(v) * 1.0 / self.size)
        self.values.append(v)
        if (len(self.values) > self.size):
            p = self.values.pop(0)
            self.avg -= (abs(p) * 1.0 / self.size)
