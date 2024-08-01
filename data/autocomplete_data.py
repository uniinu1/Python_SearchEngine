import redis

# Redis 서버에 연결
r = redis.Redis(host='localhost', port=6379, db=0)

# 자동완성을 위한 키워드 저장
keywords = {
    '교': ['교촌치킨', '교보문고'],
    '교차': ['구미교차로','울산교차로','부산교차로','서울교차로','제주교차로']
}

for prefix, words in keywords.items():
    for word in words:
        # 각 단어를 prefix를 키로 사용하여 저장
        r.zadd(f'autocomplete:{prefix}', {word: 0})

#FLUSHDB : 데이터 모두 삭제
# 키워드별 가중치 부여
#ZRANGE autocomplete:교차 0 -1 WITHSCORES
# r.zadd('autocomplete:교차', {'울산교차로': 1})
# r.zadd('autocomplete:교차', {'제주교차로': 2})
# r.zadd('autocomplete:교차', {'부산교차로': 3})
