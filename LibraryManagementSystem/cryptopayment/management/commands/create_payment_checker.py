from cryptopayment.payment_gateway import create_payment_checker
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Creates the initial background tasks. This should only be run once"
    )

    def handle(self, *args, **kwargs):
        self.stdout.write("Trying to create initial background tasks.")
        create_payment_checker()
        self.stdout.write("Started bitcoin payment checker thread")


