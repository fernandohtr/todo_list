from jinja2 import Environment, FileSystemLoader


def render(page, **items):
    file_loader = FileSystemLoader('static')
    environment = Environment(loader=file_loader)
    template = environment.get_template(page)
    return template.render(**items)
