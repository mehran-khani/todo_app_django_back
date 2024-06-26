from rest_framework.exceptions import APIException, status


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"error": "Bad request (400)"}
    default_code = "bad_request"
