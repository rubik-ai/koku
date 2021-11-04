import logging

from django.core.management.base import BaseCommand
from masu.celery.tasks import check_report_updates

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generates the cost report'

    def handle(self, *args, **kwargs):
        LOG.info("generate cost report...")
        LOG.debug("handle args: %s, kwargs: %s", str(args), str(kwargs))
        async_download_result = check_report_updates.delay()
        LOG.info("generate cost report...complete : %s", str(async_download_result))
        self.stdout.write(self.style.SUCCESS('generate cost report...complete : %s' % str(async_download_result)))
