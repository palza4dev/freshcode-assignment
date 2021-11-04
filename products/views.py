import json
from json.decoder                 import JSONDecodeError

from django.db.models.query_utils import Q
from django.http                  import JsonResponse
from django.views                 import View
from django.db                    import transaction

from .models                      import Product
#TODO: from users.decorator              import admin_decorator

class ProductView(View):
    def post(self ,request):
        try:
            data = json.loads(request.body)
            
            with transaction.atomic():
                product = Product.objects.create(
                    name        = data['name'],
                    description = data['description'],
                    is_sold     = data['is_sold'],
                    category_id = data['category'],
                    tag_id      = data['tag']
                )

                product.option_set.create(
                    name       = data['option_name'],
                    size       = data['size'],
                    price      = data['price'],
                    is_sold    = data['option_is_sold'],
                )

            return JsonResponse({'message' : 'CREATED'}, status = 201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    def get(self, request):
        try:
            product_filter = Q()
            
            search_word    = request.GET.get('search-word', '')
            product_type   = request.GET.get('tag', '')

            if search_word or product_type:
                product_filter.add(Q(name__contains=search_word) | Q(description__contains=search_word), product_filter.AND)

            category = int(request.GET.get('category', 0))

            if category:
                product_filter.add(Q(category_id=category), product_filter.AND)

            offset   = request.GET.get('offset', 0)
            limit    = request.GET.get('limit', 5)

            products = Product.objects.filter(product_filter)[offset:offset+limit]

            product_list = [{
                'id'          : product.id,
                'category'    : product.category.name,
                'name'        : product.name,
                'description' : product.description,
                'isSold'      : product.is_sold,
                'badge'       : product.badge,
                'items'       : list(product.option_set.values('id', 'product_id', 'name', 'size', 'price', 'is_sold'))

            } for product in products]
            
            return JsonResponse({'message' : 'SUCCESS', 'products' : product_list}, status = 200)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status = 400)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            
            items = [{
                'id'        : option.id,
                'productId' : product_id,
                'name'      : option.name,
                'size'      : option.size,
                'price'     : option.price,
                'isSold'    : option.is_sold
            } for option in product.option_set.all()]
            
            data = {
                'id'          : product_id,
                'category'    : product.category.name,
                'name'        : product.name,
                'description' : product.description,
                'isSold'      : product.is_sold,
                'badge'       : product.badge,
                'items'       : items
            }
            
            return JsonResponse({'product': data}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_FOUND'}, status=404)
        
        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

    #TODO: @admin_decorator
    def patch(self, request, product_id):
        try:
            data = json.loads(request.body)

            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message':'PRODUCT_NOT_FOUND'}, status=404)

            Product.objects.filter(id=product_id).update(**data)

            return JsonResponse({'message':'UPDATED'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

    #TODO: @admin_decorator
    def delete(self, request, product_id):

        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'message':'INVALID_PRODUCT_ID'}, status=404)

        product = Product.objects.get(id=product_id)
            
        product.delete()
        
        return JsonResponse({'message': 'DELETED'}, status=200)
