import datetime
from typing import Callable

from django.db import connections
from projects.models import Projects

def before_save_diagram(data: dict) -> dict:
    data['creation_date'] = datetime.datetime.now()
    return data

def add_request_files(request) -> Callable[[dict], dict]:
    def before_save_diagram_file(data: dict) -> dict:
        before_save_diagram(data)
        return data
    return before_save_diagram_file