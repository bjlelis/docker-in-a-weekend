from flask import Flask
import redis

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

@app.route('/')
def hello():
    cache.incr('hits')
    count = cache.get('hits').decode('utf-8')
    return f'Hello! This page has been viewed {count} times.'