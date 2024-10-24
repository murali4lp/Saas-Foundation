import stripe
from decouple import config

DJANGO_DEBUG = config('DJANGO_DEBUG', cast=bool, default=True)
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='', cast=str)

if 'sk_test' in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
    raise ValueError('Invalid stripe key for prod')

stripe.api_key = "sk_test_tR3PYbcVNZZ796tH88S4VQ2u"

def create_customer(name='', email='', metadata = {}, raw=False):
  response = stripe.Customer.create(
    name=name,
    email=email,
    metadata=metadata
  )
  if raw:
     return response
  stripe_id = response.id
  return stripe_id

def create_product(name='', metadata = {}, raw=False):
  response = stripe.Product.create(
    name=name,
    metadata=metadata
  )
  if raw:
     return response
  stripe_id = response.id
  return stripe_id

def create_price(
    currency="usd",
    unit_amount=9999, # corresponds to a default value of 99.99
    interval='month',
    product=None,
    metadata = {}, 
    raw=False):
  if product is None:
     return None
  response = stripe.Price.create(
    currency=currency,
    unit_amount=unit_amount,
    recurring={"interval": interval },
    product_data=product,
    metadata=metadata
  )
  if raw:
     return response
  stripe_id = response.id
  return stripe_id