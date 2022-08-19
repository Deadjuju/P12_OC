import datetime
import logging

from rest_framework.request import Request
from rest_framework.views import View


class BaseLogger:
    """
    A base class from which all custom logger classes should inherit.
    """

    logger = logging.getLogger(__name__)
    now = datetime.datetime.now

    @property
    def date_now(self):
        """ Format date of logger"""
        return f"{self.now()} || "


class PermissionLogger(BaseLogger):
    """ A class from which permission could inherit """

    def warning_logger_support_post(self, req: Request, creation_type: str):
        """ custom log when post method is disallowed """

        post = [f'{post}: {value}' for post, value in req.POST.items()]
        message = f"{self.date_now}{req.user} (SUPPORT) try create a {creation_type} --\n" \
                  f"Trying create {creation_type.title()}: {post} --"
        self.logger.warning(message)

    def warning_logger_delete(self, req: Request, view: View, model):
        """ custom log when delete method is disallowed """

        instance = model.objects.filter(pk=view.kwargs['pk']).first()
        message = f"{self.date_now}{req.user} try delete {instance._meta.model_name} -- {instance} --"
        self.logger.warning(message)

    def warning_logger_update_not_allowed(self, req: Request, obj):
        """ custom log when post method is disallowed """

        message = f"{self.date_now}" \
                  f"Method: {req.method} not allowed for user: {req.user} on {obj._meta.model_name} {obj}."
        if req.method == "PATCH" or req.method == "PUT":
            post = [f'{post}: {value}' for post, value in req.POST.items()]
            message += f"\nTrying update: {post} --"
        self.logger.warning(message)


class SerializerLogger(BaseLogger):
    """ A class from which serializer could inherit """

    def warning_logger_to_representation(self, user, instance):
        """ custom log when a client is not assigned to user """

        message = f"{self.date_now}{user} try access to {instance._meta.model_name}: {instance}"
        self.logger.warning(message)

