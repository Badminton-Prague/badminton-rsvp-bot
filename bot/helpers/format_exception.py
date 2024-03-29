from django.template.loader import render_to_string
import traceback


def format_exception(action: str, exception: Exception) -> str:
    return render_to_string(
        "format_exception.txt",
        dict(
            action=action,
            exception=str(exception),
            traceback=traceback.format_tb(exception.__traceback__, 7),
        ),
    )
