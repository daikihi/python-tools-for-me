# ファイル変換器 文字を入れ替えるくん

## このプログラムは何？

このプロフラムでは、inputs に入っているファイルを全て読み込んで、文字変換をしてoutput directory に出力します。基本的には、Linux や Mac などの Unix 系の OS を前提としていて、Windows 系の OS でのファイルは考えていません。

文言を入れ替えたい組み合わせを、dictonary 内にtxt_file としておいてください。文言は `from,to` のように 1 行に 1 組ずつおいてください。 1 行ずつであれば、ファイルは分岐しても問題ありません。

入力ファイル、dictonary ファイルは、各々任意の数置くことができます。

## 最初にやること

まず、python3 を前提とし、python3 はインストールされているものとします。

```bash
cd file-read-and-change-words
python3 -m venv .env
```

## 実行時にすること

とりあえず、実行時にはこのコマンドを実行して、環境を用意しましょう。

```bash 
cd file-read-and-change-words
source .env/bin/activate
```

## 実行方法

実行方法は簡単です。まずは、何もしないでただ実行したときはこのようになります。

```bash
python3 main.py 
Found 0 files in 'inputs' directory.
```
