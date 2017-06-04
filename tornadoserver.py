import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import facedetect as fd
import facedetectfilter as fdf
from urlparse import urlparse
import json

clients = []
auto = True
filter_mode = False
left = False
right = False
up = False
down = False


class CamSocketHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		#parsed_origin = urlparse(origin)
		#print parsed_origin
		#with open("socket_access.log", "a") as f:
		#	f.write(time.strftime("%c") + ": " + str(parsed_origin) + "\n")
		return True

	def open(self):
		print("CamSocket opened")

	def on_message(self, message):
		print "received image: " + message
		#center_face=fd.facedetect(message)
		center_face = "message received"
		print(center_face)
		self.write_message(center_face)
		update_clients()

	def on_close(self):
		print("CamSocket closed")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		parsed_origin = urlparse(origin)

		# some restrictions on origin, ip included for testing
		return parsed_origin.netloc.endswith("ec2-52-15-48-211.us-east-2.compute.amazonaws.com") or parsed_origin.netloc.endswith("52.15.48.211") or parsed_origin.netloc.endswith("kfcams.me")
	
	def open(self):
		global auto	
		auto = False
		print("WebSocket opened")
		clients.append(self)

	def on_message(self, message):
		global auto
		global filter_mode
		global up
		global down
		global right
		global left

		data = json.loads(message)
		
		# Check for tracking mode
		if 'mode' in data:
			if data['mode'] == 'auto':
				auto = True
				print "auto mode"
			elif data['mode'] == 'manual':
				auto = False
				print "manual mode"

		# Check for manual mode commands
		elif 'command' in data:
			if data['command'] == 'up':
				up = True
				down = False
			elif data['command'] == 'down':
				down = True
				up = False
			elif data['command'] == 'left':
				left = True
				right = False
			elif data['command'] == 'right':
				right = True
				left = False
		
		# Check for filter selection
		elif 'fmode' in data:
			if data['fmode'] == 'on':
				filter_mode = True
				print "filters on"
			elif data['fmode'] == 'off':
				filter_mode = False
				print "filters off"

	def on_close(self):
		print("WebSocket closed")
		clients.remove(self)


class MainHandler(tornado.web.RequestHandler):
	def post(self):

		global up
		global down
		global left
		global right

		if self.request.headers["Content-Type"]=='imagebin':
			if auto:
				image = self.request.body
				if filter_mode:
					command = fdf.facedetect(image)
				else:
					command = fd.facedetect(image)
				self.write(command)
				update_clients()

			else:
				image = self.request.body

				if filter_mode:
					fdf.facedetect(image)
				else:
					fd.facedetect(image)

				command = [0,0,0,0]

				if up:
					command[1] = 1
					command[3] = 1
					up = False
				elif down:
					command[1] = 1
					down = False
				if left:
					command[0] = 1
					left = False
				elif right:
					command[0] = 1
					command[2] = 1
					right = False
				
				cmd = "cmd="+"".join(str(x) for x in command)
				self.write(cmd)
				update_clients()

		else:
			print(self.request.headers)
			print(self.request.body)
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
