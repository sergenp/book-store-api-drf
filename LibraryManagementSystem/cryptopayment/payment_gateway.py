"""
This is the script that checks for Payment models in the database
and if the payment is received in the given bitcoin address
it sets the Payment model's success to True
then calls the create order function, and creates an order for the cart
"""

import threading
import time

import bit
import bit.exceptions
from commercebackend.models import CartModel, OrderModel

from cryptopayment.models import Invoice, Payment


def create_order(payment):
    order = OrderModel.objects.create(
        user=payment.user, cart=payment.cart, shipping=payment.shipping
    )
    print(f"{order} has been created")
    invoice = Invoice.objects.create(payment=payment, order=order)
    print(f"{invoice} has been created")


def create_payment_checker():
    threading.Thread(target=check_payment_success, daemon=True).start()

def check_payment_success():
    while True:
        # get all payments in the payment table with success 0
        for payment in Payment.objects.all().filter(success=0):
            btc_cost = payment.total_price_btc
            # get the bitcoin address for the payment
            wallet = bit.PrivateKeyTestnet(payment.btc_address_wif)
            if wallet.get_balance("btc") == str(btc_cost):
                print(f"Payment recieved for {payment}")
                # if it is successfull, set the success flag to 1
                payment.success = 1
                # get the cart and set it bought
                cart = CartModel.all_objects.get(pk=payment.cart.id)
                # user might delete the cart, so get it from all_objects rather than objects
                cart.bought = 1
                cart.save()
                payment.save()
                create_order(payment)
        time.sleep(60)  # wait a minute, continue checking payments


# this function moves all the successfull payments from payment wallets to a specificed wallet
# move_payments('bitcoin_wallet_address')
def move_payments(to_wallet):
    # get all the payments with success 1
    payments = Payment.objects.all().filter(success=1)
    for payment in payments:
        # get the wallet
        wallet = bit.PrivateKeyTestnet(payment.btc_address_wif)
        # create transactions
        try:
            tx_id = wallet.send([], leftover=to_wallet)
            print(f"Payment from {wallet} to {to_wallet} is successfull.\nTxid:\n{tx_id}")
        except bit.exceptions.InsufficientFunds as e:
            print(f"Payment wallet {wallet} has insufficent funds for a transaction, \n{e}")
            continue
