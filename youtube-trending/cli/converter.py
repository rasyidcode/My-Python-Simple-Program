import json
import csv

def to_json(data):
    trendings = {
        'total': len(data),
        'data': []
    } 

    for item in data:
        f = '%Y-%m-%d %H:%M:%S'
        fdate = '%Y-%m-%d'
        created_at = item['created_at'].strftime(f)
        updated_at = item['updated_at'].strftime(f)
        trending_date = item['trending_date'].strftime(fdate)

        video = {
            'id': item['id'],
            'num_trending': item['num_trending'],
            'title': item['title'],
            'description': item['description'],
            'channel': item['channel'],
            'views': item['views'],
            'uploaded': item['uploaded'],
            'image_url': item['image_url'],
            'video_id': item['video_id'],
            'created_at': created_at,
            'updated_at': updated_at,
            'trending_date': trending_date
        }

        trendings['data'].append(video)

    result = json.dumps(trendings, indent=4, sort_keys=True)
    
    fdate = '%Y-%m-%d'
    file_name = data[0]['trending_date'].strftime(fdate).replace('-', '_') + "_youtube_trending.json"

    file_json = open('./cli/files/' + file_name, 'w')
    file_json.write(result)
    file_json.close()

    print('Data generated to JSON.')

def to_csv(data):
    print('hello json')

def to_xls(data):
    print('hello json')

def to_xlsx(data):
    print('hello json')

def to_html(data):
    print('hello json')

def to_xml(data):
    print('hello json')

def to_yaml(data):
    print('hello json')
