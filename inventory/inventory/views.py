from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.generic import ListView
from django.views.generic.edit import BaseFormView
from django.views.generic.list import BaseListView
from django.core.exceptions import ImproperlyConfigured


class JSONResponseMixin:
    """
    A mixin that can be used to render a JSOn response
    """

    # def render_to_json_response(self, context, **response_kwargs):
    #    """
    #    Returns a JSON response
    #    """
    #    return JsonResponse(self.get_data(context))

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context))

    def get_data(self, context):
        raise ImproperlyConfigured("Method get_data must be overridden.")


class JSONListView(JSONResponseMixin, BaseListView):
    """
    Used to render a json response for a Select2 select box
    """

    def get_data(self, context):
        return {"results": list(context["object_list"])}


class JSONFormView(JSONResponseMixin, BaseFormView):
    def get_success_url(self):
        print("get_success_url")
        return None

    def form_valid(self, form):
        print("form_valid")
        return self.render_to_response(self.get_context_data(success=True))

    def form_invalid(self, form):
        print("form_invalid")
        context = self.get_context_data(success=False)
        context["errors"] = form.errors
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        print("get")
        return HttpResponseNotAllowed(
            [
                "GET",
            ]
        )

    def get_data(context):

        return {"success": context["success"]}
