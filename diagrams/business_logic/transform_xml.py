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
    processes = get_processes(diagram)
    for i in processes:
        if i['@id'] == process_ref:
            tasks = i.get('bpmn:task', [])
            return tasks if isinstance(tasks, list) else [tasks]
    return []

def add_depend(id: str, x, dependencies: dict):
    if id in dependencies: dependencies[id].append(x)
    else: dependencies[id] = [x]

def get_dependencies(diagram: dict):
    dependencies = {}
    processes = get_processes(diagram)
    for i in processes:
        keys = i.keys()
        for j in keys:
            ele = i[j] if isinstance(i[j], list) else [i[j]]
            for m in ele:
                if '@sourceRef' in m:
                    add_depend(m['@id'], m['@sourceRef'], dependencies)
                if 'bpmn:incoming' in m:
                    l = m['bpmn:incoming']
                    l = l if isinstance(l, list) else [l]
                    for k in l:
                        add_depend(m['@id'], k, dependencies)
    get_collaboration_flows(diagram, dependencies)
    return dependencies

def get_collaboration_flows(diagram: dict, dependencies: dict):
    if 'bpmn:messageFlow' in diagram['bpmn:definitions']['bpmn:collaboration']:
        flows = diagram['bpmn:definitions']['bpmn:collaboration']['bpmn:messageFlow']
        for m in flows:
            if '@sourceRef' in m:
                add_depend(m['@id'], m['@sourceRef'], dependencies)

def get_activity_relations(activity: dict, dependencies: dict):
    relations = []
    if 'bpmn:incoming' in activity:
        incoming = activity['bpmn:incoming']
        incoming = incoming if isinstance(incoming, list) else [incoming]
        for i in incoming:
            relations += get_last_activities(i, dependencies)
    return relations

def get_relations_with_names(relations: list, names: dict):
    relations = [i + ' ' + names[i] for i in relations]
    return relations

def get_last_activities(id: str, dependencies: dict):
    if id == '': return []
    if id.startswith('Activity'): return [id]
    relations = []
    for i in dependencies.get(id, []):
        relations = relations + get_last_activities(i, dependencies)
    return relations

def get_processes(diagram: dict) -> list[dict]:
    processes = diagram['bpmn:definitions']['bpmn:process']
    processes = processes if isinstance(processes, list) else [processes] 
    return processes

def get_activity_names(diagram: dict) -> dict:
    names = {}
    processes = get_processes(diagram)
    for i in processes:
        tasks = i.get('bpmn:task', [])
        tasks = tasks if isinstance(tasks, list) else [tasks]
        for j in tasks:
            names[j['@id']] = j['@name']
    return names

def get_data_for_us(diagram_id):
    diagram_data = get_diagram(diagram_id)
    data = []
    if diagram_data is None:
        return data
    xml = diagram_data.xml
    props = json.loads(diagram_data.propierties)
    diagram = transform_to_obj(xml)
    participants = get_participants(diagram)
    dependencies = get_dependencies(diagram)
    names = get_activity_names(diagram)
    for role in participants:
        name = role.get('@name', '')
        tasks = get_participant_activities(diagram, role['@processRef'])
        for i in tasks:
            task_id = i['@id']
            relations =  get_activity_relations(i, dependencies)
            relations = get_relations_with_names(relations, names)
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
                'relations': relations
            })
    return data

def has_participants(diagram_id: int):
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

def add_files_to_zip(files: list, diagram_id: str):
    path = settings.STATIC_ROOT
    file_name = os.path.join(path, 'usfiles' , diagram_id + '.zip')
    zip_obj = ZipFile(file_name, 'w')
    for i in files:
        zip_obj.write(i)
    zip_obj.close()

def create_diagram_us(diagram_id: int):
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
