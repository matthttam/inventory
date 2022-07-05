from functools import wraps
from django.urls import reverse


# Decorator used to test if a provided url_name redirets to the login url properly
# Attributes:
# url (str) - URL to request
# args (list) - Optional parameter used to pass to reverse
def assert_redirect_to_login(url: str):
    def decorated(method_to_decorate):
        @wraps(method_to_decorate)
        def wrapper(self, *args, **kwargs):
            login_url = reverse("authentication:login", kwargs={})
            response = self.client.get(url)
            self.assertRedirects(
                response,
                f"{login_url}?next={url}",
                status_code=302,
            )
            result = method_to_decorate(self, *args, **kwargs)
            return result

        return wrapper

    return decorated
