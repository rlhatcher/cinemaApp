#!/usr/bin/env python

import functools
import markdown
import os.path
import re
import tornado.web
import tornado.wsgi
import unicodedata
import wsgiref.handlers
import logging

from tornado import escape
from imdb import Person
from imdb import IMDb
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import images

class Movie(db.Model):
    imdbID = db.StringProperty()
    title = db.StringProperty()
    year = db.StringProperty()
    plotOutline = db.StringProperty()
    plot = db.TextProperty()
    picture = db.BlobProperty(default=None)
    director = db.StringListProperty()
    writer = db.StringListProperty()
    cast = db.StringListProperty()
    certificates = db.StringListProperty()
    category = db.CategoryProperty()
    runtimes = db.StringListProperty()

    def cert(self, country):
        for cert in self.certificates:
            i = cert.find('::')
            if i != -1:
                cert = cert[:i]
            i = cert.find(country)
            if i != -1:
                j = cert.find(':')
                return cert[j+1:]
        return "Unknown"

    def get_cast(self, limit=5, joiner=u', '):
        if len(self.cast) == 0 : return "Not Available"
        cast = self.cast[:limit]
        return joiner.join(cast)

    def get_director(self, limit=5, joiner=u', '):
        if len(self.director) == 0 : return "Not Available"
        director = self.director[:limit]
        return joiner.join(director)

    def get_writer(self, limit=5, joiner=u', '):
        if len(self.writer) == 0 : return "Not Available"
        writer = self.writer[:limit]
        return joiner.join(writer)

    def get_runtime(self):
        return self.runtimes[0]

class Subscriber(db.Model):
    """A mailing list subscriber"""
    emailAddres = db.StringProperty();

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
        self.redirect("cms/index.html")

class ImdbHandler(BaseHandler):
    """ Manages Showing now films http://127.0.0.1:8000/showingNow?action=store&id=1504320 """
    def _findPlot(self, movie):
        """ Find and return the most suitable plot information from a movie """
        plot = movie.get('plot')
        if not plot:
            plot = movie.get('plot outline')
            if plot:
                plot = [plot]
        if plot:
            plot = plot[0]
            i = plot.find('::')
            if i != -1:
                plot = plot[:i]
        return plot

    def _moviePoster(self, movie):
        """ Find the best poster for a movie """
        pictureFile = urlfetch.Fetch(movie.get('full-size cover url')).content

        # If we can't fina a poster then use the not avaiable image
        if not pictureFile:
            pictureFile = urlfetch.Fetch('/image/notavailable.jpg').content

        # Make all our images 500 pixels wide to avoid storing giant image blobs
        image = images.Image(pictureFile)
        image.resize(500)
        return image.execute_transforms(output_encoding=images.JPEG)

    def _personToString(self, personList):
        nl = []
        for person in personList:
            n = person.get('name', u'')
            if person.currentRole: n += u' (%s)' % person.currentRole
            nl.append(n)
        return nl

    def get(self):
        action = self.get_argument("action")

        if action == "store":
            ia = IMDb('http')
            imdbKey = self.get_argument("id")
            category = self.get_argument("cat", "SN")
            imdbMovie = ia.get_movie(imdbKey)

            movie = Movie(key_name = imdbMovie.movieID,
                          imdbID = imdbMovie.movieID,
                          title = imdbMovie.get('title', u'Not Available'),
                          year = str(imdbMovie.get('year')),
                          plotOutline = imdbMovie.get('plot outline'),
                          plot = self._findPlot(imdbMovie),
                          picture = db.Blob(self._moviePoster(imdbMovie)),
                          director = self._personToString(imdbMovie.get('director')),
                          writer = self._personToString(imdbMovie.get('writer')),
                          cast = self._personToString(imdbMovie.get('cast')),
                          certificates  = imdbMovie.get('certificates'),
                          category = db.Category(category),
                          runtimes = imdbMovie.get('runtimes')
            )
            movie.put()

            filmJson = escape.json_encode({
                'id': movie.imdbID,
                'title':movie.title,
                'year':movie.year,
                'plotOutline':movie.plotOutline,
                'plot':movie.plot,
                'director':movie.director,
                'writer':movie.writer,
                'cast':movie.cast,
                'runtimes':movie.runtimes
            })

            logging.info(filmJson)
            self.write(filmJson)

        if action == "search":
            ia = IMDb('http')
            movies = []

            for movie in ia.search_movie(self.get_argument("title")):
                movies.append({'id': movie.movieID,'title':movie.get('long imdb canonical title')})

            self.write(escape.json_encode(movies))

        if action == "display":
            ia = IMDb('http')
            imdbMovie = ia.get_movie(self.get_argument("id"))
            self.set_header("Content-Type", "text/xml")
            self.write(imdbMovie.asXML())

class ImageHandler(BaseHandler):

    def get(self):
        id = self.get_argument('id')
        newWidth = self.get_argument('width', 0)

        result = db.GqlQuery("SELECT * FROM Movie WHERE imdbID = :1 LIMIT 1",id).fetch(1)
        movie = result[0]
        picture = movie.picture

        if newWidth > 0:
            image = images.Image(picture)
            image.resize(int(newWidth))
            picture = image.execute_transforms(output_encoding=images.JPEG)

        self.set_header("Content-Type", "image/jpeg")
        self.write(str(picture))

class PurgeHandler(BaseHandler):
    """Remove all movies"""
    def get(self):
        movies = db.GqlQuery("SELECT * FROM Movie")
        for movie in movies:
            movie.delete()

class CmsHandler(BaseHandler):
    """Fire up the CMS application"""
    def get(self):
        self.redirect("/static/cinemaCMS.html")

class rcfHomeHandler(BaseHandler):
    def get(self):
        movies = db.GqlQuery("SELECT * FROM Movie WHERE category='SN' LIMIT 3")
        self.render("rcfHome.html", movies=movies)

class rcfShowingNowHandler(BaseHandler):
    """Display the Showing Now page for the Royal Cinema"""
    def get(self):
        movies = db.GqlQuery("SELECT * FROM Movie WHERE category='SN'")
        self.render("rcfShowingNow.html", movies=movies)

class rcfComingSoonHandler(BaseHandler):
    """Display the Coming Soon page for the Royal Cinema"""
    def get(self):
        movies = db.GqlQuery("SELECT * FROM Movie WHERE category='CS'")
        self.render("rcfComingSoon.html", movies=movies)

class rcfAboutUsHandler(BaseHandler):
    """Display the About Us page for the Royal Cinema"""
    def get(self):
        aboutTodayText = 'this is a chuck of text from Python - dude'
        self.render("rcfAboutUs.html", aboutTodayText=aboutTodayText)

class rcfContactUsHandler(BaseHandler):
    """Display the About Us page for the Royal Cinema"""
    def get(self):
        self.render("rcfContactUs.html")

class FilmModule(tornado.web.UIModule):
    def render(self, movies):
        return self.render_string("modules/film.html", movies=movies)

class FilmDetailModule(tornado.web.UIModule):

    def render(self, movie):
        return self.render_string("modules/filmDetail.html", movie=movie)

class AdScraperModule(tornado.web.UIModule):
    """Google Adsense Scraper Ad"""
    def render(self):
        return self.render_string("modules/scraper.html")

class FilmComingModule(tornado.web.UIModule):
    """Module for Coming Soon film details"""
    def render(self, movie):
        return self.render_string("modules/filmComing.html", movie=movie)

settings = {
    "cinema_name": u"The Royal Cinema",
    "cinema_location": u"Faversham",
    "cinema_title": u"The Royal Cinema Faversham",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "ui_modules": {
        "Film": FilmModule,
        "FilmDetail": FilmDetailModule,
        "AdScraper": AdScraperModule,
        "FilmComing": FilmComingModule
    },
    "xsrf_cookies": True,
}

application = tornado.wsgi.WSGIApplication([
    (r"/", HomeHandler),
    (r"/purge", PurgeHandler),
    (r"/cms", CmsHandler),
    (r"/imdb", ImdbHandler),
    (r"/image", ImageHandler),
], **settings)

application.add_handlers(r"royalcinema\.independent-cinemas\.com", [
    (r"/", rcfHomeHandler),
    (r"/home", rcfHomeHandler),
    (r"/index.html", rcfHomeHandler),
    (r"/showingNow", rcfShowingNowHandler),
    (r"/comingSoon", rcfComingSoonHandler),
    (r"/aboutUs", rcfAboutUsHandler),
    (r"/contactUs", rcfContactUsHandler),
    (r"/image", ImageHandler),
    ])

def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
