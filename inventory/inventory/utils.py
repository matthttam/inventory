from django.urls import reverse


def get_permitted_actions(
    request,
    app: str,
    model: str,
    action_paths: list[tuple] = [
        ("view", "detail"),
        ("change", "edit"),
        ("delete", "delete"),
    ],
) -> dict:

    permitted_actions = {}
    for action, path in action_paths:
        permitted_actions[action] = {
            "allowed": request.user.has_perm(f"{app}.{action}_{model}"),
            "path": get_reverse_placeholder(f"{app}:{path}"),
        }

    return permitted_actions


def get_reverse_placeholder(
    view_name: str, placeholder: str = "__id_placeholder__", args=[9999999]
):
    """Accepts a view and placeholder. Returns a string of the view url where the ID is replaced with a placeholder"""
    return reverse(view_name, args=[9999999]).replace(str(args[0]), placeholder)


def get_history_table_context(table_id: str):
    return get_table_context(table_id, ["Date", "Actor", "Field", "From", "To"])


def get_table_context(table_id: str, headers: list) -> dict:

    return {
        table_id: {
            "id": table_id,
            "headers": headers,
        }
    }
