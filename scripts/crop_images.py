import os
import json
import numpy as np
import cv2
from PIL import Image, ImageFile

# 최대 픽셀 수와 큰 파일 처리 설정
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True


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
            points_x = panel['shape_attributes']['all_points_x']
            points_y = panel['shape_attributes']['all_points_y']

            # 중심점 계산
            mean_x = sum(points_x) / len(points_x)
            mean_y = sum(points_y) / len(points_y)
            center_points.append((mean_x, mean_y))
            polygons.append(panel['shape_attributes'])

    return center_points, polygons


def draw_polygons_on_image(image_path, polygon, output_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    points_x = polygon['all_points_x']
    points_y = polygon['all_points_y']

    # OpenCV 포맷으로 좌표 변환
    points = np.array([[int(x), int(y)] for x, y in zip(points_x, points_y)], dtype=np.int32).reshape((-1, 1, 2))

    # 폴리곤 테두리 그리기 (주황색)
    cv2.polylines(img, [points], isClosed=True, color=(0, 165, 255), thickness=2)

    cv2.imwrite(output_path, img)
    print(f"Image with polygons saved to {output_path}")


def crop_image_around_points(image_path, polygons, center_points, output_folder, crop_size=(1024, 1024)):
    """
    특정 중심 좌표를 기준으로 이미지를 잘라 저장합니다.

    :param image_path: 원본 이미지 경로
    :param center_points: 중심 좌표 리스트 [(x1, y1), (x2, y2), ...]
    :param output_folder: 결과 저장 폴더
    :param crop_size: 잘라낼 크기 (너비, 높이), 기본값 (1024, 1024)
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(len(polygons))

    for idx, (x, y) in enumerate(center_points):
        draw_polygons_on_image(image_path, polygons[idx], output_image_path)
        img = Image.open(output_image_path)
        width, height = img.size
        crop_width, crop_height = crop_size
        # 잘라낼 좌표 계산
        left = max(0, int(x - crop_width / 2))
        right = min(width, int(x + crop_width / 2))
        top = max(0, int(y - crop_height / 2))
        bottom = min(height, int(y + crop_height / 2))

        # 이미지 자르기
        cropped_img = img.crop((left, top, right, bottom))
        output_path = os.path.join(output_folder, f"cropped_{idx}.tif")
        cropped_img.save(output_path)
        print(f"Cropped image saved to {output_path}")


if __name__ == "__main__":
    # 입력 파일 경로
    image_path = "202402603C00810034.tif"
    json_path = "202402603C00810034_input.json"

    # 출력 파일 및 폴더 설정
    output_image_path = "annotated_image.tif"
    output_folder = "output_crops"

    # 중심 좌표와 폴리곤 데이터 추출
    center_points, polygons = calculate_center_points(json_path)

    # 폴리곤을 그린 이미지 생성
   # draw_polygons_on_image(image_path, polygons, output_image_path)

    # 중심 좌표를 기준으로 이미지 자르기
    crop_image_around_points(image_path, polygons, center_points, output_folder)
