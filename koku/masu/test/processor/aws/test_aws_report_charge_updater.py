#
# Copyright 2021 Red Hat Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""Test the AWSReportDBAccessor utility object."""
from unittest.mock import patch
from unittest.mock import PropertyMock

from masu.database import AWS_CUR_TABLE_MAP
from masu.database.aws_report_db_accessor import AWSReportDBAccessor
from masu.database.provider_db_accessor import ProviderDBAccessor
from masu.database.report_manifest_db_accessor import ReportManifestDBAccessor
from masu.external.date_accessor import DateAccessor
from masu.processor.aws.aws_cost_model_cost_updater import AWSCostModelCostUpdater
from masu.test import MasuTestCase
from masu.test.database.helpers import ReportObjectCreator


class AWSCostModelCostUpdaterTest(MasuTestCase):
    """Test Cases for the AWSCostModelCostUpdater object."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class with required objects."""
        super().setUpClass()

        cls.accessor = AWSReportDBAccessor("acct10001")

        cls.report_schema = cls.accessor.report_schema

        cls.all_tables = list(AWS_CUR_TABLE_MAP.values())

        cls.creator = ReportObjectCreator(cls.schema)

        cls.date_accessor = DateAccessor()
        cls.manifest_accessor = ReportManifestDBAccessor()

    def setUp(self):
        """Set up each test."""
        super().setUp()

        billing_start = self.date_accessor.today_with_timezone("UTC").replace(day=1)
        self.manifest_dict = {
            "assembly_id": "1234",
            "billing_period_start_datetime": billing_start,
            "num_total_files": 2,
            "provider_uuid": self.aws_provider_uuid,
        }

        with ProviderDBAccessor(self.aws_provider_uuid) as provider_accessor:
            self.provider = provider_accessor.get_provider()

        self.updater = AWSCostModelCostUpdater(schema=self.schema, provider=self.provider)
        today = DateAccessor().today_with_timezone("UTC")
        bill = self.creator.create_cost_entry_bill(provider_uuid=self.provider.uuid, bill_date=today)
        cost_entry = self.creator.create_cost_entry(bill, today)
        product = self.creator.create_cost_entry_product()
        pricing = self.creator.create_cost_entry_pricing()
        reservation = self.creator.create_cost_entry_reservation()
        self.creator.create_cost_entry_line_item(bill, cost_entry, product, pricing, reservation)

        self.manifest = self.manifest_accessor.add(**self.manifest_dict)

    @patch("masu.database.cost_model_db_accessor.CostModelDBAccessor.markup", new_callable=PropertyMock)
    def test_update_summary_cost_model_costs(self, mock_markup):
        """Test to verify AWS derived cost summary is calculated."""
        mock_markup.return_value = {"value": 10, "unit": "percent"}
        start_date = self.date_accessor.today_with_timezone("UTC")
        bill_date = start_date.replace(day=1).date()

        self.updater.update_summary_cost_model_costs()
        with AWSReportDBAccessor("acct10001") as accessor:
            bill = accessor.get_cost_entry_bills_by_date(bill_date)[0]
            self.assertIsNotNone(bill.derived_cost_datetime)
