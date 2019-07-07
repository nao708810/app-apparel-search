"""
Controller
"""

import os
from flask import request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from apparel.models.customvision import Customvision
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
    message = ""
    if request.method == 'POST':
        # ファイルがなかった場合の処理
        if 'file' not in request.files:
            message = "ファイルがアップされていません"
        # データの取り出し
        else:
            file = request.files['file']
            # ファイル名がなかった時の処理
            if file.filename == '':
                message = "ファイル名がありません"
            # ファイルのチェック
            elif file and allwed_file(file.filename):
                # 危険な文字を削除（サニタイズ処理）
                filename = secure_filename(file.filename)
                # ファイルの保存
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                session['filename'] = filename
                # アップロード後のページに転送
                return redirect(url_for('result'))

    return render_template('upload.html', message=message)

#Sample Start
@app.route('/result', methods=['GET', 'POST'])
def result():
    """解析結果を表示"""
    #AI分析結果をエンティティに更新（未実装）
    customvision = Customvision(app.config['TRAINING_KEY'], app.config['PREDICTION_KEY'],\
        app.config['ENDPOINT'], app.config['VISION_PROJECT_NAME'],\
            app.config['PUBLISH_ITERATION_NAME'])
    image_path = app.config['UPLOAD_FOLDER'] + "/" + session['filename']
    prediction = customvision.get_prediction(image_path)





#初期化用
def init():
    """セッション情報初期化処理"""
    app.secret_key = os.urandom(32)

def allwed_file(filename):
    """ .があるかどうかのチェックと、拡張子の確認
    OKなら１、だめなら0
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in\
     app.config['ALLOWED_EXTENSIONS']
