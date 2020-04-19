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


class Derivative():
    def __init__(self, width):
        self.values = []
        self.val = 0.0
        self.width = width

    def add(self, v):
        self.values.append(v)
        if (len(self.values) > self.width):
            p = self.values.pop(0)
        self.val = (self.values[-1] - self.values[0]) / len(self.values)

    def value(self):
        return self.val


class Threshold():
    def __init__(self, thesholdFn):
        self.fn = thesholdFn
        self.val = 0;

    def add(self, v):
        self.val = v

    def value(self):
        return 1.0 if self.val > self.fn() else 0


class SchmittHysteresis():
    def __init__(self, thesholdOnFn, thesholdOffFn):
        self.fnOn = thesholdOnFn
        self.fnOff = thesholdOffFn
        self.val = 0;
        self.state = 0;

    def add(self, v):
        self.val = v

    def value(self):
        if self.state == 0 and self.val > self.fnOn():
            self.state = 1
        elif self.state == 1 and self.val < self.fnOff():
            self.state = 0

        return self.state


