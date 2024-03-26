class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.tail.next = self.head  

    def remove(self, data):
        current = self.head
        prev = None
        while current:
            if current.data == data:
                if prev:
                    prev.next = current.next
                    if current == self.head:
                        self.head = current.next
                    if current == self.tail:
                        self.tail = prev
                else:
                    self.head = current.next
                    if current == self.tail:
                        self.tail = None
                return True
            prev = current
            current = current.next
            if current == self.head:  # Back to the start
                break
        return False

    def __contains__(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
            if current == self.head:  # Back to the start
                break
        return False

class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache = CircularLinkedList()
        self.cache_size = 0
        self.cache_hit = 0
        self.tot_cnt = 0

    def do_sim(self, page):
        self.tot_cnt += 1
        if page in self.cache:
            self.cache.remove(page)
            self.cache.append(page)
            self.cache_hit += 1
        else:
            if self.cache_size >= self.cache_slots:
                self.cache.remove(self.cache.head.data)
                self.cache_size -= 1
            self.cache.append(page)
            self.cache_size += 1

    def print_stats(self):
        print("cache_slot =", self.cache_slots, "cache_hit =", self.cache_hit, "hit ratio =", self.cache_hit / self.tot_cnt)

if __name__ == "__main__":
    data_file = open("./linkbench.trc")
    lines = data_file.readlines()
    for cache_slots in range(100, 1001, 100):
        cache_sim = CacheSimulator(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)
        cache_sim.print_stats()
