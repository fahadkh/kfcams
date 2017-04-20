import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import facedetect as fd
from urlparse import urlparse

clients = []


class CamSocketHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		parsed_origin = urlparse(origin)
		print parsed_origin
		with open("socket_access.log", "a") as f:
			f.write(time.strftime("%c") + ": " + str(parsed_origin) + "\n")
		return True

	def open(self):
		print("CamSocket opened")

	def on_message(self, message):
		print "received image: " + message
		center_face=fd.facedetect(message)
		print(center_face)
		self.write(center_face)
		update_clients()

	def on_close(self):
		print("CamSocket closed")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		parsed_origin = urlparse(origin)
		return parsed_origin.netloc.endswith("ec2-13-58-118-151.us-east-2.compute.amazonaws.com") or parsed_origin.netloc.endswith("13.58.118.151")
	
	def open(self):
		print("WebSocket opened")
		clients.append(self)

	def on_message(self, message):
		self.write_message(u"You said: " + message)

	def on_close(self):
		print("WebSocket closed")
		clients.remove(self)


class MainHandler(tornado.web.RequestHandler):
	def post(self):
		image = self.request.body
		center_face = fd.facedetect(image)
		print(center_face)
		self.write(center_face)
		update_clients()
	get = post
	

def update_clients():
	for client in clients:
		client.write_message(".")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
		(r"/socket", WebSocketHandler),
		(r"/camsocket", CamSocketHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
