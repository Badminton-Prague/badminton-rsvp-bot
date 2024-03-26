from django.template.loader import render_to_string
from asgiref.sync import sync_to_async


async def async_render_to_string(template_name: str, context: dict) -> str:
    def executor():
        return render_to_string(template_name=template_name, context=context)

    return await sync_to_async(executor)()
