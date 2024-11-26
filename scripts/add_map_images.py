import sys
import os
import django
import json

# 현재 스크립트의 부모 폴더를 프로젝트 루트로 설정
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from panel.models import MapImage

def insert_game_images(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data['panel']:
        game_image = MapImage(
            image_url=item['image_url'],
            latitude=item['shape_attributes']['mean_point_latitude'],
            longitude=item['shape_attributes']['mean_point_longitude'],
            area_m2=item['shape_attributes']['shape_area_m2']
        )
        game_image.save()
        print(f"Saved GameImage with ID: {game_image.id}")

# 실행
if __name__ == "__main__":
    json_file_path = "202402603C00810034_output.json.updated.json"
    insert_game_images(json_file_path)
