#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PAGESIZE 256

struct Node {
    char data[MAX_PAGESIZE];
    struct Node* next;
};

struct CircularLinkedList {
    struct Node* head;
    struct Node* tail;
};

//캐시 시뮬레이터 구조체
struct CacheSimulator {
    struct CircularLinkedList cache; 
    int cache_slots;  
    int cache_hit;                 
    int tot_cnt;                    
};

void initializeLinkedList(struct CircularLinkedList* list) {
    list->head = NULL;
    list->tail = NULL;
}

//캐시 시뮬레이터 초기화
void initializeCacheSimulator(struct CacheSimulator* cache_sim, int slots) {
    initializeLinkedList(&(cache_sim->cache));
    cache_sim->cache_slots = slots;
    cache_sim->cache_hit = 0;
    cache_sim->tot_cnt = 0;
}

//페이지를 캐시에 추가하는 함수
void addToCache(struct CacheSimulator* cache_sim, char* page) {
    cache_sim->tot_cnt++;

    //캐시에 페이지가 있는지 확인
    struct Node* current = cache_sim->cache.head;
    while (current != NULL) {
        if (strcmp(current->data, page) == 0) { 
            cache_sim->cache_hit++;
            return;
        }
        current = current->next;
        if (current == cache_sim->cache.head) { 
            break;
        }
    }

    if (cache_sim->cache_slots > 0) {
        struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
        strcpy(newNode->data, page); // 페이지 데이터 복사
        if (cache_sim->cache.head == NULL) {
            newNode->next = newNode;
            cache_sim->cache.head = newNode;
            cache_sim->cache.tail = newNode;
        } else { //캐시가 비어 있지 않는 경우
            newNode->next = cache_sim->cache.head;
            cache_sim->cache.tail->next = newNode;
            cache_sim->cache.tail = newNode;
        }
        cache_sim->cache_slots--;
    } else { 
        strcpy(cache_sim->cache.head->data, page);
        cache_sim->cache.head = cache_sim->cache.head->next;
        cache_sim->cache.tail = cache_sim->cache.tail->next;
    }
}

//출력 함수
void printCacheStats(struct CacheSimulator* cache_sim) {
    printf("cache_hit = %d hit ratio = %.5f\n", cache_sim->cache_hit,
           (double)cache_sim->cache_hit / cache_sim->tot_cnt);
}

int main() {
    //데이터 파일 열기
    FILE* data_file = fopen("./linkbench.trc", "r");
    if (data_file == NULL) {
        fprintf(stderr, "Error: Unable to open the file.\n");
        return 1;
    }
    
    char line[MAX_PAGESIZE]; 
    int start_slots = 100;
    int increment = 100;

    //캐시 시뮬레이터 초기화
    struct CacheSimulator cache_sim;

    for (int cache_slots = start_slots; cache_slots <= 1000; cache_slots += increment) {
        initializeCacheSimulator(&cache_sim, cache_slots); 

        while (fgets(line, MAX_PAGESIZE, data_file) != NULL) {
            char* page = strtok(line, " \n"); 
            addToCache(&cache_sim, page);     
        }

        printf("cache_slot=%d ",cache_slots);
        printCacheStats(&cache_sim);

        fseek(data_file, 0, SEEK_SET);
    }

    fclose(data_file);

    return 0;
}
