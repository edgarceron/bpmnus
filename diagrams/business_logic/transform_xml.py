import os, xmltodict, json, platform
from typing import OrderedDict, Tuple
from xhtml2pdf import pisa
from django.template import loader
from django.conf import settings
from diagrams.models import Diagrams
from rest_framework import status
from rest_framework.response import Response
from zipfile import ZipFile


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
            tasks = i.get('bpmn:task', [])
            return tasks if isinstance(tasks, list) else [tasks]
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
        name = role.get('@name', '')
        tasks = get_participant_activities(diagram, role['@processRef'])
        for i in tasks:
            task_id = i['@id']
            data.append({
                'id': task_id,
                'project': diagram_data.project.name,
                'actor': name,
                'title': props[task_id].get('name', ''),
                'desc':  props[task_id].get('desc', ''),
                'priority':  props[task_id].get('priority', ''),
                'criteria':  props[task_id].get('criteria', ''),
                'points':  props[task_id].get('points', ''),
                'restrictionsw':  props[task_id].get('restrictions', ''),
            })
    return data

def has_participants(diagram_id):
    diagram_data = get_diagram(diagram_id)
    xml = diagram_data.xml
    diagram = transform_to_obj(xml)
    participants = get_participants(diagram)
    return (create_diagram_us(diagram_id) if len(participants) else Response(
        { "message": "Recuerde añadir un carril para representar el actor responsable del proceso" },
        status=status.HTTP_200_OK,
        content_type='application/json'
    ))

def generate_us(data: dict) -> Tuple[bool, str]:
    source_html = loader.render_to_string('diagrams/ustemplate.html', data)
    path = settings.STATIC_ROOT
    file_name = os.path.join(path, data['project'] , data['id'] + '.pdf')
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    result_file = open(file_name, "w+b")
    pisa_status = pisa.CreatePDF(source_html, dest=result_file)
    result_file.close()
    return pisa_status.err, file_name


def add_files_to_zip(files, diagram_id):
    path = settings.STATIC_ROOT
    file_name = os.path.join(path, 'usfiles' , diagram_id + '.zip')
    zip_obj = ZipFile(file_name, 'w')
    for i in files:
        zip_obj.write(i)
    zip_obj.close()

def create_diagram_us(diagram_id):
    data = get_data_for_us(diagram_id)
    files = []
    for us in data:
        error, file_name = generate_us(us)
        print(file_name)
        if not error:
            files.append(file_name)
        else: 
            print(error)

    if data == []:
        message = "No se encontraron procesos para el diagrama escogido"
        status_code = status.HTTP_200_OK
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
