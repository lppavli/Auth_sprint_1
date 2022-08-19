from gevent import monkey

monkey.patch_all()

from auth.app import create_app

app = create_app()
# http_server = WSGIServer(('', 5000), app)
# http_server.serve_forever()
