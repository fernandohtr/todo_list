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
        try:
            task = parse_qs(data_serialize.decode('utf-8'))['task'][0]
            self._save_info(task)
            raise falcon.HTTPFound('/')
        except Exception:
            raise falcon.HTTPFound('/')

    def _save_info(self, read_str):
        with open(os.path.abspath('config/save_list.txt'), 'a') as file:
            return file.write(read_str + '\n')


class DeleteItem(object):

    def on_post(self, request, response):
        data_serialize = request.stream.read()
        data_id = parse_qs(data_serialize.decode('utf-8'))['id'][0]
        index = int(data_id) - 1

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

    def _save_info(self, read_str, index):
        with open(os.path.abspath('config/save_list.txt'), 'a') as file:
            return file.write(read_str + '\n')


class EditItem(object):

    def on_post(self, request, response, **kwargs):
        data_serialize = request.stream.read()
        data_id = kwargs['id']
        task = parse_qs(data_serialize.decode('utf-8'))['task'][0]
        index = data_id - 1
        self._update_info(task, index)
        raise falcon.HTTPFound('/')

    def _update_info(self, task, index):
        with open(os.path.abspath('config/save_list.txt'), 'r') as file:
            items = file.readlines()

        with open(os.path.abspath('config/save_list.txt'), 'w') as file:
            items.pop(index)
            items.insert(index, task + '\n')
            try:
                for item in items:
                    file.write(item)
            except Exception:
                pass


app = falcon.API()

app.add_route('/', ReadMainPage())
app.add_route('/create', CreateItem())
app.add_route('/delete', DeleteItem())
app.add_route('/edit/{id:int()}', EditItem())