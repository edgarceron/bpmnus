import datetime
from typing import Callable
from projects.models import Projects

def before_save_diagram(data: dict) -> dict:
    data['creation_date'] = datetime.datetime.now()
    return data

def add_request_files(request) -> Callable[[dict], dict]:
    def before_save_diagram_file(data: dict) -> dict:
        before_save_diagram(data)
        data['file'] = request.FILES.get('file')
    return before_save_diagram_file

def before_update_diagram(id: int, request) -> Callable[[dict], dict]:
    def update(data: dict) -> dict:
        data['creation_date'] = datetime.datetime.now()
        data['file'] = request.FILES.get('file')
        try:
            data['creation_date'] = Projects.objects.get(pk=id).creation_date
        except Projects.DoesNotExist:
            pass
        return data
    return update