from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_message = "Xato yuz berdi"
        details = None

        if isinstance(response.data, dict):
            if 'detail' in response.data:
                error_message = str(response.data['detail'])
            else:
                error_message = "Validation error"
                details = {
                    field: str(errors[0]) if isinstance(errors, list) else str(errors)
                    for field, errors in response.data.items()
                }

        result = {"success": False, "error": error_message}
        if details:
            result["details"] = details

        response.data = result

    return response
