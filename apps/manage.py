"""
Flaskアプリケーションの起動エンドポイント
"""
from __future__ import print_function
from flask_bootstrap import Bootstrap
from apparel import app
from flask_session import Session

#Session
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

#Bootstrap
bootstrap = Bootstrap(app)

if __name__ == '__main__':
    app.run(debug=True)
