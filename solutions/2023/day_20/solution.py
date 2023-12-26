
# Load utils
import sys
sys.path.append('../../')
from utils import *

################################################################################
class Signal(Enum):
    Non = 0,
    High = 1,
    Low = 2


class Switch:

    def __init__(self, line):
        name, targets = line.split("->")
        self.name = name.strip()[1:]
        self.targets = []
        for t in targets.split(","):
            self.targets.append(t.strip())
        self.highs = 0
        self.lows = 0

    def process_signal(self, name, signal: Signal) -> Signal:
        s = self.process_signal_(name, signal)

        # debug(f"Switch <{self.name}> with signal <{signal.name}> from <{name}> with result <{s.name}>")
        debug(f"{name}  \t<{signal.name}>  \t->  {self.name}  \t:  <{s.name}>")

        if s == Signal.High:
            self.highs += 1
        elif s == Signal.Low:
            self.lows += 1
        return s

    def process_signal_(self, name, signal: Signal) -> Signal:
        pass

    def decode(self) -> str:
        return ""

    def add_source(self, name):
        pass

    def create_switch(line) -> "Switch":
        if line[0] == "%":
            return FlipFlop(line)
        elif line[0] == "&":
            return Conjuction(line)
        else:
            return Broadcaster(line)


class FlipFlop (Switch):

    def __init__(self, line: str):
        super().__init__(line)
        self.on = False

    def decode(self) -> str:
        if self.on:
            return "1"
        else:
            return "0"

    def process_signal_(self, name, signal: Signal) -> Signal:
        if signal == Signal.Low:
            self.on = not self.on
            if self.on:
                return Signal.High
            else:
                return Signal.Low
        else:
            return Signal.Non


class Conjuction (Switch):

    def __init__(self, line: str):
        super().__init__(line)
        self.signals = {}

    def add_source(self, name):
        self.signals[name] = False

    def process_signal_(self, name, signal: Signal) -> Signal:
        if signal == Signal.High:
            self.signals[name] = True
        else:
            self.signals[name] = False

        # debug(f"Conjuction {self.name}  with signals {self.signals}")

        if all(self.signals.values()):
            return Signal.Low
        else:
            return Signal.High


class Broadcaster (Switch):
    def __init__(self, line: str):
        super().__init__("_" + line)

    def process_signal_(self, name, signal: Signal) -> Signal:
        return Signal.Low


class Empty (Switch):
    def __init__(self, name: str):
        self.name = name
        self.targets = []

    def process_signal_(self, name, signal: Signal) -> Signal:
        return Signal.Non


################################################################################
def solution_a(inp):
    switches = {}
    for line in inp:
        s = Switch.create_switch(line)
        switches[s.name] = s

    new_dict = {}
    for name, s in switches.items():
        for t in s.targets:
            if t in switches.keys():
                switches[t].add_source(name)
            else:
                new_dict[t] = Empty(t)

    switches.update(new_dict)

    highs = 0
    lows = 0
    button_press = 1000
    for i in range(button_press):

        signals_to_process = [("broadcaster", "button", Signal.Low)]

        while len(signals_to_process) > 0:
            to, src, signal = signals_to_process.pop(0)

            if signal == Signal.High:
                highs += 1
            else:
                lows += 1

            signal_result = switches[to].process_signal(src, signal)

            if signal_result != Signal.Non:
                for t in switches[to].targets:
                    signals_to_process.append((t, to, signal_result))

    debug(f"Lows: {lows}")
    debug(f"Highs: {highs}")
    return highs * lows


################################################################################

################################################################################
def solution_b(inp):
    return -1
