#
# Copyright 2021 Red Hat Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""Tests the Masu API `manifest` Views."""
from unittest.mock import patch

from django.test.utils import override_settings
from django.urls import reverse

from api.provider.models import Provider
from api.provider.models import Sources
from masu.test import MasuTestCase


@patch("koku.middleware.MASU", return_value=True)
@override_settings(ROOT_URLCONF="masu.urls")
class SourcesViewSetTests(MasuTestCase):
    """Tests source views"""

    def setUp(self):
        """Create source entries for tests."""
        super().setUp()
        providers = Provider.objects.all()
        self.provider_count = providers.count()
        for i, provider in enumerate(providers):
            Sources(
                source_id=i,
                source_uuid=provider.uuid,
                offset=i,
                source_type=provider.type,
                authentication=provider.authentication.credentials,
                billing_source=provider.billing_source.data_source,
                koku_uuid=str(provider.uuid),
                provider=provider,
            ).save()

    def test_sources_list(self, mock_masu):
        """Test the sources LIST call."""
        url = reverse("sources-list")

        response = self.client.get(url, content_type="application/json", **self.request_context["request"].META)
        body = response.json()
        print(body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body.get("meta").get("count"), self.provider_count)

    def test_sources_detail(self, mock_masu):
        """Test the sources GET detail call."""

        # Test with UUID
        url = reverse("sources-detail", kwargs={"pk": self.aws_provider_uuid})
        response = self.client.get(url, content_type="application/json", **self.request_context["request"].META)
        self.assertEqual(response.status_code, 200)

        # Test with source ID
        url = reverse("sources-detail", kwargs={"pk": 1})
        response = self.client.get(url, content_type="application/json", **self.request_context["request"].META)
        self.assertEqual(response.status_code, 200)

        # Test invalide
        url = reverse("sources-detail", kwargs={"pk": "3258745890"})
        response = self.client.get(url, content_type="application/json", **self.request_context["request"].META)
        self.assertEqual(response.status_code, 404)

    def test_source_filters(self, mock_masu):
        """Test that filters filter."""
        url = reverse("sources-list")

        filters = {
            "source_type": "AWS",
            "name": "OCP",
            "account_id": "10002",
            "schema_name": "acct10002",
            "ocp_on_cloud": True,
            "infrastructure_provider_id": self.aws_provider_uuid,
            "cluster_id": "my-ocp",
            "active": False,
            "paused": True,
            "pending_delete": True,
            "pending_update": True,
            "out_of_order_delete": True,
            "type": "AWS",
        }

        for key, value in filters.items():
            filter_url = url + f"?{key}={value}"
            response = self.client.get(
                filter_url, content_type="application/json", **self.request_context["request"].META
            )
            body = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertLess(body.get("meta").get("count"), self.provider_count)

        filter_url = url + "?not-a=filter"
        response = self.client.get(filter_url, content_type="application/json", **self.request_context["request"].META)
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body.get("meta").get("count"), self.provider_count)
