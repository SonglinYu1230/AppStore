from flask import Flask, request, session, render_template, \
        url_for, abort, flash, Response, jsonify, redirect
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
    # print('login')
    return render_template('stylebox.html')
    # return send_static_file('stylebox.html')
    # return 'Hello World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(__name__)
    error = None
    if request.method == 'POST':
        data = {'name': 'Tom',
                "address": "NYC"}
        # return Response(json.dumps(data), mimetype='application/json')
        return  jsonify(data)
    return render_template('login.html', error=error)

@app.route('/user/<name>')
def user(name):
    return render_template('page.html', user=name)
    # if name == 'baidu':
    #     return redirect('https://www.baidu.com')
    # elif name == 'google':
    #     return redirect('https://www.google.com/ncr')
    # elif name == 'NO':
    #     return abort(404)
    # return '<h1> Hello, %s <h1>' % name

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
