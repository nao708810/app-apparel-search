"""
Controller
"""

import os
from urllib import parse
from flask import request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from apparel.models.blob import Blob
from apparel.models.customvision import Customvision
from apparel import app


#Mainルート
@app.route('/', methods=['GET', 'POST'])
def start():
    """初期化後にホームページに遷移。
    POSTであれば次ページへ
    """
    if request.method == 'POST':
        return redirect(url_for('upload'))
    init()
    return render_template('home.html')

#画像アップロードページ
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

                #--Blobへの画像アップロード(インスタンス生成含む)
                blob = Blob(app.config['STORAGE_NAME'], app.config['STORAGE_KEY'])
                blob.upload_image(app.config['BLOB_NAME'], filename, \
                    os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #ファイル名をセッションに格納
                session['filename'] = filename
                # AI解析結果メソッドにリダイレクト
                return redirect(url_for('result'))

    return render_template('upload.html', message=message)

#AI解析結果
@app.route('/result', methods=['GET', 'POST'])
def result():
    """AI解析結果を表示"""
    #画像解析API操作クラスのインスタンス生成
    customvision = Customvision(app.config['TRAINING_KEY'], app.config['PREDICTION_KEY'],\
        app.config['ENDPOINT'], app.config['VISION_PROJECT_NAME'],\
            app.config['PUBLISH_ITERATION_NAME'])
    #画像取得先URL生成（BLOB_URL）
    blob_url = app.config['BLOB_URL'] + session['filename']
    #Azure上で学習済みAIに画像解析をさせて結果を取得
    predictions = customvision.get_prediction(blob_url)

    #HTML表示情報生成
    keyword = get_keyword(predictions)
    predictions = get_disp_prediction(predictions)


    return render_template('result.html', predictions=predictions, keyword=keyword)



#初期化用
def init():
    """セッション情報初期化処理"""
    app.secret_key = os.urandom(32)
    session.pop('filename', None)

#ファイル名チェック処理
def allwed_file(filename):
    """
    .があるかどうかのチェックと、拡張子の確認
    OKなら１、だめなら0
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in\
     app.config['ALLOWED_EXTENSIONS']

#HTML表示用の予測結果を生成(リスト)
def get_disp_prediction(predictions):
    '''HTML表示用の予測結果を生成'''
    ret_list = []
    for prediction in predictions:
        #適合率を%表記に直して少数第３位まで表示
        temp_float = prediction.probability * 100
        prediction.probability = round(temp_float, 3)
        #返却用のリストに追加
        ret_list.append(prediction)
    return ret_list

#アパレルサイト検索キーワード生成
def get_keyword(predictions):
    '''アパレルサイト検索キーワード生成'''
    keyword = app.config['APPAREL_URL']
    for prediction in predictions:
        if prediction.probability > 0.5:
            #URL用に検索文字列をエンコード
            temp = parse.quote(prediction.tag_name, encoding='shift-jis')
            keyword = keyword + " " + temp
    return keyword
