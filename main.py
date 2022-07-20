from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/song-list')
def song_list():
    return render_template('song-list.html')


if __name__ == '__main__':
    app.run()
