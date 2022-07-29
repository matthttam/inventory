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

    temp_id = 9999999
    placeholder = "__id_placeholder__"
    permitted_actions = {}
    for action, path in action_paths:
        permitted_actions[action] = {
            "allowed": request.user.has_perm(f"{app}.{action}_{model}"),
            "path": reverse(f"{app}:{path}", args=[temp_id]).replace(
                str(temp_id), placeholder
            ),
        }

    return permitted_actions


def get_history_table_context(table_id: str):
    return get_table_context(table_id, ["Date", "Actor", "Field", "From", "To"])


def get_table_context(table_id: str, headers: list) -> dict:

    return {
        table_id: {
            "id": table_id,
            "headers": headers,
        }
    }
