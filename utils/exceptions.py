
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
import logging

logger = logging.getLogger('api')

class APIError(Exception):
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if isinstance(exc, APIError):
        logger.error(f"API Error: {exc.message}")
        return Response(
            {
                'success': False,
                'status_code': exc.status_code,
                'message': exc.message,
                'data': None
            },
            status=exc.status_code
        )
    
    if response is not None:
        logger.error(f"DRF Error: {response.data}")
        response.data = {
            'success': False,
            'status_code': response.status_code,
            'message': response.data.get('detail', 'An error occurred'),
            'data': None
        }
    else:
        logger.error(f"Server Error: {str(exc)}")
        response = Response(
            {
                'success': False,
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Internal server error',
                'data': None
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response