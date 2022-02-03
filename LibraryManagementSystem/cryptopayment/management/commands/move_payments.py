from cryptopayment.payment_gateway import move_payments
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Moves all the completed payments to an address"
    )
    def add_arguments(self, parser):
        parser.add_argument('bitcoin_wallet', nargs='+', type=str)
        parser.add_argument('--no-input', help="Add this is if you don't want to answer any input and directly move payments to given wallet (not recommended at all)",action="store_const", const="n")
        
    def handle(self, *args, **kwargs):
        # whatever is given us after the command is called is the wallet, if nothing is given then 
        # assume it is my testnet wallet
        wallet = kwargs["bitcoin_wallet"][0]
        self.stdout.write(f"Moving payments to adress {wallet.upper()}, are you sure you want to do that? If the address is wrong, your funds will be irrecoverable.Please double check the bitcoin address you want to transfer your BTC to.")
        if not kwargs["no_input"]:
            inp = input("y/yes, n/no : ").lower()
            if inp in ["y", "yes"]:
                move_payments(wallet)
            else:
                self.stdout.write(f"Aborted moving payments to {wallet}")                    
        else:
            move_payments(wallet)

