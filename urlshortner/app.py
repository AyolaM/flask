# import main Flask class and request object. render template tells it to look at template file
# redirect and url_for are for redirecting to whatever page using the function name
# abort is for error code, 404
# session stores cookies
import code
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session
import json
import os.path
from werkzeug.utils import secure_filename

# create the Flask app
app = Flask(__name__)
app.secret_key = 'nfhueygegs73gfug'


@app.route('/')
def home():
    return render_template('home.html', codes=session.keys())

# route() enter what URL we want to return data for


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That file name is already taken')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/ayola/Desktop/urlshortner/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        # urls[request.form['code']] = {'url': request.form['url']}
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            # session stores cookies
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])

    else:
        return redirect(url_for('home'))

    @app.route('/<string:code>')
    def redirect_to_url(code):
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
                if code in urls.keys():
                    if 'url' in urls[code].keys():
                        return redirect(urls[code]['url'])
                    else:

                        return redirect(url_for('static', filename='user_files/' +
                                                urls[code]['file']))
        return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('Page not found'), 404
