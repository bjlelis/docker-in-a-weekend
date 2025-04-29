from flask import Flask, render_template
import os

app = Flask(__name__)

# Get the environment variable APP_ENVIRONMENT (default to 'dev')
environment = os.getenv('APP_ENVIRONMENT', 'dev')

@app.route('/')
def home():
    # Serve different templates based on environment
    if environment == 'dev':
        return render_template('dev.html')
    elif environment == 'qa':
        return render_template('qa.html')
    else:
        return "<h1>Unknown Environment</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
