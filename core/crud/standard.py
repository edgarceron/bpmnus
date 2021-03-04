"""Standard functions for crud"""
from rest_framework import status
from rest_framework.response import Response

class Crud():
    """Manages the standard functions for crud in modules"""

    def __init__(self, serializer_class, model_class, operation=None, after=None):
        if operation is None:
            self.operation = lambda x: x
        else:
            self.operation = operation
        if after is None:
            self.after = lambda x, y: y
        else:
            self.after = after

        self.serializer_class = serializer_class
        self.model_class = model_class

    def save_instance(self, data, request=None, identifier=0):
        """Saves a model intance"""
        if identifier:
            model_obj = self.model_class.objects.get(pk=identifier)
            data_serializer = self.serializer_class(model_obj, data=data)

        else:
            data_serializer = self.serializer_class(data=data)
        if data_serializer.is_valid():
            model_obj = data_serializer.save()
            self.after(request, data_serializer)
            return {"success": True, "id": model_obj.pk}, status.HTTP_201_CREATED

        answer = self.error_data(data_serializer)
        return answer, status.HTTP_400_BAD_REQUEST

    def add(self, request, action_name):
        """Tries to create a row in the database and returns the result"""
        data = self.operation(request.data.copy())
        answer, answer_status = self.save_instance(data, request)
        return Response(
            answer,
            status=answer_status,
            content_type='application/json'
        )

    def replace(self, request, identifier, action_name):
        """Tries to update a row in the db and returns the result"""    
        data = self.operation(request.data.copy())
        answer, answer_status =  self.save_instance(data, request, identifier)
        return Response(
            answer,
            status=answer_status,
            content_type='application/json'
        )

    def get(self, request, identifier, action_name):
        """Return a JSON response with data for the given id"""
        try:
            model_obj = self.model_class.objects.get(pk=identifier)
            data_serializer = self.serializer_class(model_obj)
            model_data = data_serializer.data.copy()
            model_data = self.operation(model_data)

            data = {
                "success": True,
                "data": model_data
            }
            data = self.after(request, data)

            return Response(
                data,
                status=status.HTTP_200_OK,
                content_type='application/json'
            )
        except self.model_class.DoesNotExist:
            data = {
                "success": False,
                "error": "No existe el registro, quiza haya sido borrado hace poco"
            }
            return Response(
                data,
                status=status.HTTP_404_NOT_FOUND,
                content_type='application/json'
            )

    def delete(self, request, identifier, action_name, message):
        """Tries to delete a row from db and returns the result"""
        model_obj = self.model_class.objects.get(id=identifier)
        model_obj.delete()
        data = {
            "success": True,
            "message": message
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    def toggle(self, request, identifier, action_name, data_name):
        """Toogles the active state for a given row"""
        model_obj = self.model_class.objects.get(id=identifier)
        previous = model_obj.active

        if previous:
            message = data_name + " desactivado con exito"
        else:
            message = data_name + " activado con exito"

        model_obj.active = not model_obj.active
        model_obj.save()
        data = {
            "success": True,
            "message": message
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    def picker_search(self, request, action_name):
        """Returns a JSON response with data for a selectpicker."""
        value = request.data['value']
        queryset = self.operation(value)
        serializer = self.serializer_class(queryset, many=True)
        result = serializer.data
        data = {
            "success": True,
            "result": result
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    def listing(self, request, action_name):
        """ Returns a JSON response containing registered users"""
        sent_data = request.data
        draw = int(sent_data['draw'])
        start = int(sent_data['start'])
        length = int(sent_data['length'])
        search = sent_data['search[value]']

        records_total = self.model_class.objects.count()

        if search != '':
            queryset = self.operation(
                search, start, length
            )
            records_filtered = self.operation(
                search, start, length, True
            )
        else:
            queryset = self.model_class.objects.all()[start:start + length]
            records_filtered = records_total

        queryset = self.after(request, queryset)
        result = self.serializer_class(queryset, many=True)
        data = {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': result.data
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    @staticmethod
    def error_data(serializer):
        """Return a common JSON error result"""
        error_details = []
        for key in serializer.errors.keys():
            error_details.append(
                {"field": key, "message": serializer.errors[key][0]})

        data = {
            "succes": False,
            "Error": {
                "success": False,
                "status": 400,
                "message": "Los datos enviados no son validos",
                "details": error_details
            }
        }
        return data
