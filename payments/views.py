import stripe
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from payments.models import Membership

stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'


@csrf_exempt
def create_checkout_session(request, **kwargs):
    import json
    data = json.loads(request.body.decode("utf-8"))
    id = data['id']
    mem = Membership.objects.get(id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
          'price_data': {
            'currency': 'inr',
            'product_data': {
              'name': '3 months Subscription',
            },
            'unit_amount':(mem.price)*100,
          },
          'quantity': 1,
        }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=YOUR_DOMAIN + '/cancel.html',
    )
    return JsonResponse({'id': session.id})


# home view
def home(request):
    mem = Membership.objects.all()
    return render(request, 'payments/product_detail.html', {"mem": mem})


# success view
def success(request,**kwargs):
    if "session_id" in request.GET:
        session_id = request.GET['session_id']
        print(session_id)
    session = stripe.checkout.Session.retrieve(session_id)
    print(session)
    print(session.amount_total)
    print(session.payment_intent)
    print(session.customer_details)
    amount = session.amount_total/100
    email = session.customer_details["email"]
    name = session.customer_details["name"]
    print(session.customer_details["email"])
    context = {
        "session": session,
        "amount": amount,
        "email": email,
        "name": name
    }
    return render(request, 'payments/payment_success.html', context)


# cancel view
def cancel(request):
    return render(request, 'payments/payment_failed.html')
