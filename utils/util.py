import os
from glob import glob

files = glob(os.path.join("..", "..", "dog_mosaic_annotation", "pickles", "*.JPG"))
assert len(files) != 0, "ファイルが見つかりません。"

for file in files:
    os.rename(file, file.replace("JPG", "jpg"))
