import os
import time
from math import ceil

import cv2
import torch
from logzero import logger
from tqdm import trange


def mosaic(img, alpha=0.05):
    try:
        w = img.shape[1]
        h = img.shape[0]

        # int()で丸めると0になった場合にエラーとなるためceil()を使用
        _w = ceil(w * alpha)
        _h = ceil(h * alpha)

        img = cv2.resize(img, (_w, _h))
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_NEAREST)

        return img

    except Exception as e:
        logger.error(f"Error mosaic : {e}  (w={w} h={h} alpha={alpha})")


def write_moseic_to_frame(writer, frames, results):
    for frame, xyxys in zip(frames, results.xyxy):
        for xyxy in xyxys:
            xmin = int(xyxy[0])
            ymin = int(xyxy[1])
            xmax = int(xyxy[2])
            ymax = int(xyxy[3])

            frame[ymin:ymax, xmin:xmax] = mosaic(frame[ymin:ymax, xmin:xmax])

        writer.write(frame)


def main(video_path: str, model_path: str, bacth_size: int = 64) -> None:
    # video
    video = cv2.VideoCapture(video_path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = video.get(cv2.CAP_PROP_FPS)

    logger.info(f"frame count: {frame_count}")
    logger.info(f"FPS: {frame_rate}")

    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (w, h)
    logger.info(f"video size: {size}")

    # model
    model = torch.hub.load(
        "ultralytics/yolov5",
        "custom",
        path=model_path,
    )

    model.classes = [0]  # filter by class

    # output
    fmt = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    writer = cv2.VideoWriter(
        video_path.replace(".mp4", "_processed.mp4v"),
        fmt,
        frame_rate,
        size,
    )

    try:
        # detect
        # frameをすべてメモリに載せることができない可能性も考慮して
        # ミニバッチを都度作成してモデルに入力している
        i = 0
        j = 0
        frame_list = []
        for frame_idx in trange(frame_count):  # tgdm(range(frame_count))
            i += 1

            video.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = video.read()

            if ret == False:
                j += 1
                continue

            frame_list.append(frame)

            if (i == bacth_size) or (frame_idx == frame_count - 1):
                results = model(frame_list)
                write_moseic_to_frame(writer, frames=frame_list, results=results)

                i = 0
                frame_list.clear()

    except Exception as e:
        writer.release()
        video.release()

        logger.error(f"{e}")

    # finish
    if j != 0:
        logger.warning(f"n of ret: {j}")

    writer.release()
    video.release()


if __name__ == "__main__":
    start_time = time.time()

    model_path = os.path.join("models", "yolov5n.pt")
    video_path = os.path.join("sample_movie", "sample_walk.mp4")

    main(video_path=video_path, model_path=model_path, bacth_size=128)

    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    logger.info(f"elapsed time: {minutes} min {seconds} sec")
