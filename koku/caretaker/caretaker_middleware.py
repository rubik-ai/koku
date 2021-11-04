
"""Custom Caretaker Middleware."""
import json
import logging
from base64 import b64decode
from base64 import b64encode
from unittest.mock import Mock

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from api.common import RH_IDENTITY_HEADER
from api.iam.models import User

LOG = logging.getLogger(__name__)


class CaretakerIdentityHeaderMiddleware(MiddlewareMixin):
    """Middleware to add header for development."""

    header = RH_IDENTITY_HEADER

    def process_request(self, request):
        """Inject an identity header for caretaker purposes.
        Note: This identity object is still processed by koku.middleware.IdentityHeaderMiddleware
        Args:
            request (object): The request object
        """
        LOG.debug("caretaker middleware process request...")
        if hasattr(request, "META") and (hasattr(settings, "CARETAKER_IDENTITY") and settings.CARETAKER_IDENTITY):
            request_id_header = None
            if request.META.get(self.header):
                request_id_header = json.loads(b64decode(request.META.get(self.header)).decode("utf-8"))
            identity_header = request_id_header or settings.CARETAKER_IDENTITY

            user_dict = identity_header.get("identity", {}).get("user")
            user = Mock(
                spec=User,
                access=user_dict.get("access", {}),
                username=user_dict.get("username", "caretaker"),
                email=user_dict.get("email", "caretaker@tmdc.io"),
                admin=user_dict.get("is_org_admin", False),
                customer=Mock(account_id=identity_header.get("account_number", "001")),
                req_id="CARETAKER",
            )

            request.user = user
            json_identity = json.dumps(identity_header)
            LOG.debug("Identity: %s", json_identity)
            header = b64encode(json_identity.encode("utf-8")).decode("utf-8")
            request.META[self.header] = header
        LOG.debug("caretaker middleware process request...complete")
