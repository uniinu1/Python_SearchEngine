from flask import Flask, request, jsonify, render_template, url_for
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    suggestions = []

    # Redis에서 접두사에 해당하는 자동완성 키워드를 점수가 높은 순으로 조회
    if search:
        #ZREVRANGE : Redis의 Sorted Set 데이터 구조에서 사용되며, 지정된 범위의 요소들을 점수가 높은 순서(내림차순)로 가져옵니다.
        results = r.zrevrange(f'autocomplete:{search}', 0, -1, withscores=False)
        suggestions = [result.decode('utf-8') for result in results]

    return jsonify(matching_results=suggestions)



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
