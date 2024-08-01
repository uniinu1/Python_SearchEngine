from flask import Flask, request, jsonify, render_template, url_for
import redis

# 이 경로가 정확해야 합니다. 프로젝트 구조에 따라 다를 수 있습니다.
from data.suffix_data import search_by_keyword

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    suggestions = []

    if search:
        # CSV 파일의 실제 경로로 변경해야 합니다.
        file_path = '/Users/smpark/Documents/all.xlsx'
        # 올바르게 함수를 호출하도록 수정했습니다.
        suggestions = search_by_keyword(file_path, search)
    return jsonify(matching_results=suggestions)

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('q', '')
    results = []
    if query:
        # CSV 파일의 실제 경로로 변경해야 합니다.
        file_path = '/Users/smpark/Documents/all.xlsx'
        results = search_by_keyword(file_path, query)
    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)