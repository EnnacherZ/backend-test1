from django.shortcuts import render
from django.utils.encoding import smart_str
import time

import requests
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from rest_framework import status
from .serializers import *
import json
from django.views import View
from youcanpay.youcan_pay import YouCanPay, APIService
from youcanpay.models.data import Customer
from rest_framework.permissions import AllowAny
from youcanpay.models.token import TokenData
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed



# Create your views here.
@api_view(['POST'])
def handlePaymentCheck(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            shoes_order = data.get('shoes_order', [])
            sandals_order = data.get('sandals_order', [])
            shirts_order = data.get('shirts_order', [])
            pants_order = data.get('pants_order', [])
            ordered_product = []
            if len(shoes_order)>0:
                for p in shoes_order:
                    prod = ShoeDetail.objects.get(productId=p['productId'], size=p['size'])
                    prod1 = Shoe.objects.get(id = p['productId'])
                    if prod:
                        prod.quantity -= p['quantity']
                        prod.save()
                        ordered_product.append({
                            "product_type" : 'Shoe',
                            "size" : p['size'],
                            "quantity" : p['quantity'],
                            "category" : prod1.category,
                            "ref" : prod1.ref,
                            "name" : prod1.name,
                            "product_id" : prod1.id
                        })
                        
            if len(sandals_order)>0:
                for p in sandals_order:
                    prod = SandalDetail.objects.get(productId=p['productId'], size=p['size'])
                    prod1 = Sandal.objects.get(id = p['productId'])
                    if prod:
                        prod.quantity -= p['quantity']
                        prod.save()
                        ordered_product.append({
                            "product_type" : 'Sandal',
                            "size" : p['size'],
                            "quantity" : p['quantity'],
                            "category" : prod1.category,
                            "ref" : prod1.ref,
                            "name" : prod1.name,
                            "product_id" : prod1.id
                        })
            if len(shirts_order)>0:
                for p in shirts_order:
                    prod = ShirtDetail.objects.get(productId=p['productId'], size=p['size'])
                    prod1 = Shirt.objects.get(id = p['productId'])
                    if prod:
                        prod.quantity -= p['quantity']
                        prod.save()
                        ordered_product.append({
                            "product_type" : 'Shirt',
                            "size" : p['size'],
                            "quantity" : p['quantity'],
                            "category" : prod1.category,
                            "ref" : prod1.ref,
                            "name" : prod1.name,
                            "product_id" : prod1.id
                        })
            if len(pants_order)>0:
                for p in pants_order:
                    prod = PantDetail.objects.get(productId=p['productId'], size=p['size'])
                    prod1 = Pant.objects.get(id = p['productId'])
                    if prod:
                        prod.quantity -= p['quantity']
                        prod.save()
                        ordered_product.append({
                            "product_type" : 'Pant',
                            "size" : p['size'],
                            "quantity" : p['quantity'],
                            "category" : prod1.category,
                            "ref" : prod1.ref,
                            "name" : prod1.name,
                            "product_id" : prod1.id
                        })
        
        return JsonResponse({'message':'success', 'orderedProducts':ordered_product}, status = status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'message':f'An error occured: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def handlePayment(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            transaction_id = data.get('transaction_id', '')
            client_data = data.get('client_data', {})
            ordered_product = data.get('orderedProduct', [])
            if client_data:
                new_client =Client.objects.create(
                    transaction_id = transaction_id,
                    order_id = client_data['OrderId'],
                    first_name = client_data['FirstName'],
                    last_name = client_data['LastName'],
                    email = client_data['Email'],
                    phone = str(client_data['Tel']),
                    city = client_data['City'],
                    address = client_data['Address'],
                    amount = client_data['Amount'])
                for p in ordered_product:
                    ProductOrdered.objects.create(
                        client = new_client,
                        product_type = p["product_type"],
                        size = p["size"],
                        quantity = p["quantity"],
                        category = p["category"],
                        ref = p["ref"],
                        name = p["name"],
                        product_id = p["product_id"]
                    )
                        
            return JsonResponse({'message': 'Success'}, status=200)
    except Exception as e:
        return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=400)
                    


@api_view(['POST'])
def CreateTokenView(request):
    youcan_pay = YouCanPay.instance().use_keys(
        'pri_sandbox_a54c2b28-f8e5-4920-a440-64003',
        'pub_sandbox_1bfc0387-7aea-49ab-b51e-930e5'
    )
    # data = json.loads(request.body)
    # customer_params = data.get('customer', {})
    # token_params = data.get('tokenParams', {})
    # customer_data = Customer(
    #     name = customer_params.get("name"), 
    #     address = customer_params.get('address'), 
    #     zip_code = customer_params.get('zip_code'), 
    #     city = customer_params.get('city'), 
    #     state = customer_params.get('state'),
    #     country_code = customer_params.get('country_code'), 
    #     phone = customer_params.get('phone'), 
    #     email = customer_params.get('email'),
    # )
    # token_data = TokenData(
    #     amount = token_params.get('amount'),
    #     currency = token_params.get('currency'),
    #     customer_ip = token_params.get('customer'),
    #     order_id = token_params.get('order_id'),
    #     success_url = token_params.get('success_url'),
    #     error_url = token_params.get('error_url'),
    #     customer_info= customer_data,
    # )
    customer_data = Customer(
        name = "customer_params.get()", 
        address = "customer_params.get('address')", 
        zip_code = "customer_params.get('zip_code')", 
        city = "customer_params.get('city')", 
        state = "customer_params.get('state')",
        country_code = "customer_params.get('country_code')", 
        phone = "customer_params.get('phone')", 
        email = "customer_params.get('email')",
    )
    token_data = TokenData(
        amount = 10000,
        currency = "MAD",
        customer_ip =" token_params.get('customer')",
        order_id = "token_params.get('order_id')",
        success_url = "token_params.get('success_url')",
        error_url = "token_params.get('error_url')",
        customer_info= customer_data,
    )
    try:
        token = YouCanPay.check_keys(
            'pri_sandbox_a54c2b28-f8e5-4920-a440-64003',
        'pub_sandbox_1bfc0387-7aea-49ab-b51e-930e5'
        )
        return HttpResponse({'token': token})
    except Exception as e :
        return HttpResponse({'message': f'error occured : {str(e)}'})


@api_view(['POST'])
def get_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    return JsonResponse({'ip': ip})

@api_view(['POST'])
def getTokengg(request):
    # Initialize YouCanPay with your private and public keys
    YouCanPay.enable_sandbox_mode()
    youcan_pay = YouCanPay.instance().use_keys(
    "pri_sandbox_a54c2b28-f8e5-4920-a440-64003",
    "pub_sandbox_02182fd8-34fa-4250-a810-91307",
    )
    data = json.loads(request.body)
    customer_params = data.get('customer', {})
    token_params = data.get('tokenParams', {})
    customer_info = Customer(
        name = customer_params.get("name"), 
        address = customer_params.get('address'), 
        zip_code = customer_params.get('zip_code'), 
        city = customer_params.get('city'), 
        state = customer_params.get('state'),
        country_code = customer_params.get('country_code'), 
        phone = customer_params.get('phone'), 
        email = customer_params.get('email'),
    )
    
    token_params = TokenData(
        amount = token_params.get('amount'),
        currency = token_params.get('currency'),
        customer_ip = token_params.get('customer'),
        order_id = token_params.get('order_id'),
        success_url = token_params.get('success_url'),
        error_url = token_params.get('error_url'),
        customer_info= customer_info,
    )
    try:
        token = youcan_pay.token.create_from(token_params)
        return  JsonResponse({'token': token.id})
    except Exception as e :
        return JsonResponse({'message': f'error occured : {str(e)}'})
    

ALLOWED_ORIGINS = [
    'http://192.168.1.9:3000'
]

@api_view(['GET'])
def get_products(request,):
    try:
        shoes_products = Shoe.objects.filter(newest=True)
        sandals_products = Sandal.objects.filter(newest=True)
        shirts_products = Shirt.objects.filter(newest=True)
        pants_products = Pant.objects.filter(newest=True)
        shoes_serializer = ShoeSerializer(shoes_products, many=True)
        sandals_serializer = SandalSerializer(sandals_products, many=True)
        shirts_serializer = ShirtSerializer(shirts_products, many=True)
        pants_serializer = PantSerializer(pants_products, many=True)
        return JsonResponse({'list_shoes': shoes_serializer.data,
                            'list_sandals': sandals_serializer.data,
                            'list_shirts' : shirts_serializer.data,
                            'list_pants':pants_serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_newest_products(model, modelSerializer):
    try:
        products = model.objects.filter(newest=True)
        serializer = modelSerializer(products, many=True)
        return JsonResponse({'list_products':serializer.data})
    except Exception as e: 
        return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_new_shoes(request): return get_newest_products(model=Shoe, modelSerializer=ShoeSerializer)
@api_view(['GET'])
def get_new_sandals(request): return get_newest_products(model=Sandal, modelSerializer=SandalSerializer)
@api_view(['GET'])
def get_new_shirts(request): return get_newest_products(model=Shirt, modelSerializer=ShirtSerializer)
@api_view(['GET'])
def get_new_pants(request): return get_newest_products(model=Pant, modelSerializer=PantSerializer)

#EventSoure functions
def event_stream_shoes():
    while True:
        products = Shoe.objects.all()
        serializer = ShoeSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)
def event_stream_shoes_newest():
    while True:
        products = Shoe.objects.filter(newest=True)
        serializer = ShoeSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)   
def event_stream_shoesSizes():
    while True:
        products = ShoeDetail.objects.all()
        serializer = ShoeDetailSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)
def sse_shoes(request):
        response = StreamingHttpResponse(event_stream_shoes(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_shoes_new(request):
        response = StreamingHttpResponse(event_stream_shoes_newest(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_sizes_shoes(request):
        response = StreamingHttpResponse(event_stream_shoesSizes(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response


def event_stream_sandals():
    while True:
        products = Sandal.objects.all()
        serializer = SandalSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)
def event_stream_sandals_newest():
    while True:
        products = Sandal.objects.filter(newest=True)
        serializer = SandalSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)   
def event_stream_sandalsSizes():
    while True:
        products = SandalDetail.objects.all()
        serializer = SandalDetailSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)
def sse_sandals(request):
        response = StreamingHttpResponse(event_stream_sandals(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_sandals_new(request):
        response = StreamingHttpResponse(event_stream_sandals_newest(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_sizes_sandals(request):
        response = StreamingHttpResponse(event_stream_sandalsSizes(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response



def event_stream_shirts():
    while True:
        products = Shirt.objects.all()
        serializer = ShirtSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)
def event_stream_shirts_newest():
    while True:
        products = Shirt.objects.filter(newest=True)
        serializer = ShirtSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)   
def event_stream_shirtsSizes():
    while True:
        products = ShirtDetail.objects.all()
        serializer = ShirtDetailSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)
def sse_shirts(request):
        response = StreamingHttpResponse(event_stream_shirts(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_shirts_new(request):
        response = StreamingHttpResponse(event_stream_shirts_newest(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_sizes_shirts(request):
        response = StreamingHttpResponse(event_stream_shirtsSizes(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response



def event_stream_pants():
    while True:
        products = Pant.objects.all()
        serializer = PantSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)
def event_stream_pants_newest():
    while True:
        products = Pant.objects.filter(newest=True)
        serializer = PantSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)   
def event_stream_pantsSizes():
    while True:
        products = PantDetail.objects.all()
        serializer = PantDetailSerializer(products, many=True)
        data = json.dumps({'data': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)
def sse_pants(request):
        response = StreamingHttpResponse(event_stream_pants(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_pants_new(request):
        response = StreamingHttpResponse(event_stream_pants_newest(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_sizes_pants(request):
        response = StreamingHttpResponse(event_stream_pantsSizes(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response



