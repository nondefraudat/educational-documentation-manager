from flask import Flask, jsonify, url_for

class RequestManager:
    def __init__(self, appName : str, dataAccessor, documentGenerator):
        self.__flaskInstance = Flask(appName)

    def run(self, host : str, port : int):
        self.__routes()
        self.__flaskInstance.run(host, port)

    def __routes(self):
        @self.__flaskInstance.route('/')
        @self.__flaskInstance.route('/index')
        def index():
            return jsonify({ "path": str(url_for('index')) })