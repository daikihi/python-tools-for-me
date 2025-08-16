# CSV ファイルの一部の情報をマスキングしちゃうツール

CSV ファイルのサンプルがほしい時に、個人情報等が入っていると、渡せない・もらえないので、そう言った情報はマスキングしちゃえふぁいる

Mac や Linux を前提としており、Windows の場合はわかりません。

# 初回の実行

python の仮想環境を作りましょう

```bash
python3 -m venv ./env
```

# 初回を含め毎回実行するコマンド

```bash 
source ./env/bin/activate
```

# 実行時

```
python3 masking-file.py input_file_name output_file_name masking_columns_csv
```

- input_file_name : 入力ファイル名
- output_file_name : 出力ファイル名、既に同一ファイル名が存在する場合には、勝手に上書きされ前のデータはなくなります
- masking_columns_csv : マスキングするカラム名：０からカウントしてください

input_file_name とoutput_file_name が同じ場合は、安全のため動かなくしてあります

```bssh
python3 masking-file.py ./sample-csv.csv output_20250816.csv 1,2,3,4,5
```

# サンプルの出典

サンプルデータは、以下のサイトから持ってきたものを NKF を使って文字コードを utf-8 に変換した。また最後の２行は削除した。

政府統計の総合窓口(e-Stat)　https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200521&tstat=000001011777&cycle=0&tclass1=000001094741&tclass2val=0

https://www.e-stat.go.jp/terms-of-use