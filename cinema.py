#!/usr/bin/env python

import functools
import markdown
import os.path
import re
import tornado.web
import tornado.wsgi
import unicodedata
import wsgiref.handlers
import imdb

import traceback 

from google.appengine.api import users
from google.appengine.ext import db

class Movie(db.Model):
    imdbID = db.StringProperty()
    title = db.StringProperty()
    coverURL = db.StringProperty()
    plotOutline = db.StringProperty()
    category = db.CategoryProperty()

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

        self.render("ic/home.html")
        
class PopulateHandler(BaseHandler):
    """Populates default movie database objects"""
    def get(self):
        
        movie = Movie(key_name = "1504320",
                      imdbID = "1504320",
                      title = "The King's Speech",
                      plotOutline = "The story of King George VI of Britain, his impromptu ascension to the throne and the speech therapist who helped the unsure monarch become worthy of it.",
                      coverURL = "/static/images/1504320_250.jpg",
                      category = db.Category("Showing Now"))
                      
        movie.put()
        
        movie = Movie(key_name = "0076759",
                      imdbID = "0076759",
                      title = "Star Wars",
                      plotOutline = "Luke Skywalker leaves his home planet, teams up with other rebels, and tries to save Princess Leia from the evil clutches of Darth Vader.",
                      coverURL = "/static/images/0076759_250.jpg",
                      category = db.Category("Showing Now"))
        movie.put()

        movie = Movie(key_name = "0062622",
                      imdbID = "0062622",
                      title = "2001: A Space Odyssey",
                      plotOutline = "Mankind finds a mysterious, obviously artificial, artifact buried on the moon and, with the intelligent computer HAL, sets off on a quest.",
                      coverURL = "/static/images/0062622_250.jpg",
                      category = db.Category("Showing Now"))
                      
        movie.put()

class PurgeHandler(BaseHandler):
    """Remove all movies"""
    def get(self):
        
        movies = db.GqlQuery("SELECT * FROM Movie LIMIT 3")
        for movie in movies:
            movie.delete()
        
class CmsHandler(BaseHandler):
    """Fire up the CMS application"""
    def get(self):
        
        self.redirect("/static/cinemaCMS.html")

class rcfHomeHandler(BaseHandler):
    def get(self):
        movies = db.GqlQuery("SELECT * FROM Movie LIMIT 3")
        self.render("rcfHome.html", movies=movies)
        
class rcfShowingNowHandler(BaseHandler):
    """Display the Showing Now page for the Royal Cinema"""
    def get(self):
        movies = db.GqlQuery("SELECT * FROM Movie LIMIT 3")
        self.render("rcfShowingNow.html", movies=movies)
                                
class rcfComingSoonHandler(BaseHandler):
    """Display the Showing Now page for the Royal Cinema"""
    def get(self):
        movies = db.GqlQuery("SELECT * FROM Movie LIMIT 3")
        self.render("rcfComingSoon.html", movies=movies)

class rcfAboutUsHandler(BaseHandler):
    """Display the About Us page for the Royal Cinema"""
    def get(self):
        self.render("rcfAboutUs.html")

class rcfContactUsHandler(BaseHandler):
    """Display the About Us page for the Royal Cinema"""
    def get(self):
        self.render("rcfContactUs.html")

class FilmModule(tornado.web.UIModule):
    def render(self, movie):
        return self.render_string("modules/film.html", movie=movie)

class FilmDetailModule(tornado.web.UIModule):
    def render(self, movie):
        return self.render_string("modules/filmDetail.html", movie=movie)

settings = {
    "cinema_name": u"The Royal Cinema",
    "cinema_location": u"Faversham",
    "cinema_title": u"The Royal Cinema Faversham",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "ui_modules": {"Film": FilmModule,"FilmDetail": FilmDetailModule},
    "xsrf_cookies": True,
}

application = tornado.wsgi.WSGIApplication([
    (r"/", HomeHandler),
    (r"/populate", PopulateHandler),
    (r"/purge", PurgeHandler),
    (r"/cms", CmsHandler),
], **settings)

application.add_handlers(r"royalcinema\.independent-cinemas\.com", [
    (r"/", rcfHomeHandler),
    (r"/home", rcfHomeHandler),
    (r"/index.html", rcfHomeHandler),
    (r"/showingNow", rcfShowingNowHandler),
    (r"/comingSoon", rcfComingSoonHandler),
    (r"/aboutUs", rcfAboutUsHandler),
    (r"/contactUs", rcfContactUsHandler),
    ])

def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
