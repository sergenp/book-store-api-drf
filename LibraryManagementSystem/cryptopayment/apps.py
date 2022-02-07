import threading

from django.apps import AppConfig


class CryptopaymentConfig(AppConfig):
    name = "cryptopayment"

    def ready(self) -> None:
        from cryptopayment.payment_gateway import check_payment_success  # noqa

        # create the payment checker thread on cryptopayment app ready
        threading.Thread(target=check_payment_success, daemon=True).start()

