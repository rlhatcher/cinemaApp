#!/usr/bin/env python

import functools
import markdown
import os.path
import re
import tornado.web
import tornado.wsgi
import unicodedata
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import db


class Entry(db.Model):
    """A single blog entry."""
    author = db.UserProperty()
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    markdown = db.TextProperty(required=True)
    html = db.TextProperty(required=True)
    published = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)


def administrator(method):
    """Decorate with this method to restrict to site admins."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method == "GET":
                self.redirect(self.get_login_url())
                return
            raise tornado.web.HTTPError(403)
        elif not self.current_user.administrator:
            if self.request.method == "GET":
                self.redirect("/")
                return
            raise tornado.web.HTTPError(403)
        else:
            return method(self, *args, **kwargs)
    return wrapper


class BaseHandler(tornado.web.RequestHandler):
    """Implements Google Accounts authentication methods."""
    def get_current_user(self):
        user = users.get_current_user()
        if user: user.administrator = users.is_current_user_admin()
        return user

    def get_login_url(self):
        return users.create_login_url(self.request.uri)

    def render_string(self, template_name, **kwargs):
        # Let the templates access the users module to generate login URLs
        return tornado.web.RequestHandler.render_string(
            self, template_name, users=users, **kwargs)

class HomeHandler(BaseHandler):
	def get(self):
		self.render("home.html")
	
class EntryHandler(BaseHandler):
    def get(self, slug):
        entry = db.Query(Entry).filter("slug =", slug).get()
        if not entry: raise tornado.web.HTTPError(404)
        self.render("entry.html", entry=entry)


class ArchiveHandler(BaseHandler):
    def get(self):
        entries = db.Query(Entry).order('-published')
        self.render("archive.html", entries=entries)


class FeedHandler(BaseHandler):
    def get(self):
        entries = db.Query(Entry).order('-published').fetch(limit=10)
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", entries=entries)


class ComposeHandler(BaseHandler):
    @administrator
    def get(self):
        key = self.get_argument("key", None)
        entry = Entry.get(key) if key else None
        self.render("compose.html", entry=entry)

    @administrator
    def post(self):
        key = self.get_argument("key", None)
        if key:
            entry = Entry.get(key)
            entry.title = self.get_argument("title")
            entry.markdown = self.get_argument("markdown")
            entry.html = markdown.markdown(self.get_argument("markdown"))
        else:
            title = self.get_argument("title")
            slug = unicodedata.normalize("NFKD", title).encode(
                "ascii", "ignore")
            slug = re.sub(r"[^\w]+", " ", slug)
            slug = "-".join(slug.lower().strip().split())
            if not slug: slug = "entry"
            while True:
                existing = db.Query(Entry).filter("slug =", slug).get()
                if not existing or str(existing.key()) == key:
                    break
                slug += "-2"
            entry = Entry(
                author=self.current_user,
                title=title,
                slug=slug,
                markdown=self.get_argument("markdown"),
                html=markdown.markdown(self.get_argument("markdown")),
            )
        entry.put()
        self.redirect("/entry/" + entry.slug)


class FilmModule(tornado.web.UIModule):
    def render(self, movie):
        return self.render_string("modules/film.html", movie=movie)


settings = {
    "cinema_name": u"The Royal Cinema",
    "cinema_location": u"Faversham",
    "cinema_title": u"The Royal Cinema Faversham",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "ui_modules": {"Film": FilmModule},
    "xsrf_cookies": True,
}
application = tornado.wsgi.WSGIApplication([
    (r"/", HomeHandler),
    (r"/archive", ArchiveHandler),
    (r"/feed", FeedHandler),
    (r"/entry/([^/]+)", EntryHandler),
    (r"/compose", ComposeHandler),
], **settings)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == "__main__":
    main()
