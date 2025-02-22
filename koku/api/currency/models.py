#
# Copyright 2021 Red Hat Inc.
# SPDX-License-Identifier: Apache-2.0
#
# from uuid import uuid4
# from env import currency endpoimy
from django.db import models

from api.currency.currencies import CURRENCIES


class ExchangeRates(models.Model):
    SUPPORTED_CURRENCIES = tuple([(curr.get("code", "").lower(), curr.get("code")) for curr in CURRENCIES])

    currency_type = models.CharField(max_length=5, choices=SUPPORTED_CURRENCIES, unique=False, blank=True)
    exchange_rate = models.FloatField(default=0)
