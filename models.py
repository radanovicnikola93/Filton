from google.appengine.ext import ndb

class GuestBook(ndb.Model):
    fullname = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.StringProperty()
    entrymade = ndb.DateTimeProperty(auto_now_add=True)