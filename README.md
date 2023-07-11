# dog-face-mosaic-ai

## environment
- venv

```powershell
py -3.9 -m venv env

.\env\Scripts\activate

pip install -U pip
pip install -r requirements.txt

```

## モザイク処理
```
python main.py --video /your/video/path --model /your/model/path
```

## warning
- 動画コーデックの違いで入力ファイルと若干の差異が出ることがある
- labelImg は Python3.9 以下で動作
- utils内のコードはREADME.mdの階層から実行