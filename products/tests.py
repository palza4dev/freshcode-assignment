import json, jwt, bcrypt

from django.test     import TestCase, Client, client
from my_settings import ALGORITHM, SECRET_KEY

from freshcode.settings import SECRET_KEY, ALGORITHM
from users.models       import User
from products.models    import Category, Option, Product, Tag

class ProductDetailTest(TestCase):
    def setUp(self):
        global password
        password = 'sample_password'
        user = User.objects.create(
            id       = 1,
            email    = 'user@freshcode.me',
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            role     = 'user'   
        )
        global user_token
        user_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)        
        
        admin = User.objects.create(
            id       = 2,
            email    = 'admin@freshcode.me',
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            role     = 'admin'  
        )
        global admin_token
        admin_token = jwt.encode({'id':admin.id}, SECRET_KEY, algorithm=ALGORITHM)

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

    def test_detail_get_not_found_fail(self):
        client = Client()

        response = client.get('/products/99', content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{'message':'PRODUCT_NOT_FOUND'})
        
    def test_detail_patch_success(self):
        client = Client()
        
        headers     = {'HTTP_Authorization': admin_token}
        data        = {
            'name'  : 'name_change',
            'badge' : 'badge_change'
        }
        response = client.patch('/products/1', data=data, content_type='application/json', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message':'UPDATED'})

    def test_detail_patch_not_admin_fail(self):
        client = Client()
        
        headers     = {'HTTP_Authorization': user_token}
        data        = {
            'name'  : 'name_change',
            'badge' : 'badge_change'
        }
        response = client.patch('/products/1', data=data, content_type='application/json', **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message':'NOT_ADMIN'})
        
    def test_detail_patch_product_not_found_fail(self):
        client = Client()
        
        headers     = {'HTTP_Authorization': admin_token}
        data        = {
            'name'  : 'name_change',
            'badge' : 'badge_change'
        }
        response = client.patch('/products/99', data=data, content_type='application/json', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'PRODUCT_NOT_FOUND'})

    def test_detail_delete_success(self):
        client = Client()
        
        headers  = {'HTTP_Authorization': admin_token}
        response = client.delete('/products/1', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message':'DELETED'})

    def test_detail_delete_not_admin_fail(self):
        client = Client()
        
        headers  = {'HTTP_Authorization': user_token}
        response = client.patch('/products/1', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message':'NOT_ADMIN'})

    def test_detail_delete_product_not_found_fail(self):
        client = Client()
        
        headers  = {'HTTP_Authorization': admin_token}
        response = client.delete('/products/99', content_type='application/json', **headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'message':'PRODUCT_NOT_FOUND'})   

class ProductViewTest(TestCase):
    def setUp(self):
        pw = bcrypt.hashpw("admin".encode("utf-8"), bcrypt.gensalt())
        User.objects.create(
            id = 1,
            email="admin@freshcode.me", 
            password=pw.decode("utf-8"), 
            role="admin"
        )

        pw1 = bcrypt.hashpw("user".encode("utf-8"), bcrypt.gensalt())
        User.objects.create(
            id = 2,
            email="user@freshcode.me", 
            password=pw1.decode("utf-8"), 
            role="user"
        )

        [Category.objects.create(
            id = i+1,
            name = '메뉴{}'.format(i+1)
        ) for i in range(5)]

        [Tag.objects.create(
            id = i+1,
            name = '태그{}'.format(i+1),
            type = 'tag{}'.format(i+1)
        ) for i in range(5)]

        [Product.objects.create(
            id = i+1,
            name = "상품{}".format(i+1),
	        description = "설명{}".format(i+1),
	        is_sold = 0,
	        badge = "NEW",
	        category_id = (i % 5) + 1,
	        tag_id = (i % 5) + 1,
        ) for i in range(10)]

        name = ["미디움", "라지"]
        size = ["M", "L"]

        for i in range(10):
            for j in range(2):
                Product.objects.get(id=i+1).option_set.create(
                    id = 2*i + (j+1),
                    name = name[j%2],
                    size = size[j%2],
                    price = 10000 + i+1,
                    is_sold = 0
                )
        
    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()
        Tag.objects.all().delete()
        Option.objects.all().delete()

    def test_products_post_success(self):
        client = Client()
        data = {
	        "name" : "상품10",
	        "description" : "설명10",
	        "is_sold" : 0,
	        "badge" : "NEW",
	        "category" : 4,
	        "tag" : 1,
	        "option_name" : "미디움",
	        "size" : "M",
	        "price" : 10000,
	        "option_is_sold" : 0
        }

        headers = {'HTTP_Authorization' : jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)}
        response = client.post('/products', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'CREATED'})

    def test_products_post_not_admin(self):
        client = Client()
        data = {
	        "name" : "상품10",
	        "description" : "설명10",
	        "is_sold" : 0,
	        "badge" : "NEW",
	        "category" : 4,
	        "tag" : 1,
	        "option_name" : "미디움",
	        "size" : "M",
	        "price" : 10000,
	        "option_is_sold" : 0
        }

        headers = {'HTTP_Authorization' : jwt.encode({'id' : 2}, SECRET_KEY, ALGORITHM)}
        response = client.post('/products', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'NOT_ADMIN'})

    def test_products_post_key_error(self):
        client = Client()
        data = {
	        "description" : "설명10",
	        "is_sold" : 0,
	        "badge" : "NEW",
	        "category" : 4,
	        "tag" : 1,
	        "option_name" : "미디움",
	        "size" : "M",
	        "price" : 10000,
	        "option_is_sold" : 0
        }

        headers = {'HTTP_Authorization' : jwt.encode({'id' : 1}, SECRET_KEY, ALGORITHM)}
        response = client.post('/products', json.dumps(data), content_type='application/json', **headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})

    def test_products_get_success(self):
        client = Client()
        
        response = client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                
            "message": "SUCCESS",
            "products": [
                {
                    "id": 1,
                    "category": "메뉴1",
                    "name": "상품1",
                    "description": "설명1",
                    "isSold": False,
                    "badge": "NEW",
                    "items": [
                        {
                        "id": 1,
                        "product_id": 1,
                        "name": "미디움",
                        "size": "M",
                        "price": 10001,
                        "is_sold": False
                        },
                        {
                        "id": 2,
                        "product_id": 1,
                        "name": "라지",
                        "size": "L",
                        "price": 10001,
                        "is_sold": False
                        }
                    ],
                    "tags": {
                        "name": "태그1",
                        "type": "tag1"
                    }
                    },
                    {
                    "id": 2,
                    "category": "메뉴2",
                    "name": "상품2",
                    "description": "설명2",
                    "isSold": False,
                    "badge": "NEW",
                    "items": [
                        {
                        "id": 3,
                        "product_id": 2,
                        "name": "미디움",
                        "size": "M",
                        "price": 10002,
                        "is_sold": False
                        },
                        {
                        "id": 4,
                        "product_id": 2,
                        "name": "라지",
                        "size": "L",
                        "price": 10002,
                        "is_sold": False
                        }
                    ],
                    "tags": {
                        "name": "태그2",
                        "type": "tag2"
                    }
                    },
                    {
                    "id": 3,
                    "category": "메뉴3",
                    "name": "상품3",
                    "description": "설명3",
                    "isSold": False,
                    "badge": "NEW",
                    "items": [
                        {
                        "id": 5,
                        "product_id": 3,
                        "name": "미디움",
                        "size": "M",
                        "price": 10003,
                        "is_sold": False
                        },
                        {
                        "id": 6,
                        "product_id": 3,
                        "name": "라지",
                        "size": "L",
                        "price": 10003,
                        "is_sold": False
                        }
                    ],
                    "tags": {
                        "name": "태그3",
                        "type": "tag3"
                    }
                    },
                    {
                    "id": 4,
                    "category": "메뉴4",
                    "name": "상품4",
                    "description": "설명4",
                    "isSold": False,
                    "badge": "NEW",
                    "items": [
                        {
                        "id": 7,
                        "product_id": 4,
                        "name": "미디움",
                        "size": "M",
                        "price": 10004,
                        "is_sold": False
                        },
                        {
                        "id": 8,
                        "product_id": 4,
                        "name": "라지",
                        "size": "L",
                        "price": 10004,
                        "is_sold": False
                        }
                    ],
                    "tags": {
                        "name": "태그4",
                        "type": "tag4"
                    }
                    },
                    {
                    "id": 5,
                    "category": "메뉴5",
                    "name": "상품5",
                    "description": "설명5",
                    "isSold": False,
                    "badge": "NEW",
                    "items": [
                        {
                        "id": 9,
                        "product_id": 5,
                        "name": "미디움",
                        "size": "M",
                        "price": 10005,
                        "is_sold": False
                        },
                        {
                        "id": 10,
                        "product_id": 5,
                        "name": "라지",
                        "size": "L",
                        "price": 10005,
                        "is_sold": False
                        }
                    ],
                    "tags": {
                        "name": "태그5",
                        "type": "tag5"
                    }
                }
                ]
            }
        )

    def test_products_get_category_success(self):
        client = Client()
        
        response = client.get('/products?category=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                
            "message": "SUCCESS",
            "products": [
                {
                    "id": 1,
                    "category": "메뉴1",
                    "name": "상품1",
                    "description": "설명1",
                    "isSold": False,
                    "badge": "NEW",
                    "items": [
                        {
                        "id": 1,
                        "product_id": 1,
                        "name": "미디움",
                        "size": "M",
                        "price": 10001,
                        "is_sold": False
                        },
                        {
                        "id": 2,
                        "product_id": 1,
                        "name": "라지",
                        "size": "L",
                        "price": 10001,
                        "is_sold": False
                        }
                    ],
                    "tags": {
                        "name": "태그1",
                        "type": "tag1"
                    }
                    },
                    {
                    "id": 6,
                    "category": "메뉴1",
                    "name": "상품6",
                    "description": "설명6",
                    "isSold": False,
                    "badge": "NEW",
                    "items": [
                        {
                        "id": 11,
                        "product_id": 6,
                        "name": "미디움",
                        "size": "M",
                        "price": 10006,
                        "is_sold": False
                        },
                        {
                        "id": 12,
                        "product_id": 6,
                        "name": "라지",
                        "size": "L",
                        "price": 10006,
                        "is_sold": False
                        }
                    ],
                    "tags": {
                        "name": "태그1",
                        "type": "tag1"
                    }
                    }],
            
                }
            
            )

    def test_products_get_value_error(self):
        client = Client()

        response = client.get('/products?offset=string')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'message' : 'VALUE_ERROR'
        })