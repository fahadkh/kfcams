import tornado.ioloop
import tornado.web
import tornado.websocket
from urlparse import urlparse
import facedetect as fd

clients = []

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
		client.write_message("hi")
		print("sent message to client")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
		(r"/socket", WebSocketHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
