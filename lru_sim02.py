from list.circularLinkedList import CircularLinkedList

class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache_hit = 0
        self.tot_cnt = 0
        self.cache = CircularLinkedList()

    def do_sim(self, page):
        self.tot_cnt += 1
        # 페이지가 캐시에 이미 존재하는지 확인
        page_in_cache = False
        curr = self.cache._CircularLinkedList__tail.next
        for _ in range(self.cache.size()):
            if curr.item == page:
                page_in_cache = True
                break
            curr = curr.next

        if page_in_cache:
            # 페이지가 이미 캐시에 있으면 해당 페이지를 제거하고 다시 추가하여 최근 사용된 것으로 표시
            self.cache.remove(page)
            self.cache.append(page)
            self.cache_hit += 1
        else:
            # 페이지가 캐시에 없으면 새 페이지를 추가
            if self.cache.size() == self.cache_slots:
                # 캐시가 가득 찼으면 가장 오래된 페이지를 제거
                self.cache.pop(0)
            self.cache.append(page)
        
    def print_stats(self):
        print("cache_slot = ", self.cache_slots, "cache_hit = ", self.cache_hit, "hit ratio = ", self.cache_hit / self.tot_cnt)

if __name__ == "__main__":

    data_file = open("./linkbench.trc")
    lines = data_file.readlines()
    for cache_slots in range(100, 1001, 100):
        cache_sim = CacheSimulator(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)
        
        cache_sim.print_stats()
