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
cd test_or_samples/error-detector
source .env/bin/activate
```

# dymmy_error_generator

適当にランダムな間隔で、ランダムなログレベルでLog っぽいものを出力してくれる君です

## sample output

```
2025-09-15 15:51:50,848 - INFO - this is info log : dummy log 10 : wait for 239 ms
2025-09-15 15:51:51,156 - INFO - this is info log : dummy log 11 : wait for 215 ms
2025-09-15 15:51:51,375 - ERROR - this is error log : dummy log 12 : wait for 469 ms
2025-09-15 15:51:51,849 - WARNING - this is warning log : dummy log 13 : wait for 805 ms
2025-09-15 15:51:52,659 - ERROR - this is error log : dummy log 14 : wait for 480 ms
2025-09-15 15:51:53,142 - WARNING - this is warning log : dummy log 15 : wait for 757 ms
```

