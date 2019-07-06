"""
create app
"""

from flask import Flask, session

app = Flask(__name__)
app.config.from_object('apparel.config')

import apparel.views
