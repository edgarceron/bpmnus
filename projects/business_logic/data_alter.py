import datetime
from projects.models import Projects

def before_save_project(data):
    data['creation_date'] = datetime.datetime.now()
    return data


def before_update_project(id):
    def update(data):
        data['creation_date'] = datetime.datetime.now()
        try:
            data['creation_date'] = Projects.objects.get(pk=id).creation_date
        except Projects.DoesNotExist:
            pass
        return data
    return update