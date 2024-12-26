from django.shortcuts import render
from django.utils.encoding import smart_str
import time
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
import requests



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
    data = json.loads(request.body)
    customer_params = data.get('customer', {})
    token_params = data.get('tokenParams', {})
    customer_data = Customer(
        name = customer_params.get("name"), 
        address = customer_params.get('address'), 
        zip_code = customer_params.get('zip_code'), 
        city = customer_params.get('city'), 
        state = customer_params.get('state'), 
        country_code = customer_params.get('country_code'), 
        phone = customer_params.get('phone'), 
        email = customer_params.get('email'),
    )
    token_data = TokenData(
        amount = token_params.get('amount'),
        currency = token_params.get('currency'),
        customer_ip = token_params.get('customer'),
        order_id = token_params.get('order_id'),
        success_url = token_params.get('success_url'),
        error_url = token_params.get('error_url'),
        customer_info= customer_data,
    )
    try:
        token = youcan_pay.token.create_from(token_data) 
        return JsonResponse({'token': token.id})
    except Exception as e :
        return JsonResponse({'message': f'error occured : {str(e)}'})



def get_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    return JsonResponse({'ip': ip})



ALLOWED_ORIGINS = [
    'http://10.25.28.33:3000'
]

@api_view(['GET'])
def get_shoes(request):
    try:
        shoes = Shoe.objects.all()
        serializer = ShoeSerializer(shoes, many=True)
        return Response({'list_shoes': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_newest_shoes(request):
    try:
        newest_shoes = Shoe.objects.filter(newest=True)
        serializer = ShoeSerializer(newest_shoes, many=True)
        return JsonResponse({'list_newest_shoes': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_shoes_sizes(request):
    try:
        shoes_sizes = ShoeDetail.objects.all()
        serializer = ShoeDetailSerializer(shoes_sizes, many =True)
        return JsonResponse({'list_shoeSizes':serializer.data}, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return JsonResponse({'message':f'An error occured: {str(e)}'}, status=status.HTTP_401_UNAUTHORIZED)


api_view
@api_view(['POST'])
def test(request):
    try:
        if request.method == 'POST':
            data = request.POST.get('data')
            if data:
                data = json.loads(data)
            new_shoe = Shoe(
                category = data.get('category'),
                ref = data.get('ref'),
                name = data.get('name'),
                price = float(data.get('price')),
                promo = float(data.get('promo')),
                newest = bool(data.get('newest', False)),
                image = request.FILES.get('image')
            )
            new_shoe.save()
            return JsonResponse({'message': 'Shoe uploaded successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'message': f'An error occured: {str(e)}'}, status=status.HTTP_401_UNAUTHORIZED)



def event_stream_shoes():
    while True:
        shoes = Shoe.objects.all()
        serializer = ShoeSerializer(shoes, many=True)
        data = json.dumps({'list_shoes': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(300)  

def sse_shoes(request):
        response = StreamingHttpResponse(event_stream_shoes(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin  # Adjust as necessary
        return response


def event_stream_shoe_sizes():
    while True:
        shoe_sizes = ShoeDetail.objects.all()
        serializer = ShoeDetailSerializer(shoe_sizes, many=True)
        data = json.dumps({'list_shoeSizes': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2)  # Adjust the frequency of updates as needed

def sse_shoe_sizes(request):
        response = StreamingHttpResponse(event_stream_shoe_sizes(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response
def event_stream_newest_shoes():
    while True:
        shoes = Shoe.objects.filter(newest=True)
        serializer = ShoeSerializer(shoes, many=True)
        data = json.dumps({'list_shoes': serializer.data})
        yield f"data: {smart_str(data)}\n\n"
        time.sleep(2) 

def sse_stream_newest_shoes(request):
        response = StreamingHttpResponse(event_stream_newest_shoes(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        return response