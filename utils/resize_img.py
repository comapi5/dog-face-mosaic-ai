import cv2
import numpy as numpy


def resize_with_padding(image, target_size):
    height, width = image.shape[:2]
    target_width, target_height = target_size

    # 元の画像のアスペクト比とターゲットサイズのアスペクト比を比較して、拡大/縮小する方向を決定する
    aspect_ratio = width / height
    target_aspect_ratio = target_width / target_height

    if aspect_ratio > target_aspect_ratio:
        # 元の画像の幅が大きい場合、幅をターゲットサイズに合わせてリサイズし、余白を追加
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
        padding = (target_height - new_height) // 2
        resized_image = cv2.resize(image, (new_width, new_height))
        padded_image = cv2.copyMakeBorder(resized_image, padding, padding, 0, 0, cv2.BORDER_CONSTANT)

    else:
        # 元の画像の高さが大きい場合、高さをターゲットサイズに合わせてリサイズし、余白を追加
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
        padding = (target_width - new_width) // 2
        resized_image = cv2.resize(image, (new_width, new_height))
        padded_image = cv2.copyMakeBorder(resized_image, 0, 0, padding, padding, cv2.BORDER_CONSTANT)

    return padded_image



if __name__ == "__main__":
    import os
    from glob import glob
    from tqdm import tqdm

    target_size = (1280, 720)

    img_paths = glob(os.path.join("..", "..", "dog_mosaic_annotation", "kaggle_animal_faces_val", "*"))
    

    for path in tqdm(img_paths):
        img = cv2.imread(path)
        img = resize_with_padding(img, target_size)
        cv2.imwrite(path, img)

