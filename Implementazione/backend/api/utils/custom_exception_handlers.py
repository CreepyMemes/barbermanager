from rest_framework.views import exception_handler

def customExceptionHandler(exc, context):
    """
    Custom exception handler that returns JSON format
    """
    response = exception_handler(exc, context)

    if response is not None and 'non_field_errors' in response.data:
        errors = response.data.pop('non_field_errors')

        if isinstance(errors, list) and len(errors) == 1:
            response.data['detail'] = errors[0]
        else:
            response.data['detail'] = errors

    return response
