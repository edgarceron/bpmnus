import os, xmltodict, json, platform
from typing import OrderedDict
from xhtml2pdf import pisa
from django.template import loader
from django.conf import settings
from diagrams.models import Diagrams
from rest_framework import status
from rest_framework.response import Response


def get_diagram(id: int) -> Diagrams:
    try:
        return Diagrams.objects.get(pk=id)
    except Diagrams.DoesNotExist:
        return None


def transform_to_obj(xml: str) -> dict:
    return xmltodict.parse(xml)


def get_participants(diagram: dict) -> list:
    try:
        participants = diagram['bpmn:definitions']['bpmn:collaboration']['bpmn:participant']
        return participants if isinstance(participants, list) else [participants]
    except KeyError:
        return []


def get_participant_activities(diagram: dict, process_ref: str) -> list:
    processes = diagram['bpmn:definitions']['bpmn:process']
    processes = processes if isinstance(processes, list) else [processes]
    for i in processes:
        if i['@id'] == process_ref:
            return i['bpmn:task'] if isinstance(i['bpmn:task'], list) else [i['bpmn:task']]
    return []


def get_data_for_us(diagram_id):
    diagram_data = get_diagram(diagram_id)
    data = []
    if diagram_data is None:
        return data
    xml = diagram_data.xml
    props = json.loads(diagram_data.propierties)
    diagram = transform_to_obj(xml)
    participants = get_participants(diagram)
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

    if data == []:
        message = "No se generaron historias para el diagrama escogido"
        status_code = status.HTTP_204_NO_CONTENT
    else:
        message = "Se generaron {} historia/s para el diagrama escogido".format(str(len(data)))
        status_code = status.HTTP_200_OK

    
    answer = {
        "message": message
    }

    return Response(
            answer,
            status=status_code,
            content_type='application/json'
    )
