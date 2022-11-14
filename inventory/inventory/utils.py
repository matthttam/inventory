from django.urls import reverse


def get_history_table_context(table_id: str):
    return get_table_context(table_id, ["Date", "Actor", "Field", "From", "To"])


def get_table_context(table_id: str, headers: list) -> dict:

    return {
        table_id: {
            "id": table_id,
            "headers": headers,
        }
    }
