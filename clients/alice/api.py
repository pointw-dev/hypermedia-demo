import requests
import base64
from config import BASE_API_URL


class Api:
    usernames = [
        'phartman',
        'tgraves',
        'jkelly',
        'manderson',
        'hreagan',
        'clopez',
        'sheath',
        'gjohnson',
        'dthibideau',
        'admin',
        'root'
    ]
    logged_in_as = None
    
    # <<alice_only>>
    root_resource = None

    @classmethod
    def _get_token(cls):
        username = cls.logged_in_as.lower() if cls.logged_in_as else 'root'

        if username in cls.usernames:
            b64 = base64.b64encode(f'{username}:password'.encode('ascii'))
            token = b64.decode('ascii')
            return f'Basic {token}'
        
    @classmethod
    def get_headers(cls):
        return {
            'Authorization': cls._get_token(),
            'Content-type': 'application/json',
            'Accept': 'application/hal+json, application/json;q=0.9, */*;q=0'
        }

    # <<alice_only>>
    @classmethod
    def get_root_resource(cls):
        if cls.root_resource:
            return cls.root_resource

        result = requests.get(BASE_API_URL, headers=cls.get_headers())
        cls.root_resource = result.json()
        return cls.root_resource

    @staticmethod
    def display_error(result):
        print(f'\n>  {result.status_code} {result.reason}')

        response_body = result.json()
        error_message = response_body['_error']['message']

        if result.status_code == 422:
            print('>  One or more fields have invalid values:')
            for issue, details in response_body['_issues'].items():
                print(f'>  - {issue} {details}')
        elif result.status_code == 500:
            print('>  Service threw one or more exceptions')
            for issue in response_body['_issues']:
                for arg in issue['exception']['args']:
                    print(f'>  - {arg}')
        else:
            print('>  ' + error_message)

    @staticmethod
    def url_join(base, path):
        return "{0}/{1}".format(base.rstrip("/"), path.lstrip("/"))

    # <<alice_only>>
    @staticmethod
    def url_from_resource(resource, rel):
        href = resource['_links'][rel]['href']
        url = href
        if href.startswith('/'):
            url = Api.url_join(BASE_API_URL, href)
        return url
