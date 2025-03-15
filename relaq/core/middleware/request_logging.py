import time
import logging
from typing import Callable

from django.http import HttpRequest, HttpResponse


logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Start timing
        start_time = time.time()

        # Log request
        logger.info(
            f"[Request] {request.method} {request.path} "
            f"Query Params: {dict(request.GET.items())} "
            f"Body: {request.body.decode() if request.body else ''}"
        )

        # Get response
        response = self.get_response(request)

        # Calculate execution time
        execution_time = time.time() - start_time

        # Log response
        logger.info(
            f"[Response] {request.method} {request.path} "
            f"Status: {response.status_code} "
            f"Time: {execution_time:.2f}s "
            f"Content-Type: {response.get('Content-Type', '')}"
        )

        return response 