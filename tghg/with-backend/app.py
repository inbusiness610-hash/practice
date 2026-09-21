import random
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Единственное место, где хранится и измеряется баланс
balance = 100
SYMBOLS = ['🍒', '🍋', '🍇', '🔔', '💎', '7️⃣']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/first.html')
def first_page():
    return render_template('first.html')


@app.route('/hr.html')
def hr_page():
    return render_template('hr.html')

@app.route('/api/state', methods=['GET'])
def get_state():
    # Отдаем текущий баланс из Python
    return jsonify({'balance': balance})


@app.route('/api/spin', methods=['POST'])
def spin():
    global balance
    data = request.get_json() or {}
    bet = data.get('bet', 10)

    # Проверка баланса происходить НА СЕРВЕРЕ
    if bet > balance or bet <= 0:
        return jsonify({
            'error': 'Недостаточно средств на сервере!',
            'balance': balance
        }), 400

    balance -= bet

    # Генерация символов
    reel_results = [[random.choice(SYMBOLS) for _ in range(3)] for _ in range(3)]

    # Проверка выигрышных линий
    lines = [
        [reel_results[0][0], reel_results[1][0], reel_results[2][0]],  # top
        [reel_results[0][1], reel_results[1][1], reel_results[2][1]],  # middle
        [reel_results[0][2], reel_results[1][2], reel_results[2][2]],  # bottom
        [reel_results[0][0], reel_results[0][1], reel_results[0][2]],  # reel 1
        [reel_results[1][0], reel_results[1][1], reel_results[1][2]],  # reel 2
        [reel_results[2][0], reel_results[2][1], reel_results[2][2]]   # reel 3
    ]

    total_win = 0
    winning_lines_count = 0

    for line in lines:
        if line[0] == line[1] == line[2]:
            total_win += bet * 5
            winning_lines_count += 1

    balance += total_win

    # Возвращаем обновленный баланс
    return jsonify({
        'balance': balance,
        'totalWin': total_win,
        'winningLinesCount': winning_lines_count,
        'reelResults': reel_results
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)