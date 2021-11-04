import json, jwt, bcrypt

from django.test     import TestCase, Client

from users.models    import User
from products.models import Category, Option, Product, Tag

class ProductDetailTest(TestCase):
    def setUp(self):
        password = 'abc1234!'
        User.objects.create(
            id       = 1,
            email    = 'test@test.com',
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')          
        )
        
        Category.objects.create(
            id   = 1,
            name = 'sample_category'
        )
        
        Tag.objects.create(
            id   = 1,
            name = 'sample_tag'
        )
        
        Product.objects.create(
            id          = 1,
            name        = 'sample_name',
            description = 'sample_description',
            badge       = 'sample_badge',
            is_sold     = False,
            category_id = 1,
            tag_id      = 1
        )
        
        Option.objects.create(
            id         = 1,
            name       = 'sample_option',
            size       = 'sample_size',
            price      = 7700,
            product_id = 1,
            is_sold    = False
        )

    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        Product.objects.all().delete()
        Option.objects.all().delete()
    
    def test_detail_get_success(self):
        client = Client()
        
        response = client.get('/products/1', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
            'product' : {
                'id'          : 1,
                'category'    : 'sample_category',
                'name'        : 'sample_name',
                'description' : 'sample_description',
                'isSold'      : False,
                'badge'       : 'sample_badge',
                'items'       : [
                    {
                        'id'       : 1,
                        'productId': 1,
                        'name'     : 'sample_option',
                        'size'     : 'sample_size',
                        'price'    : 7700,
                        'isSold'   : False
                    }
                ]
            }
        })
    
    #def test_detail_get_not_found_fail(self):
    
    #def test_detail_get_value_error_fail(self):    
