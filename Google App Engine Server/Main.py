import os
import cgi
import datetime
import webapp2
import jinja2

from google.appengine.ext import db
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), extensions=['jinja2.ext.autoescape'])

class RaspberryPiInfo(db.Model):
  temperature = db.TextProperty()
  luminosity = db.TextProperty()
  date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
  def get(self):
    infoAll = RaspberryPiInfo.all()   
    infoAll.order("-date")
    infoList = infoAll.fetch(limit=15)

    latestInsertDate = infoList[0].date

    if((datetime.datetime.now() - latestInsertDate) > datetime.timedelta(seconds=12)) :
      available = "OFFLINE"
    else :
      available = "ONLINE"

    template_values = {'infoList': infoList, 'available' : available}

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))

class CollectInfo(webapp2.RequestHandler):
  def post(self):
    info = RaspberryPiInfo()
    info.temperature = self.request.get('temperature')
    info.luminosity = self.request.get('luminosity')
    info.put()

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/CollectInfo', CollectInfo)
], debug=True)
