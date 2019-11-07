import falcon
import os
import json

from urllib.parse import parse_qs

from config.utils import render


class TodoResource(object):

    def on_get(self, request, response):
        response.status = falcon.HTTP_200
        response.content_type = 'text/html; charset=utf-8'
        content = {"items": ["Estudar", "Comprar pão"]}
        response.body = render('main.html', list_items=self._list_items())

    def on_post(self, request, response):
        data_serialize = request.stream.read()
        data_byte = parse_qs(data_serialize)[b'task'][0]
        data = data_byte.decode('utf-8')
        self._save_info(data)
        self.on_get(request, response)

    def _list_items(self):
        with open(os.path.abspath('config/save_list.txt')) as file:
            return file.readlines()

    def _save_info(self, read_str):
        with open(os.path.abspath('config/save_list.txt'), 'a') as file:
            return file.write(read_str + '\n')


app = falcon.API()

app.add_route('/', TodoResource())
