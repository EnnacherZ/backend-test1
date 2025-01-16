from django.utils.encoding import smart_str
from django.shortcuts import render
import time
from .models import *
from rest_framework.decorators import api_view
from django.http import HttpResponseForbidden, JsonResponse, StreamingHttpResponse
from rest_framework import status
from .serializers import *
import json
import os
from dotenv import load_dotenv
from youcanpay.youcan_pay import YouCanPay
from youcanpay.models.data import Customer
from youcanpay.models.token import TokenData
load_dotenv()
key1 = os.environ.get('payment_second_key')
key2 = os.environ.get('payment_first_key')
allowed_origins = os.environ.get('REQUEST_ALLOWED_ORIGINS')
is_sandbox = os.environ.get('IS_SANDBOX_MODE')
forbbiden_message = 'Forbidden-Acces denied'
ALLOWED_ORIGINS = [allowed_origins]
def origin_checker(request):
    referer = request.META.get('HTTP_REFERER','')
    if referer in ALLOWED_ORIGINS: return False
    else : return True



# Create your views here.
@api_view(['POST'])
def handlePaymentCheck(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            shoes_order = (data.get('shoes_order', []), Shoe, ShoeDetail)
            sandals_order = (data.get('sandals_order', []), Sandal, SandalDetail)
            shirts_order = (data.get('shirts_order', []), Shirt, ShirtDetail)
            pants_order = (data.get('pants_order', []), Pant, PantDetail)
            all_items = [shoes_order, sandals_order, shirts_order, pants_order]
            ordered_product = []
            for item in all_items:
                if len(item[0])>0:
                    for p in item[0]:
                        prod = item[2].objects.get(productId=p['productId'], size=p['size'])
                        prod1 = item[1].objects.get(id = p['productId'])
                        if prod:
                            prod.quantity -= p['quantity']
                            prod.save()
                            ordered_product.append({
                                "product_type" : prod1.productType,
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

def quantity_manager(data, model, modelDetail, ordered_product):
    if len(data)>0:
        for p in data:
            if modelDetail == ShoeDetail or modelDetail ==SandalDetail:prod = modelDetail.objects.get(productId=p['id'], size=int(p['size']))
            else: prod = modelDetail.objects.get(productId=p['id'], size=p['size'])
            prod1 = model.objects.get(id = p['id'])
            if prod:
                prod.quantity -= p['quantity']
                prod.save()
                ordered_product.append({
                    "product_type" : prod1.productType,
                    "size" : p['size'],
                    "quantity" : p['quantity'],
                    "category" : prod1.category,
                    "ref" : prod1.ref,
                    "name" : prod1.name,
                    "product_id" : prod1.id
                    })               
     
def data_dict(data, model, modelDetail):return({'data':data, 'model':model, 'modelDetail':modelDetail})
@api_view(['POST'])
def handlePayment(request):
    try:
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        else:
            if request.method == 'POST':
                data = json.loads(request.body)

                # Extraction des données de la requête
                shoes_data = data.get('shirts_order', [])
                sandals_data = data.get('shoes_order', [])
                shirts_data = data.get('sandals_order', [])
                pants_data = data.get('pants_order', [])
                
                # Créez un dictionnaire des données
                shirts_order = data_dict(shoes_data, Shirt, ShirtDetail)
                shoes_order = data_dict(sandals_data, Shoe, ShoeDetail)
                sandals_order = data_dict(shirts_data, Sandal, SandalDetail)  # Corrigé ici pour utiliser Sandal et SandalDetail
                pants_order = data_dict(pants_data, Pant, PantDetail)
                
                # Récupérer le transaction_id et client_data de la requête
                transaction_id = data.get('transaction_id', '')
                client_data = data.get('client_data', {})
                
                # Liste pour stocker les produits commandés
                ordered_product = []
                orders = [shoes_order, sandals_order, shirts_order, pants_order]
                
                # Parcourez toutes les commandes
                for item in orders:
                    if len(item['data']) > 0:
                        for p in item['data']:
                            # Obtenez le produit selon le modèle et les détails associés
                            prod = item['modelDetail'].objects.get(productId=p['id'], size=p['size'])
                            prod1 = item['model'].objects.get(id=p['id'])
                            
                            # Si le produit est trouvé, mettez à jour la quantité et sauvegardez
                            if prod:
                                prod.quantity -= p['quantity']
                                prod.save()
                                
                                # Ajoutez les informations du produit commandé à la réponse
                                ordered_product.append({
                                    "product_type": prod1.productType,
                                    "size": p['size'],
                                    "quantity": p['quantity'],
                                    "category": prod1.category,
                                    "ref": prod1.ref,
                                    "name": prod1.name,
                                    "product_id": prod1.id
                                })
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
                # Retourner une réponse JSON avec la liste des produits commandés
                return JsonResponse({'ordered_products': ordered_product}, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=400)
                    
@api_view(['POST'])
def get_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    return JsonResponse({'ip': ip})

@api_view(['POST'])
def getPaymentToken(request):
    if is_sandbox: YouCanPay.enable_sandbox_mode()
    youcan_pay = YouCanPay.instance().use_keys(
    key1,
    key2,
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
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        else:                                   
            token = youcan_pay.token.create_from(token_params)
            return  JsonResponse({'token': token.id})
    except Exception as e :
        return JsonResponse({'message': f'error occured : {str(e)}'})
    



@api_view(['GET'])
def get_newest_products(request,):
    try:
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        else:
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
                                'list_pants':pants_serializer.data,}, status=status.HTTP_200_OK
                                )
    except Exception as e:
        print(e)
        return JsonResponse({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        response = StreamingHttpResponse(event_stream_shoes(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response
def sse_shoes_new(request):
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        response = StreamingHttpResponse(event_stream_shoes_newest(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_sizes_shoes(request):
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
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
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        response = StreamingHttpResponse(event_stream_sandals(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_sandals_new(request):
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        response = StreamingHttpResponse(event_stream_sandals_newest(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_sizes_sandals(request):
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
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
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        response = StreamingHttpResponse(event_stream_shirts(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_shirts_new(request):
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        response = StreamingHttpResponse(event_stream_shirts_newest(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_sizes_shirts(request):
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
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
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        response = StreamingHttpResponse(event_stream_pants(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_pants_new(request):
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        response = StreamingHttpResponse(event_stream_pants_newest(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response
def sse_sizes_pants(request):
        if origin_checker(request):return HttpResponseForbidden(forbbiden_message)
        response = StreamingHttpResponse(event_stream_pantsSizes(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        origin = request.headers.get('Origin')
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
        return response



