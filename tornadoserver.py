import tornado.ioloop
import tornado.web
import facedetect as fd

class MainHandler(tornado.web.RequestHandler):
	def post(self):
		image = self.get_argument('image', '')
		center_face = fd.facedetect(image)
		self.write(center_face)
	get = post
	


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
