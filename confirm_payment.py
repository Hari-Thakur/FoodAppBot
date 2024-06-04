import sqlite3
import razorpay
import time
import threading
import qrcode
from PIL import Image
import os

# Razorpay API credentials
RAZORPAY_API_KEY = 'rzp_test_qK6RSMZyNHR70N'
RAZORPAY_API_SECRET = 'SVJGrxLbKhIbwyT4gVzptpJC'

client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))

class PaymentProcessor:
    def __init__(self):
        self.payment_status = "pending"
        self.payment_id = None
        self.order_id = None
        self.payment_link_id = None
        self.cancelled = False

    def create_order(self, amount):
        order_amount = amount * 100  # Amount in paise
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {'desc': 'UPI Payment for test'}

        order = client.order.create({
            'amount': order_amount,
            'currency': order_currency,
            'receipt': order_receipt,
            'notes': notes,
            'payment_capture': '0'  # Payment capture should be manual
        })
        self.order_id = order['id']
        return self.order_id

    def make_payment(self, amount, upi_id):
        order_id = self.create_order(amount)
        
        # Create a payment link
        payment_link = client.invoice.create({
            "type": "link",
            "amount": amount * 100,
            "description": "UPI Payment",
            "customer": {
                "contact": "+918688850452"
            },
            "notify": {
                "sms": True,
                "email": False
            },
            "callback_url": "https://example.com/callback",
            "callback_method": "get"
        })
        
        self.payment_link_id = payment_link['id']
        qr_url = payment_link['short_url']
        qr = qrcode.make(qr_url)
        qr.save("payment_qr.png")
        Image.open("payment_qr.png").show()

        return payment_link

    def check_payment_status(self):
        if self.payment_link_id:
            payment_link = client.invoice.fetch(self.payment_link_id)
            amount_due = payment_link.get('amount_due', 0)/100
            amount_paid = payment_link.get('amount_paid', 0)/100
            print(f"Amount due: ₹{amount_due}, Amount paid: ₹{amount_paid}")
            if amount_paid > 0 and amount_due == 0:
                self.payment_status = 'captured'
                self.payment_id = payment_link.get('payment_id')
            else:
                self.payment_status = 'pending'
        return self.payment_status

    def refund_payment(self):
        if self.payment_id:
            client.payment.refund(self.payment_id)
            self.payment_status = "refunded"
            return "Payment has been refunded."
        return "No payment to refund."

    def confirm_payment(self):
        self.payment_status = "successful"
        conn = sqlite3.connect('food.db')
        c = conn.cursor()
        commandd="DELETE FROM current_order;"
        commands = "INSERT INTO previous_order (dish_name, quantity, restaurant_name, price, instructions) SELECT dish_name, quantity, restaurant_name, price, instructions FROM current_order;"
        results = []
        c.execute(commands)
        c.execute(commandd)
        result = c.fetchall()
        results.append(result)
        conn.commit()
        conn.close()
        return "Payment successful."

def track_payment(processor):
    start_time = time.time()
    while True:
        print(processor.payment_status)
        if time.time() - start_time > 600:  # 10 minutes timeout
            if processor.payment_status == "pending":
                processor.payment_status = "closed"
                print("Payment window closed due to timeout.")
            break
        if processor.payment_status == "pending":
            time.sleep(10)
            processor.check_payment_status()
            if processor.payment_status == "captured":
                print("Payment made.")
                print("You have 5 seconds to cancel the payment.")
                paid_time = time.time()
                while time.time() - paid_time <= 5:
                    user_input = input()
                    if user_input == "cancel":
                        processor.cancelled = True
                        break
                if processor.cancelled:
                    print(processor.refund_payment())
                else:
                    print(processor.confirm_payment())
                break
        time.sleep(1)

def main():
    # Connect to the database
    conn = sqlite3.connect('food.db')
    c = conn.cursor()

    # Fetch all rows from the current_order table
    c.execute("SELECT dish_name, price FROM current_order")
    orders = c.fetchall()

    # Calculate the total price
    total_price = sum(price for dish_name, price in orders)
    total_price = 2000
    # Display dish names and final amount to the user
    print("Your Order:")
    for dish_name, price in orders:
        print(f"- {dish_name}: ₹{price}")
    print(f"Total Amount: ₹{total_price}")
    # Ask for confirmation
    confirmation = input("Confirm your order? (yes/no): ")

    if confirmation.lower() == "yes":
        # Proceed to payment
        processor = PaymentProcessor()
        processor.make_payment(total_price, "8688850452@axl")

        tracking_thread = threading.Thread(target=track_payment, args=(processor,))
        tracking_thread.start()

        # Wait for the tracking thread to finish
        tracking_thread.join()
    
    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()
