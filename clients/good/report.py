from halchemy import Api

API = Api('http://localhost:2112')
ROOT = API.get('/')


def main():
    regions = API.get_from_rel(ROOT, 'regions')
    
    for region in regions['_items']:
        print(region['name'])
        print()
        print('  Notifications')
        notifications = API.get_from_rel(region, 'notifications')
        for notification in notifications['_items']:
            print(f'  - {notification["name"]}')
            
        print()
        print('  Brands')
        brands = API.get_from_rel(region, 'brands')
        for brand in brands['_items']:
            print(f'  - {brand["name"]}')
        print()
        print()
            


if __name__ == '__main__':
    main()
