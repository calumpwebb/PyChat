# from flask import Flask, request
# from flask_socketio import Namespace, SocketIO, emit
#
# app = Flask(__name__)
# # todo: change SECRET_KEY
# app.config["SECRET_KEY"] = "secret! pls change"
# socketio = SocketIO(app)
#
# users = set()
# messages = []
#
#
# class Main(Namespace):
#     @staticmethod
#     def get_sid():
#         return request.sid
#
#     def on_connect(self):
#         sid = self.get_sid()
#         users.add(sid)
#         print("number of users", len(users))
#         return sid
#
#     def on_disconnect(self):
#         sid = self.get_sid()
#         users.remove(sid)
#         print("number of users", len(users))
#
#     def on_message(self, data):
#         print("i got a message")
#
#         emit("new_message", data, broadcast=True)
#
#
# socketio.on_namespace(Main("/"))
#
#
# if __name__ == "__main__":
#     app.run()
#     socketio.run(app, host="0.0.0.0")
