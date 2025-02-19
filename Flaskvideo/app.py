from flask import Flask, redirect, url_for, request, render_template, session
from flask_session import Session
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from bson.datetime_ms import DatetimeMS
from datetime import datetime

import auth
import os
from mongoutils import get_client_and_db

UPLOAD_FOLDER = 'static/assets/'

app = Flask(__name__)
app.config['SECRET_KEY'] = '3e4a268a5eba45057bf77e03b04d73ce9fdb335578226d33d33aef008a07190d'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Session(app)

@app.route('/')
def index():  # put application's code here
    _, db = get_client_and_db()
    feed = db.videos.find({})
    return render_template('index.html', user=auth.get_current_user(), feed=feed)

@app.route('/videos/<oid>')
def videos(oid):
    _, db = get_client_and_db()
    video = db.videos.find_one({'_id': ObjectId(oid)})
    video['uploader'] = db.users.find_one(video['uploader'])
    video['liked'] = False
    video['disliked'] = False
    return render_template('video.html', user=auth.get_current_user(), video=video, comments=[], recommendations=[])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        _, db = get_client_and_db()
        thumb = request.files.get('thumb', None)
        video = request.files.get('video', None)
        thumb.save(f'static/assets/thumbnails/{thumb.filename}')
        video.save(f'static/assets/videos/{video.filename}')
        print(request.form)
        # 400 bad request
        result = db.videos.insert_one({
            'title': request.form['title'],
            'description': request.form['desc'],
            'thumbnail': f'assets/thumbnails/{thumb.filename}',
            'source': f'assets/videos/{video.filename}',
            'uploader': ObjectId('664efdf60ece02b75907d810'),
            'view_count': 0,
            'like_count': 0,
            'dislike_count': 0,
            'tags': [],
            'creation_timestamp': DatetimeMS(datetime.now())
        })
        print('b')
        return redirect(url_for('videos', oid=str(result.inserted_id)))
    return render_template('upload_video.html', user=auth.get_current_user())

if __name__ == '__main__':
    app.run()
