class Node:
    def __init__(self, floor_name, R, C, F, S, patterns):
        self.floor_name = floor_name
        self.R = R
        self.C = C
        self.F = F
        self.S = S
        self.patterns = patterns
        self.next = None