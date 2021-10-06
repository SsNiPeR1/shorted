from project.forms import UrlForm
from flask import Flask, render_template, redirect, url_for, request, session
import config
import hashlib

app = Flask(__name__)
app.config.from_object(config.Config)
app.config['SECRET_KEY'] = "Secret key for flask app."
app.config['RECAPTCHA_USE_SSL'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc6r6EcAAAAAEaUwknkIcXAutqPBwon4lLqfivj'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'YOUR_PRIVATE_KEY'
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}
urls = {}


def short(url):
    global urls
    url = url.encode()
    short = hashlib.sha512(url).hexdigest()[-6:]
    urls[short] = url.decode()
    return short


@app.route('/changetheme')
def themechanger():
	if 'theme' not in session or session['theme'] == "light":
		session['theme'] = "dark"
	elif session['theme'] == "dark":
		session['theme'] = "light"
	return redirect("/")

@app.route('/', methods=["GET"])
def enterUrl():
    form = UrlForm()
    return render_template("short.html", form=form)

@app.route('/', methods=["POST"])
def shortUrl():
    form = UrlForm()
    if form.validate_on_submit():
        url = form.url.data
        shorted = short(url)
        return render_template("readyurl.html", url=shorted)
    return render_template("short.html", form=form)

@app.route('/<url>')
def redir(url):
    if urls[url].startswith("http") or urls[url].startswith("https"):
        return redirect(f"{urls[url]}")
    else:
        return redirect(f"http://{urls[url]}")


if __name__ == '__main__':
    app.run()
