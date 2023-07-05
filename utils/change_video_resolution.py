import os

import cv2
from logzero import logger


def change_resolution(
    video_path, targe_size, save_frame: bool = False, output_directory: str = None
):
    input_video = cv2.VideoCapture(video_path)
    logger.info(f"frame counts: {int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))}")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 出力動画のコーデック
    output_video = cv2.VideoWriter(
        video_path.replace(".mp4", "_preprocessed.mp4"),
        fourcc,
        input_video.get(cv2.CAP_PROP_FPS),
        (targe_size[0], targe_size[1]),
    )

    frame_count = 0
    while input_video.isOpened():
        ret, frame = input_video.read()

        if ret:
            resized_frame = cv2.resize(frame, (targe_size[0], targe_size[1]))

            if save_frame & (frame_count % 10 == 0):  # save per 10 frames
                os.makedirs(output_directory, exist_ok=True)
                output_path = os.path.join(output_directory, f"frame_{frame_count}.jpg")
                cv2.imwrite(output_path, resized_frame)
                logger.info(f"save {os.path.basename(output_path)}")

            output_video.write(resized_frame)

        else:
            break

        frame_count += 1

    logger.info("loop finish.")

    input_video.release()


if __name__ == "__main__":
    video_path = os.path.join("sample_movie", "sample_pickles.mp4")

    target_size = (1280, 720)

    change_resolution(
        video_path=video_path,
        targe_size=target_size,
        save_frame=True,
        output_directory=os.path.join("sample_movie", "frames"),
    )
