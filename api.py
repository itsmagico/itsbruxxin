from flask import Flask, request, jsonify, g
import itertools
import time

app = Flask(__name__)
anagram_list = []

@app.before_request
def log_request_info():
    g.start_time = time.time()
    print(f"Recebido {request.method} em {request.path}")

@app.after_request
def add_custom_header(response):
    duration = time.time() - g.start_time
    response.headers["X-Response-Time"] = f"{duration:.3f}s"
    response.headers["X-Developer"] = "Itsbruxxin"
    return response

def generate_anagrams(word):
    return [''.join(p) for p in set(itertools.permutations(word))]

@app.route('/anagram', methods=['POST'])
def create_anagram():
    data = request.get_json()
    if not data or 'word' not in data:
        return jsonify({'error': 'Corpo da requisição deve conter "word"'}), 400

    word = data['word']
    anagrams = generate_anagrams(word)

    anagram_entry = {
        'word': word,
        'anagrams': anagrams
    }
    anagram_list.append(anagram_entry)

    return jsonify(anagram_entry), 201

@app.route('/anagrams', methods=['GET'])
def list_anagrams():
    return jsonify(anagram_list), 200

# NOVA ROTA - GET direto na URL
@app.route('/anagram/<word>', methods=['GET'])
def get_anagram_by_url(word):
    anagrams = generate_anagrams(word)

    anagram_entry = {
        'word': word,
        'anagrams': anagrams
    }
    return jsonify(anagram_entry), 200

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
