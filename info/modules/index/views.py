from . import index_blue
from flask import render_template,current_app

@index_blue.route('/')
def index():
    # 渲染主页
    return render_template('news/index.html')

@index_blue.route('/favicon.ico',methods=['GET'])
def favicon():
    # title左侧的图标
    return current_app.send_static_file('news/favicon.ico')