from flask import Flask

app = Flask(__name__)
@app.route('/')

def index():
    return "Hello from Dave 27/04/2024"

if __name__ == "__main__":
    app.run(debug=True)