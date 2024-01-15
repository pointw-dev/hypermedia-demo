from halchemy import Api

API = Api('http://localhost:2112')
ROOT = API.get('/')

def main():
    notify_count = 1
    brand_count = 1
    for region_name in ['Canada', 'US', 'Middle East']:
        region = API.post_to_rel(ROOT, 'regions', {'name': region_name})
    
        API.post_to_rel(region, 'notifications', {'name': f'notify{notify_count}'})
        notify_count += 1
        API.post_to_rel(region, 'notifications', {'name': f'notify{notify_count}'})
        notify_count += 1
        API.post_to_rel(region, 'notifications', {'name': f'notify{notify_count}'})
        notify_count += 1
            
        API.post_to_rel(region, 'brands', {'name': f'brand{brand_count}'})
        brand_count += 1
        API.post_to_rel(region, 'brands', {'name': f'brand{brand_count}'})
        brand_count += 1
        API.post_to_rel(region, 'brands', {'name': f'brand{brand_count}'})
        brand_count += 1
    
if __name__ == '__main__':
    main()
