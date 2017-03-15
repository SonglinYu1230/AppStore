from flask import Flask, request, session, render_template, \
        url_for, abort, flash, Response, jsonify, redirect
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
    return redirect('/login')
    # return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request)
    print(request.form)
    error = None
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        return render_template('homepage.html')
    else:
        abort()

@app.route('/app/data', methods=['POST'])
def handleFile():
    print(request)
    print('request.files')
    print(request.files)
    imfile = request.files['ipa']
    imfile.save("/Users/Yu/Desktop/1.ipa")
    print(request.content_length)
    return jsonify({'status': 'OK'})

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
