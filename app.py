from flask import Flask, request, jsonify, render_template, url_for
import redis
import re

from data.autocomplete_data2 import search_by_keyword

# autocomplete_date2.py에서 정의된 함수를 가져오도록 수정해야 할 수 있습니다.

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    suggestions = []

    if search:
        # search_by_keyword 함수를 사용하여 검색어에 해당하는 자동완성 키워드를 조회
        suggestions = search_by_keyword(search)

        # 정규 표현식 패턴
        pattern = r'\[.*?\]|\(.*?\)'

        # 괄호와 괄호 안의 텍스트 제거를 위해 리스트 컴프리헨션 사용
        cleaned_suggestions = [re.sub(pattern, '', suggestion) for suggestion in suggestions]

        # 정제된 키워드로 suggestions 업데이트
        suggestions = cleaned_suggestions

    return jsonify(matching_results=suggestions)


@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('q', '')  # 검색어를 받습니다.
    results = []
    if query:
        results = search_by_keyword(query)
    return render_template('index.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
