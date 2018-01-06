from flask import Flask, render_template, request
from sudoku import *
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
	entries = [request.form[str(x)] for x in range(1, 82)]
	game = [0 if x == "" else int(x) for x in entries]
	sudoku_game = Game(game)
	solved = sudoku_game.solve()
	return render_template('solution.html', solution=solved)

if __name__ == "__main__":
    app.run()
    