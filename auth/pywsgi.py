from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from auth.app import app

# http_server = WSGIServer(('', 5000), app)
# http_server.serve_forever()