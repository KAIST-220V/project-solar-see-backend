import os
import json
import numpy as np
import cv2
from PIL import Image

def calculate_center_points(json_path):
    """
    JSON 파일에서 각 패널의 중심점 좌표와 폴리곤 데이터를 추출합니다.

    :param json_path: JSON 파일 경로
    :return: 중심점 좌표 리스트, 폴리곤 데이터 리스트
    """
    center_points = []
    polygons = []

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for panel in data['panel']:
            points_x = np.array(panel['shape_attributes']['all_points_x'])
            points_y = np.array(panel['shape_attributes']['all_points_y'])

            # 중심점 계산 (벡터 연산)
            mean_x = points_x.mean()
            mean_y = points_y.mean()
            center_points.append((mean_x, mean_y))
            polygons.append(panel['shape_attributes'])

    return center_points, polygons


def draw_polygon_on_image_memory(img, polygon):
    """
    메모리 내에서 폴리곤 데이터를 이미지에 그립니다.

    :param img: OpenCV 이미지 배열
    :param polygon: 폴리곤 데이터 {'all_points_x': [...], 'all_points_y': [...]}
    :return: 폴리곤이 그려진 이미지
    """
    points_x = polygon['all_points_x']
    points_y = polygon['all_points_y']

    # OpenCV 포맷으로 좌표 변환
    points = np.array([[int(x), int(y)] for x, y in zip(points_x, points_y)], dtype=np.int32).reshape((-1, 1, 2))

    # 폴리곤 테두리 그리기 (주황색)
    annotated_img = cv2.polylines(img.copy(), [points], isClosed=True, color=(0, 165, 255), thickness=2)
    return annotated_img


def crop_image_around_points(image_path,json_path,polygons, center_points, output_folder, crop_size=(1024, 1024)):
    """
    특정 중심 좌표를 기준으로 이미지를 잘라 저장합니다.

    :param image_path: 원본 이미지 경로
    :param polygons: 폴리곤 데이터 리스트
    :param center_points: 중심 좌표 리스트 [(x1, y1), (x2, y2), ...]
    :param output_folder: 결과 저장 폴더
    :param crop_size: 잘라낼 크기 (너비, 높이), 기본값 (1024, 1024)
    """
    # 이미지를 한 번만 읽기
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    width, height = img.shape[1], img.shape[0]

    with open(json_path, 'r', encoding='utf-8') as file:
      data = json.load(file)
      for idx, ((x, y), polygon) in enumerate(zip(center_points, polygons)):
          # 이미지에 폴리곤 그리기
          annotated_img = draw_polygon_on_image_memory(img, polygon)

          # PIL 이미지로 변환
          pil_img = Image.fromarray(cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB))

          # 잘라낼 좌표 계산
          left = max(0, int(x - crop_size[0] / 2))
          right = min(width, int(x + crop_size[0] / 2))
          top = max(0, int(y - crop_size[1] / 2))
          bottom = min(height, int(y + crop_size[1] / 2))
          if(left==0):
            right = crop_size[0]
          if(right==width):
            left = width - crop_size[0]
          if(top==0):
            bottom = crop_size[1]
          if(bottom==height):
            top = height - crop_size[1]

          # 이미지 자르기
          cropped_img = pil_img.crop((left, top, right, bottom))

          # 결과 저장
          image_name=f"{data['image_id']}_cropped_{idx}.png"
          output_path = os.path.join(output_folder, image_name)
          cropped_img.save(output_path)
          print(f"Cropped image saved to {output_path}")
          data['panel'][idx]['image_url'] = "images/map/"+image_name
    
    updated_json_path = os.path.join("./", json_output_path+'.updated.json')
    with open(updated_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Updated JSON saved to {updated_json_path}")


if __name__ == "__main__":
    # 입력 파일 경로
    image_path = "202402603C00810034.tif"
    json_path = "202402603C00810034_input.json"
    json_output_path = "202402603C00810034_output.json"

    # 출력 폴더 설정
    output_folder = "output_crops"

    # 중심 좌표와 폴리곤 데이터 추출
    center_points, polygons = calculate_center_points(json_path)

    # 중심 좌표를 기준으로 이미지 자르기
    crop_image_around_points(image_path,json_output_path, polygons, center_points, output_folder)
