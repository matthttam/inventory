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
