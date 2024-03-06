from nodo import Node

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, floor_name, R, C, F, S, patterns):
        new_node = Node(floor_name, R, C, F, S, patterns)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def search_floor(self, floor_name):
        current = self.head
        while current:
            if current.floor_name == floor_name:
                return current
            current = current.next
        return None

    def search_pattern(self, floor_name, pattern_code):
        floor = self.search_floor(floor_name)
        if floor:
            patterns = floor.patterns
            if pattern_code in patterns:
                return patterns[pattern_code]
        return None