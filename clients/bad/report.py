import requests

CATALOG_API_URL = 'http://localhost:2112'




def main():
    response = requests.get(f'{CATALOG_API_URL}/regions')
    data = response.json()
    
    for region in data['_items']:
        print(region['name'])
        print()
        print('  Notifications')
        response = requests.get(f'{CATALOG_API_URL}/regions/{region["_id"]}/notifications')
        notifications = response.json()
        for notification in notifications['_items']:
            print(f'  - {notification["name"]}')
            
        print()
        print('  Brands')
        response = requests.get(f'{CATALOG_API_URL}/regions/{region["_id"]}/brands')
        brands = response.json()
        for brand in brands['_items']:
            print(f'  - {brand["name"]}')
        print()
        print()
        
        


if __name__ == '__main__':
    main()
