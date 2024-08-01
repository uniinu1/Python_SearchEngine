import csv
import redis

# Redis 연결 설정
r = redis.Redis(host='localhost', port=6379, db=0)

def insert_product_names_from_csv(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # 첫 번째 행(헤더)을 건너뜁니다.
        for row in csv_reader:
            product_name = row[0]
            insert_product_name(product_name)
            create_inverted_index_for_product_name(product_name)

def insert_product_name(product_name):
    for end in range(1, len(product_name) + 1):
        prefix = product_name[:end]
        # 접두사를 키로 하고, 상품명을 값으로 하는 Sorted Set에 저장
        r.zadd('autocomplete', {product_name: 0}, nx=True, ch=True)

def create_inverted_index_for_product_name(product_name):
    # 상품명을 공백을 기준으로 분리하여 각 단어에 대해 인버티드 인덱스 생성
    words = product_name.split()
    for word in words:
        # 각 단어에 대해 상품명을 저장하는 Sorted Set에 추가
        r.zadd(f'word:{word.lower()}', {product_name: 0}, nx=True, ch=True)

def search_products(prefix):
    # 주어진 접두사로 시작하는 모든 상품명을 조회
    results = r.zrangebylex('autocomplete', f'[{prefix}', f'[{prefix}\xff')
    return results

def search_by_keyword(keyword):
    # 인버티드 인덱스를 사용하여 키워드를 포함하는 모든 상품명 조회
    # 'autocomplete' Sorted Set에서 모든 상품명을 조회
    all_products = r.zrange('autocomplete', 0, -1)
    # 키워드를 포함하는 상품명을 필터링
    keyword_lower = keyword.lower()
    results = [product.decode('utf-8') for product in all_products if keyword_lower in product.decode('utf-8').lower()]
    return results

# CSV 파일에서 상품명 읽어 Redis에 저장
csv_file_path = '/Users/smpark/Documents/example2.csv'  # 경로는 환경에 맞게 수정해야 합니다.
insert_product_names_from_csv(csv_file_path)

# 접두사 '마그'로 시작하는 상품명 검색 예제
# search_results_prefix = search_products('마그')
# print(search_results_prefix)

# 키워드 '마그네'를 포함하는 상품명 검색 예제
# search_results_keyword = search_by_keyword('마그네틱')
# print(search_results_keyword)