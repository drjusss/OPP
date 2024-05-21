from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from . import models, serializers, utils


class AppealsApiView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        appeals = models.Appeal.objects.all()
        page_size = int(request.GET.get('page-size', default=5))
        page_id = int(request.GET.get('page-id', default=1))
        appeals_by_page = utils.get_data_by_page(data=appeals, page_id=page_id, page_size=page_size)  # пагинация
        response_data = [serializers.serialize_appeal(appeal=appeal) for appeal in appeals_by_page]
        return JsonResponse(data=response_data, safe=False, status=200)

    def post(self, request: HttpRequest) -> HttpResponse:
        pass

    def put(self, request: HttpRequest) -> HttpResponse:
        pass

    def patch(self, request: HttpRequest) -> HttpResponse:
        pass

    def delete(self, request: HttpRequest) -> HttpResponse:
        pass


class AppealApiView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        pass

    def put(self, request: HttpRequest, pk: int) -> HttpResponse:
        pass

    def patch(self, request: HttpRequest, pk: int) -> HttpResponse:
        pass

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        pass
