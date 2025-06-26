
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger('api')

def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    logger.info(f"Success Response: {message}")
    return Response(
        {
            "success": True,
            "status_code": status_code,
            "message": message,
            "data": data
        },
        status=status_code
    )

def error_response(message="Error", status_code=status.HTTP_400_BAD_REQUEST, data=None):
    logger.error(f"Error Response: {message}")
    return Response(
        {
            "success": False,
            "status_code": status_code,
            "message": message,
            "data": data
        },
        status=status_code
    )