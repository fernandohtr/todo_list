import falcon
import os

from config.utils import render


class TodoResource(object):

    def on_get(self, request, response):
        response.status = falcon.HTTP_200
        response.content_type = 'text/html; charset=utf-8'
        response.body = render('main.html', list_items=self.list_items())

    def list_items(self):
        with open(os.path.abspath('config/save_list.txt')) as file:
            return file.readlines()


app = falcon.API()

app.add_route('/', TodoResource())
