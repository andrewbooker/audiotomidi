
from utils.analysis import AbsMovingAvg, Threshold, Derivative
class Chaser():
    def __init__(self, consumer):
        self.avg = AbsMovingAvg(44)
        self.deriv = Derivative(2)
        self.thrOn = Threshold(lambda: 0.04)
        self.thrOff = Threshold(lambda: 0.0039)
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
