import axios from 'axios';
const API_URL = 'http://localhost:8000/projects';

export default class ProjectsService{
    addProject(project){
        const url = `${API_URL}/add/`;
        return axios.post(url,project);
    }

    getProjects(draw, start, length, search){
        const url = `${API_URL}/data_list/`;
        return axios.post(url,{
            draw: draw,
            start: start,
            length: length,
            search: search
        });
    }

    getProject(pk){
        const url = `${API_URL}/get/${pk}`;
        return axios.get(url);
    }

    deleteProject(pk){
        const url = `${API_URL}/delete/${pk}`;
        return axios.delete(url);
    }

    upateProject(project){
        const url = `${API_URL}/replace/${project.id}`;
        return axios.put(url, project);
    }
}
