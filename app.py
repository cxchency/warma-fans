from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('nav_items.json', 'r', encoding='utf-8') as f:
        nav_items = json.load(f)
    rendered_html = render_template('index.html', nav_items=nav_items)
    return rendered_html

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
