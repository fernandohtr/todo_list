import falcon
import os
import json

from urllib.parse import parse_qs

from config.utils import render


class ReadMainPage(object):

    def on_get(self, request, response):
        response.status = falcon.HTTP_200
        response.content_type = 'text/html; charset=utf-8'
        response.body = render('index.html', list_items=self._list_items())

    def _list_items(self):
        with open(os.path.abspath('config/save_list.txt')) as file:
            return file.readlines()


class CreateItem(object):

    def on_post(self, request, response):
        data_serialize = request.stream.read()
        data = parse_qs(data_serialize.decode('utf-8'))['task'][0]
        self._save_info(data)
        raise falcon.HTTPFound('/')

    def _save_info(self, read_str):
        with open(os.path.abspath('config/save_list.txt'), 'a') as file:
            return file.write(read_str + '\n')


class DeleteItem(object):

    def on_post(self, request, response):
        data_serialize = request.stream.read()
        data = parse_qs(data_serialize.decode('utf-8'))['id'][0]
        index = int(data) - 1
        deleted_item = self._delete_items(index)
        raise falcon.HTTPFound('/')

    def _delete_items(self, index):
        with open(os.path.abspath('config/save_list.txt'), 'r') as file:
            items = file.readlines()

        with open(os.path.abspath('config/save_list.txt'), 'w') as file:
            deleted_item = items.pop(index)
            try:
                for item in items:
                    file.write(item)
            except Exception:
                pass
            return deleted_item


app = falcon.API()

app.add_route('/', ReadMainPage())
app.add_route('/create', CreateItem())
app.add_route('/delete', DeleteItem())
