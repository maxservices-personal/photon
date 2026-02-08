from photon.core.response import HttpResponse

def render(template_name: str, context: dict | None = None) -> HttpResponse:
    """
    Renders a template with the given context using the configured template engine.

    Args:
        template_name (str): The name of the template to render.
        context (dict | None): The context data to pass to the template.

    Returns:
        str: The rendered template as a string.
    """
    from photon.core.config import settings

    if not settings._template_engine_class_instance:
        raise Exception("Template engine is not configured.")

    return HttpResponse(settings._template_engine_class_instance.render_template(template_name, context), 
                        headers=[("Content-Type", "text/html")]
                    )