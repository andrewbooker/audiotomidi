
from utils.analysis import AbsMovingAvg, Threshold, Derivative
class Chaser():
    def __init__(self, consumer, high, low):
        self.avg = AbsMovingAvg(44)
        self.deriv = Derivative(2)
        self.thrOn = Threshold(lambda: high)
        self.thrOff = Threshold(lambda: low)
        self.state = 0
        self.consumer = consumer
        
    def add(self, v):
        self.avg.add(v)
        self.thrOn.add(self.avg.value())
        self.thrOff.add(self.avg.value())
        self.deriv.add(self.avg.value())

        if self.thrOn.value() == 1 and self.state == 0:
            self.state = 1
        elif self.deriv.value() < 0 and self.state == 1:
            self.consumer.on(self.thrOn.overshoot())
            self.state = 2
        elif self.thrOff.value() == 0 and self.state == 2:
            self.state = 0
            self.consumer.off()
