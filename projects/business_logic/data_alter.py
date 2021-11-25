import datetime

def before_save_project(data):
    data['creation_date'] = datetime.datetime.now()
    return data
