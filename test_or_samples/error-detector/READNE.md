# Log からエラーを検出して何とかしてあげよう君

このプロジェクトでは、ファイルに吐き出されるLog を観測して、ERROR の場合にはなんとかしようと言うものです。

なんとか：メールで送信するか、Slack などに通知するか・・・あたり？

## 構成要素

- dymmy_log_generator.py

これは、テストのために、ランダムにSleep しながら、Info, Warning, INFO を出すプログラムです。


## 最初にやること

まず、python3 を前提とし、python3 はインストールされているものとします。

```bash
cd file-read-and-change-words
python3 -m venv .env
mkdir inputs
mkdir outputs
mkdir dictionary
```

## 実行時にすること

とりあえず、実行時にはこのコマンドを実行して、環境を用意しましょう。

```bash 
cd file-read-and-change-words 
source .env/bin/activate
```


