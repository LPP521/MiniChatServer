# coding=utf-8
from flask import Flask
from app import create_app

app = create_app()
if __name__ == '__main__':
    app.debug=True
    # 使得服务器对外部开放
    app.run(host='0.0.0.0')