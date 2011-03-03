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
from google.appengine.api import urlfetch
from google.appengine.api import images

class Movie(db.Model):
    imdbID = db.StringProperty()
    title = db.StringProperty()
    picture = db.BlobProperty(default=None)
    coverURL = db.StringProperty()
    plotOutline = db.StringProperty()
    plot = db.TextProperty()
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
        
class ShowingNowHandler(BaseHandler):
    """Manages Showing now films http://127.0.0.1:8000/showingNow?action=store&id=1504320 """

    def _findPlot(self, movie):
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
                
    def get(self):
        action = self.get_argument("action")
        if action == "store":
            imdbKey = self.get_argument("id")
            ia = imdb.IMDb('http')
            imdbMovie = ia.get_movie(imdbKey)
            # print "id"
            # print imdbMovie.movieID
            # print "title:" 
            # print imdbMovie.get('long imdb canonical title')
            # print "plot summary"
            # print imdbMovie.get('plot outline')
            # print "plot:"
            # print self._findPlot(imdbMovie)
            # print "Poster URL:"
            # print imdbMovie.get('full-size cover url')
            # print imdbMovie.asXML()
            pictureFile = urlfetch.Fetch(imdbMovie.get('full-size cover url')).content
            # file = open("test.jpg", "rw")
            # file.write(pictureFile)
            # file.close()

            self.set_header("Content-Type", "image/jpeg")
            self.write(pictureFile)
            
            movie = Movie(key_name = imdbMovie.movieID,
                          imdbID = imdbMovie.movieID,
                          title = imdbMovie.get('long imdb canonical title'),
                          plotOutline = imdbMovie.get('plot outline'),
                          plot = self._findPlot(imdbMovie),
                          coverURL = imdbMovie.get('full-size cover url'),
                          picture = db.Blob(pictureFile),
                          category = db.Category("Showing Now"))
            movie.put()
        if action == "display":
            ia = imdb.IMDb('http')
            imdbMovie = ia.get_movie(self.get_argument("id"))
            print imdbMovie.asXML()
        
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
        movie = Movie(key_name = "0947798",
                      imdbID = "0947798",
                      title = "The Black Swan",
                      plotOutline = "A ballet dancer wins the lead in 'Swan Lake' and is perfect for the role of the delicate White Swan - Princess Odette - but slowly loses her mind as she becomes more and more like Odette's evil sister, Odile, the Black Swan.",
                      coverURL = "/static/images/0947798_250.jpg",
                      category = db.Category("Coming Soon"))
                      
        movie.put()
        
        movie = Movie(key_name = "0120737",
                      imdbID = "0120737",
                      title = "The Lord of the Rings: The Fellowship of the Ring",
                      plotOutline = "In a small village in the Shire a young Hobbit named Frodo has been entrusted with an ancient Ring. Now he must embark on an Epic quest to the Cracks of Doom in order to destroy it.",
                      coverURL = "/static/images/0120737_250.jpg",
                      category = db.Category("Coming Soon"))
        movie.put()

        movie = Movie(key_name = "1285016",
                      imdbID = "1285016",
                      title = "The Social Network",
                      plotOutline = "A chronicle of the founding of Facebook, the social-networking Web site.",
                      coverURL = "/static/images/1285016_250.jpg",
                      category = db.Category("Coming Soon"))
                      
        movie.put()

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
        movies = db.GqlQuery("SELECT * FROM Movie WHERE category='Showing Now' LIMIT 3")
        self.render("rcfHome.html", movies=movies)
        
class rcfShowingNowHandler(BaseHandler):
    """Display the Showing Now page for the Royal Cinema"""
    def get(self):
        movies = db.GqlQuery("SELECT * FROM Movie WHERE category='Showing Now' LIMIT 3")
        self.render("rcfShowingNow.html", movies=movies)
                                
class rcfComingSoonHandler(BaseHandler):
    """Display the Showing Now page for the Royal Cinema"""
    def get(self):
        movies = db.GqlQuery("SELECT * FROM Movie WHERE category='Coming Soon' LIMIT 3")
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
    (r"/showingNow", ShowingNowHandler),
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
    ])

def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
