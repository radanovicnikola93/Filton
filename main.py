#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import GuestBook

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")


class RezultatHandler(BaseHandler):
    def post(self):
        fullname = self.request.get('fullname')
        email = self.request.get('email')
        message = self.request.get('message')


        guestbook = GuestBook(fullname=fullname, email=email, message=message)
        guestbook.put()

        return self.write(fullname)

class GuestBookHandler(BaseHandler):
    def get(self):
        list = GuestBook.query(GuestBook.delete == False).fetch()
        params = {'list': list}

        return self.render_template('guestbook.html', params=params)

class GuestbookDetails(BaseHandler):
    def get(self, guestbook_id):
        guestbook = GuestBook.get_by_id(int(guestbook_id))
        params = {'guestbook': guestbook}
        return self.render_template('single_guestbook_entry.html', params=params)

class ModifyGuestBookHandler(BaseHandler):
    def get(self, guestbook_id):
        guestbook = GuestBook.get_by_id(int(guestbook_id))
        params = {'guestbook': guestbook}
        return self.render_template('modify_guestbook.html', params=params)

    def post(self, guestbook_id):
        fullname = self.request.get('fullname')
        email = self.request.get('email')
        message = self.request.get('message')
        guestbook = GuestBook.get_by_id(int(guestbook_id))
        guestbook.fullname = fullname
        guestbook.email = email
        guestbook.message = message
        guestbook.put()
        return self.redirect_to('guestbook')

class DeleteGuestBookHandler(BaseHandler):
    def get(self, guestbook_id):
        guestbook = GuestBook.get_by_id(int(guestbook_id))
        params = {'guestbook': guestbook}
        return self.render_template('delete_guestbook.html', params=params)

    def post(self, guestbook_id):
        guestbook = GuestBook.get_by_id(int(guestbook_id))
        guestbook.delete = True
        guestbook.put()
        return self.redirect_to('guestbook')

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/guestbook', GuestBookHandler),
    webapp2.Route('/guestbook/<guestbook_id:\d+>', GuestbookDetails),
    webapp2.Route('/guestbook/<guestbook_id:\d+>/modify', ModifyGuestBookHandler),
    webapp2.Route('/guestbook/', GuestBookHandler, name='guestbook'),
    webapp2.Route('/guestbook/<guestbook_id:\d+>/delete', DeleteGuestBookHandler),
], debug=True)