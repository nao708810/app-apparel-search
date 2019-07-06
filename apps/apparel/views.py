"""
Controller
"""

import os
from flask import request, redirect, url_for, render_template, session
from apparel import app

#Mainルート
@app.route('/')
def start():
    """初期化後にsampleページに遷移"""
    init()
    return redirect(url_for('upload'))

#Sample Start
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """画像アップロードページを表示"""

    return render_template('upload.html')

#初期化用
def init():
    """セッション情報初期化処理"""
    app.secret_key = os.urandom(32)
