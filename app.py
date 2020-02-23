import falcon

from psycopg2.errors import UndefinedTable
from urllib.parse import parse_qs

from config.utils import render
from config.connect_db import connection


class ReadMainPage(object):

    def on_get(self, request, response):
        response.status = falcon.HTTP_200
        response.content_type = 'text/html; charset=utf-8'

        try:
            with connection as conn:
                with conn.cursor() as cursor:

                    cursor.execute('SELECT id, task FROM todo')
                    list_items = cursor.fetchall()

                    response.body = render('index.html', list_items=list_items)

        except UndefinedTable:
            with connection as conn:
                with conn.cursor() as cursor:

                    cursor.execute('CREATE TABLE todo (id serial PRIMARY KEY, task text)')
                    cursor.execute('SELECT id, task FROM todo')
                    list_items = cursor.fetchall()

                    response.body = render('index.html', list_items=list_items)


class CreateItem(object):

    def on_post(self, request, response):
        data_serialize = request.stream.read()
        try:
            task = parse_qs(data_serialize.decode('utf-8'))['task'][0]

            with connection as conn:
                with conn.cursor() as cursor:

                    cursor.execute('INSERT INTO todo (task) VALUES (%s)', (task,))
                    conn.commit()

                    raise falcon.HTTPFound('/')
        except Exception:
            raise falcon.HTTPFound('/')


class DeleteItem(object):

    def on_post(self, request, response):
        data_serialize = request.stream.read()
        data_id = parse_qs(data_serialize.decode('utf-8'))['id'][0]
        index = int(data_id)

        with connection as conn:
            with conn.cursor() as cursor:

                cursor.execute('DELETE FROM todo WHERE "id" = %s', (index,))
                conn.commit()

        raise falcon.HTTPFound('/')


class EditItem(object):

    def on_post(self, request, response, **kwargs):
        data_serialize = request.stream.read()
        data_id = kwargs['id']
        task = parse_qs(data_serialize.decode('utf-8'))['task'][0]
        index = data_id

        with connection as conn:
            with conn.cursor() as cursor:

                cursor.execute('UPDATE todo SET task = %s WHERE id = %s', (task, index))
                conn.commit()

        raise falcon.HTTPFound('/')


app = falcon.API()

app.add_route('/', ReadMainPage())
app.add_route('/create', CreateItem())
app.add_route('/delete', DeleteItem())
app.add_route('/edit/{id:int()}', EditItem())