import requests

CATALOG_API_URL = 'http://localhost:2113'
NOTIFICATION_API_URL = 'http://localhost:2114'
REGION_API_URL = 'http://localhost:2115'


def main():
    response = requests.get(f'{REGION_API_URL}/regions')
    data = response.json()
    
    for region in data['_items']:
        print(region['name'])
        print()
        print('  Notifications')
        response = requests.get(f'{NOTIFICATION_API_URL}/notifications?where={{"_region_ref=={region["_id"]}}}')
        notifications = response.json()
        for notification in notifications['_items']:
            print(f'  - {notification["name"]}')
            
        print()
        print('  Brands')
        response = requests.get(f'{CATALOG_API_URL}/brands?where={{"_region_ref=={region["_id"]}}}')
        brands = response.json()
        for brand in brands['_items']:
            print(f'  - {brand["name"]}')
        print()
        print()
        
        


if __name__ == '__main__':
    main()
