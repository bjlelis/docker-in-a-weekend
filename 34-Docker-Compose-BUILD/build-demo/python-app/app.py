from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "V2: Hello, Docker Compose Build Demo"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
