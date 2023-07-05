import os

import cv2
from logzero import logger

video_path = os.path.join("..", "sample_movie", "sample_walk.mp4")
video = cv2.VideoCapture(video_path)

# エンコード方式の取得
fourcc = int(video.get(cv2.CAP_PROP_FOURCC))

# fourccコードからエンコード方式の文字列を取得
encode_format = (
    chr(fourcc & 0xFF)
    + chr((fourcc >> 8) & 0xFF)
    + chr((fourcc >> 16) & 0xFF)
    + chr((fourcc >> 24) & 0xFF)
)

logger.info(f"エンコード方式: {encode_format}")

# ビデオキャプチャを解放
video.release()
