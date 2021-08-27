import json

import requests

data = {
    'username': 'Nar_mAttaru',
    'password': 'personaldata',
    'email': 'mymail@mail.com',
    'profile': {
        'role': ['заказчик'],
        'categories': [
            {'name': 'Сантехника'},
            {'name': 'Строительство'}
        ],
        'subcategories': [
            {'name': 'мелкий ремонт'},
            {"name": "монтаж новой"}
        ]
    }
    
}

if __name__ == '__main__':
    host = 'http://127.0.0.1:8000/auth/users/'
    r = requests.post(host, json=data)
    print(r.json())