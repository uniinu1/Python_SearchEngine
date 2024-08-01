import re
import pandas as pd
import time

def build_suffix_array(s):
    s = str(s)  # product_name을 문자열로 명시적 변환
    suffixes = [(s[i:], i) for i in range(len(s))]
    suffixes.sort(key=lambda x: x[0])
    return [suffix[1] for suffix in suffixes]

def search_patterns_in_text(suffix_array, text, pattern):
    l, r = 0, len(suffix_array) - 1
    results = []

    while l <= r:
        mid = (l + r) // 2
        suffix = text[suffix_array[mid]:]
        if suffix.startswith(pattern):
            results.append(suffix_array[mid])
            tmp = mid - 1
            while tmp >= 0 and text[suffix_array[tmp]:].startswith(pattern):
                results.append(suffix_array[tmp])
                tmp -= 1
            tmp = mid + 1
            while tmp < len(suffix_array) and text[suffix_array[tmp]:].startswith(pattern):
                results.append(suffix_array[tmp])
                tmp += 1
            break
        elif pattern < suffix:
            r = mid - 1
        else:
            l = mid + 1
    return results

def search_by_keyword(file_path, pattern):
    start_time = time.time()  # 처리 시작 시간 측정

    products_with_scores = []

    df = pd.read_excel(file_path, dtype={'goodsNm': str, 'score': float})  # 상품명을 문자열로, 점수를 부동소수점으로 명시적 지정
    for _, row in df.iterrows():
        product_name = str(row['goodsNm'])  # 명시적으로 문자열로 변환
        score = row.get('score', 0.0)

        # 상품명이 문자열로 처리되었는지 확인 후 접미사 배열 생성
        if isinstance(product_name, str):
            suffix_array = build_suffix_array(product_name)
            match_positions = search_patterns_in_text(suffix_array, product_name, pattern.lower())

            if match_positions:
                products_with_scores.append((product_name, score))

    sorted_products = sorted(products_with_scores, key=lambda x: x[1], reverse=True)[:20]
    pattern_to_remove = r'\[.*?\]|\(.*?\)'
    cleaned_products = [(re.sub(pattern_to_remove, '', product), score) for product, score in sorted_products]

    end_time = time.time()  # 처리 종료 시간 측정
    elapsed_time = end_time - start_time  # 경과 시간 계산

    print(f"검색 완료까지 걸린 시간: {elapsed_time:.2f}초")

    return [product for product, score in cleaned_products]
