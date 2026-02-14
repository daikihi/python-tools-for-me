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
```

## 実行時にすること

とりあえず、実行時にはこのコマンドを実行して、環境を用意しましょう。

```bash 
cd test_or_samples/error-detector
source .env/bin/activate
touch last_executed_data.txt
```

# dymmy_error_generator

適当にランダムな間隔で、ランダムなログレベルでLog っぽいものを出力してくれる君です

`last_executed_data.txt` というファイルに、最終実行時間を記録します。その実行時間から `_TIME_DIFF_THRESHOLD_SECONDS` 秒以上時間が空いていたら、エラーを上げる。

## sample output

```
2025-09-15 15:51:50,848 - INFO - this is info log : dummy log 10 : wait for 239 ms
2025-09-15 15:51:51,156 - INFO - this is info log : dummy log 11 : wait for 215 ms
2025-09-15 15:51:51,375 - ERROR - this is error log : dummy log 12 : wait for 469 ms
2025-09-15 15:51:51,849 - WARNING - this is warning log : dummy log 13 : wait for 805 ms
2025-09-15 15:51:52,659 - ERROR - this is error log : dummy log 14 : wait for 480 ms
2025-09-15 15:51:53,142 - WARNING - this is warning log : dummy log 15 : wait for 757 ms
```

# check_fleshness_of_timestamp_on_file.py

最終実行時間監視君

このプログラムでは、自分が最終実行時間から一定時間実行されていなかった場合に。エラーをあげます。

本来は、別のプログラムが実行されているか確認するためですが、今回は事故実行を確認しています。

## sample output 

```
ERROR DETECTION - start
load condition file
last executed time : 2025-09-22 23:16:46
last exec time : 2025-09-22 23:16:46, now 2025-09-22 23:16:47.934711
diff : 1.934711
```

## sample error output

仮に、エラーが上がったとしても、ファイルには書き込む様になっています。

本来は、別のプログラムがファイルを書き込みますが、今回は自己実行をチェックしています。

`last_executed_data.txt` は初回実行時は空かもしれないので、実行が落ちる可能性もあります。

```
ERROR DETECTION - start
load condition file
last executed time : 2025-09-22 23:14:56
last exec time : 2025-09-22 23:14:56, now 2025-09-22 23:16:44.339707
diff : 108.339707
error detected : error detector seems not working. last exec time is too old. diff seconds : 108.339707
```