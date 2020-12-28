from authentication.utils import email_template
from authentication.models import User
from .models import Order
from rest_framework.response import Response

def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    user = User.username
    order = Order.objects.get(id=order_id)
    subject = 'Order number {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                Your order id is {}.'.format(order.first_name,
                                             order.id)
    email_subject = "We've recieved your order"
    email_body = f'''
        Hello {user.username}, we thank you for your patronage.
        <br><br><b>Note: <i>We have recieved your order and a staff will call you shortly.</i> </b>'''

    email_template(email_subject, user.email, email_body)
    return Response({'message': 'email sent'})