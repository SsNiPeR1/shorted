from project.forms import UrlForm
from flask import Flask, render_template, redirect, url_for, request
import config
import hashlib

app = Flask(__name__)
app.config.from_object(config.Config)
urls = {}


def short(url):
    global urls
    url = url.encode()
    short = hashlib.sha512(url).hexdigest()[-6:]
    urls[short] = url.decode()
    return short




@app.route('/', methods=["GET", "POST"])
def shortUrl():
    form = UrlForm()
    if form.validate_on_submit():
        url = form.url.data
        shorted = short(url)
        return render_template("readyurl.html", url=shorted)
    return render_template("short.html", form=form)

@app.route("/redirect")
def redir():
    arg = request.args.get("url")
    if urls[arg].startswith("http") or urls[arg].startswith("https"):
        return redirect(f"{urls[arg]}")
    else:
        return redirect(f"https://{urls[arg]}")


if __name__ == '__main__':
    app.run()
