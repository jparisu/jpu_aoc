
# Load utils
import sys
sys.path.append('../../')
from utils import *
from functools import reduce

################################################################################
class Part:
    def __init__(self, line: str):
        self.parts = {}
        debug(line)

        line = line[1:-1]
        debug(line)
        for x in line.split(","):
            debug(x)
            n, v = x.split("=")
            self.parts[n] = int(v)

    def value(self) -> int:
        return sum(self.parts.values())

    def __str__(self) -> str:
        return str(self.parts)


class Condition:

    def __init__(self, condition_str: str):
        self.letter = None
        self.value = None
        self.gt = None

        if "<" in condition_str:
            self.letter, v = condition_str.split("<")
            self.value = int(v)
            self.gt = False

        else:
            self.letter, v = condition_str.split(">")
            self.value = int(v)
            self.gt = True

    def work(self, part: Part) -> bool:
        v = part.parts[self.letter]
        if self.gt and v > self.value:
            return True
        elif not self.gt and v < self.value:
            return True
        return False



class TrueCondition(Condition):

    def __init__(self):
        pass

    def work(self, part: Part) -> bool:
        return True


class Rule:

    def __init__(self, line):
        name, d = line.split("{")

        self.name = name
        self.conditions = []

        d = d[:-1]
        conditions = d.split(",")
        for c in conditions[:-1]:
            con, res = c.split(":")
            self.conditions.append((Condition(con), res))

        self.conditions.append((TrueCondition(), conditions[-1]))

    def work(self, part: Part) -> str:
        for c in self.conditions:
            if c[0].work(part):
                debug(f"Rule {self.name} with part {part} returns {c[1]}")
                return c[1]


def routine(rules: Dict[str, Rule], parts: List[Part]) -> int:
    value = 0
    for p in parts:
        rule = rules["in"]
        while True:
            rule_name = rule.work(p)
            if rule_name == "R":
                break
            elif rule_name == "A":
                value += p.value()
                break
            else:
                rule = rules[rule_name]
    return value


################################################################################
def solution_a(inp):
    rules = {}
    parts = []
    for line in inp:
        if line == "":
            continue

        if line[0] != "{":
            r = Rule(line)
            rules[r.name] = r
        else:
            parts.append(Part(line))

    return routine(rules, parts)

################################################################################
class Range:

    def __init__(self, ini, fin):
        self.ini = ini
        self.fin = fin

    def divide(self, point: int) -> List["Range"]:
        if point <= self.ini and point > self.fin:
            return [self]
        else:
            return [Range(self.ini, point), Range(point, self.fin)]

    def value(self) -> int:
        return self.fin - self.ini


class PartRange:

    def __init__(self, x: Range, m: Range, a: Range, s: Range):
        self.parts = {
            "x": x,
            "m": m,
            "a": a,
            "s": s,
        }

    def value(self) -> int:
        return reduce((lambda x, y : x*y), [z.value() for z in self.parts.values()])


class ConditionRange:

    def __init__(self, condition_str: str):
        self.letter = None
        self.value = None
        self.gt = None
        cs, self.path = condition_str.split(":")

        if "<" in cs:
            self.letter, v = cs.split("<")
            self.value = int(v)
            self.gt = False

        else:
            self.letter, v = cs.split(">")
            self.value = int(v)
            self.gt = True


    def work(self, part: "PartRange") -> Tuple["ConditionRange", "ConditionRange"]:
        # TODO
        return (part, None)


class TrueConditionRange(ConditionRange):

    def __init__(self, condition_str: str):
        self.path = condition_str

    def work(self, part: "PartRange") -> Tuple["ConditionRange", "ConditionRange"]:
        return (part, None)


class RuleRange:

    def __init__(self, line):
        name, d = line.split("{")

        self.name = name
        self.conditions = []

        d = d[:-1]
        conditions = d.split(",")
        for c in conditions[:-1]:
            self.conditions.append(ConditionRange(c))

        self.conditions.append((TrueConditionRange(d[-1]), conditions[-1]))

    def work(self, part: "PartRange") -> List[Tuple["PartRange", str]]:
        result = []
        for c in self.conditions:

            p, r = c.work(part)
            if p is not None:
                result.append((p, c.path))

            if r is None:
                break

            part = r

        return result


def routine(rules: Dict[str, RuleRange]):
    value = 0
    N = 2

    first_range = PartRange(Range(0,N),Range(0,N),Range(0,N),Range(0,N))
    ranges = [(first_range, "in")]

    while len(ranges) > 0:

        rang, rule_name = ranges.pop()
        rule = rules[rule_name]
        results = rule.work(rang)

        for r, n in results:
            if n == "A":
                value += r.value()
            elif n != "R":
                ranges.append((r, n))

    return value


################################################################################
def solution_b(inp):
    rules = {}
    for line in inp:
        if line == "":
            continue
        if line[0] != "{":
            r = RuleRange(line)
            rules[r.name] = r

    return routine(rules)
