from flask import Flask, jsonify, abort
from flask import request

app = Flask(__name__)

# A1G
@app.route('/squared/<int:n>')
def square_one_number(n):
    return jsonify(result=n * n)

# A1F
@app.route('/immutable')
def get_immutable():
    data = (1, 2, 3)
    return jsonify(result=data)

# A1E
class Number:
    def __init__(self, value):
        self.value = value

    def double(self):
        return self.value * 2

@app.route('/double_oo/<int:n>')
def double_oo(n):
    number = Number(n)
    return jsonify(result=number.double())

def double_number(value):
    return value * 2

@app.route('/double_procedural/<int:n>')
def double_procedural(n):
    return jsonify(result=double_number(n))

@app.route('/double_functional')
def double_functional():
    numbers = [1, 2, 3]
    doubled = list(map(lambda x: x*2, numbers))
    return jsonify(result=doubled)

# B1G
@app.route('/gcd/<int:a>/<int:b>')
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return jsonify(result=a)

# B1F
def square(n):
    return n * n

def cube(n):
    return n * n * n

@app.route('/calculate_values', methods=['POST'])
def calculate_values():
    numbers = request.json.get('numbers', [])
    squared_values = [square(n) for n in numbers]
    cubed_values = [cube(n) for n in numbers]
    return jsonify(squared=squared_values, cubed=cubed_values)

# B1E
def find_max(numbers):
    max_number = numbers[0]
    for number in numbers:
        if number > max_number:
            max_number = number
    return max_number

@app.route('/max/<numbers>')
def max_of_numbers(numbers):
    numbers_list = [int(number) for number in numbers.split(',')]
    return {'Maximum': find_max(numbers_list)}

# B2G
def greet(name):
    return f'Hello, {name}!'

def farewell(name):
    return f'Goodbye, {name}!'

@app.route('/<action>/<name>')
def handle_action(action, name):
    actions = {'greet': greet, 'farewell': farewell}
    return actions[action](name)

# B2F
def log_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__} aufgerufen mit {args}, Ergebnis: {result}")
        return result
    return wrapper

def add(x, y):
    return x + y

@app.route('/add/<int:x>/<int:y>')
@log_decorator
def add_route(x, y):
    return {'Ergebnis': add(x, y)}

# B2E
def make_multiplier(factor):
    def multiplier(number):
        return number * factor
    return multiplier

triple = make_multiplier(3)

def apply_triple(number):
    return triple(number)

@app.route('/triple/<int:number>')
def triple_route(number):
    return {'Result': apply_triple(number)}

# B3G
squared = lambda x: x * x

uppercase = lambda s: s.upper()

@app.route('/square/<int:number>')
def square_number(number):
    return {'Quadrat': squared(number)}

@app.route('/uppercase/<string:text>')
def uppercase_text(text):
    return {'Großbuchstaben': uppercase(text)}

# B3F
add = lambda x, y: x + y

max_number = lambda x, y: x if x > y else y

@app.route('/add/<int:x>/<int:y>')
def add_numbers(x, y):
    return {'Summe': add(x, y)}

@app.route('/max/<int:x>/<int:y>')
def max_of_two_numbers(x, y):
    return {'Maximum': max_number(x, y)}

# B3E
sort_by_second = lambda item: item[1]

tuple_list = [(1, 'd'), (2, 'b'), (3, 'c'), (4, 'a')]

@app.route('/sort-tuples')
def sort_tuples():
    sorted_list = sorted(tuple_list, key=sort_by_second)
    return {'Sortierte Liste': sorted_list}

# B4G
from functools import reduce

numbers = [1, 2, 3, 4, 5]
squared_numbers = map(lambda x: x**2, numbers)

even_numbers = filter(lambda x: x % 2 == 0, numbers)

sum_of_numbers = reduce(lambda x, y: x + y, numbers)

@app.route('/squared')
def show_squared_numbers():
    return {'Quadrat Zahlen': list(squared_numbers)}

@app.route('/even')
def show_even_numbers():
    return {'Gerade Zahlen': list(even_numbers)}

@app.route('/sum')
def show_sum_of_numbers():
    return {'Summe': sum_of_numbers}

# B4F
people = [
    {'name': 'Alice', 'age': 25, 'score': 88},
    {'name': 'Bob', 'age': 30, 'score': 75},
    {'name': 'Charlie', 'age': 35, 'score': 93},
]

# 1. 'filter' findet alle Personen über 27 Jahre.
# 2. 'map' wandelt das gefilterte Ergebnis in eine Liste von Scores um.
# 3. 'reduce' berechnet die durchschnittliche Punktzahl der gefilterten Gruppe.
average_score = reduce(
    lambda x, y: x + y,
    map(lambda person: person['score'],
        filter(lambda person: person['age'] > 27, people))
) / len(people)

@app.route('/average-score')
def show_average_score():
    return {'Durchschnittliche Punktzahl': average_score}

# B4E
orders = [
    {'id': 1, 'amount': 25},
    {'id': 2, 'amount': 15},
    {'id': 3, 'amount': 30},
    {'id': 4, 'amount': 10},
]

amounts = map(lambda order: order['amount'], orders)

large_amounts = filter(lambda amount: amount > 20, amounts)

total_large_amounts = reduce(lambda x, y: x + y, large_amounts)

@app.route('/total')
def calculate_total():
    return {'Total of Large Amounts': total_large_amounts}

# C1G
def average_of_first_two(nums):
    return sum(nums[:2]) / 2

def validate_numbers(nums):
    if len(nums) <= 10:
        abort(400, description='Nicht genug Daten')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    nums = data.get('numbers')

    if not nums:
        abort(400, description='Fehlende Daten')

    validate_numbers(nums)
    result = average_of_first_two(nums)
    message = 'Ergebnis größer als 5' if result > 5 else 'Ergebnis 5 oder kleiner'
    return jsonify({'message': message})

# C1F
@app.route('/average')
def average():
    values = request.args.getlist('values', type=int)
    if len(values) != 4:
        abort(400, description="Es müssen genau vier Werte bereitgestellt werden.")
    average_result = calculate_average(values)
    return jsonify({'Durchschnitt': average_result})

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

# C1E
@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.form.get('data')
    if not data:
        return "Keine Daten zum Speichern.", 400

    processed_data = process_input(data)
    if not processed_data:
        return "Datenverarbeitung fehlgeschlagen.", 500

    return "Daten gespeichert."

def process_input(input_data):
    try:
        return input_data.upper()
    except AttributeError:
        return None

# Tests nach dem Refactoring
def test_submit_form_no_data():
    with app.test_client() as client:
        response = client.post('/submit', data={})
        assert response.status_code == 400

def test_submit_form_success():
    with app.test_client() as client:
        response = client.post('/submit', data={'data': 'test'})
        assert response.status_code == 200
        assert response.data == b"Daten gespeichert."


if __name__ == '__main__':
    app.run()
