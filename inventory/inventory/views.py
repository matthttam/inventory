from django.http import JsonResponse
from django.views.generic import ListView


class JSONResponseMixin:
    """
    A mixin that can be used to render a JSOn response
    """

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response
        """
        print(context["object_list"])
        return JsonResponse(self.get_data(context))
        # return JsonResponse({})

    def get_data(self, context):
        return {"results": list(context["object_list"])}


class JSONListView(JSONResponseMixin, ListView):
    """
    Used to render a json response for a Select2 select box
    """

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)
