from pyramid.config import Configurator
from wsgiref.simple_server import make_server
from api.processing import pre,process

# web view functions is defined inside blueprints

# consist web management panel
class panel:
    # constructor
    def __init__(self, webapp_port, mysql_host, mysql_port=3306, mysql_user, mysql_passwd, mysql_db, log_file_obj):
        self.mysql_host = mysql_host
        self.mysql_port = int(mysql_port)
        self.mysql_user = mysql_user
        self.mysql_passwd = mysql_passwd
        self.mysql_db = mysql_db
        self.webapp_port = int(webapp_port)
        conf = Configurator()
        # index = login page
        conf.add_route('index',"/")
        conf.add_view(self.index, route_name='index')
        # panel = web panel, web app
        conf.add_route('panel','/panel')
        conf.add_view(self.panel, route_name='panel')
        self.app = conf.make_wsgi_app()
    
    # listening function
    def run(self):
        self.app = make_server('127.0.0.1', self.webapp_port, self.app)
        self.app.serve_forever()

# consists of API server and Post Server
# webapp_port is for API Server only
class server:
    # constructor
    def __init__(self, webapp_port, mysql_host, mysql_port=3306, mysql_user, mysql_passwd, mysql_db, log_file_obj):
        self.mysql_host = mysql_host
        self.mysql_port = int(mysql_port)
        self.mysql_user = mysql_user
        self.mysql_passwd = mysql_passwd
        self.mysql_db = mysql_db
        self.webapp_port = int(webapp_port)
        conf = Configurator()
        # API = API Server
        conf.add_route('API','/api_req')
        conf.add_view(self.API, route_name='API')
        self.app = conf.make_wsgi_app()
    
    # listening function
    def run(self):
        self.app = make_server('127.0.0.1', self.webapp_port, self.app)
        self.app.serve_forever()
    
    # web view function, API
    def API(self,request):
        # perform authentication first
        auth_key = request.POST['auth_key']
        req_type = request.POST['req_type']
        user,req_type = pre(self, auth_key, req_type)
