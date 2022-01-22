import os, xmltodict, json, platform
from typing import OrderedDict
from xhtml2pdf import pisa
from django.template import loader
from django.conf import settings
from diagrams.models import Diagrams


def get_diagram(id: int) -> Diagrams:
    try:
        return Diagrams.objects.get(pk=id)
    except Diagrams.DoesNotExist:
        raise


def transform_to_obj(xml: str) -> dict:
    return xmltodict.parse(xml)


def get_participants(diagram: dict) -> list:
    try:
        return diagram['bpmn:definitions']['bpmn:collaboration']['bpmn:participant']
    except KeyError:
        return []


def get_participant_activities(diagram: dict, process_ref: str) -> list:
    processes = diagram['bpmn:definitions']['bpmn:process']
    for i in processes:
        if i['@id'] == process_ref:
            return i['bpmn:task'] if isinstance(i['bpmn:task'], list) else [i['bpmn:task']]
    return []


def get_data_for_us(diagram_id):
    diagram_data = get_diagram(diagram_id)
    xml = diagram_data.xml
    props = json.loads(diagram_data.propierties)
    diagram = transform_to_obj(xml)
    participants = get_participants(diagram)
    data = []
    for role in participants:
        name = role['@name']
        tasks = get_participant_activities(diagram, role['@processRef'])
        for i in tasks:
            task_id = i['@id']
            data.append({
                'id': task_id,
                'project': diagram_data.project.name,
                'actor': name,
                'title': props[task_id].get('name', ''),
                'desc':  props[task_id].get('desc', '')
            })
    return data


def generate_us(data: dict):
    source_html = loader.render_to_string('diagrams/ustemplate.html', data)
    path = settings.BASE_DIR if platform.system() == 'Windows' else settings.MEDIA_ROOT
    file_name = os.path.join(path, data['project'] , data['id'] + '.pdf')
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    result_file = open(file_name, "w+b")
    pisa_status = pisa.CreatePDF(source_html, dest=result_file)
    result_file.close()
    return pisa_status.err


def create_diagram_us(diagram_id):
    data = get_data_for_us(diagram_id)
    for us in data:
        generate_us(us)

d = create_diagram_us(9)
