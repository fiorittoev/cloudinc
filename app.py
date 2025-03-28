from flask import Flask

app=Flask

@app.route('/')
def index():
    return "Landing Page"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)