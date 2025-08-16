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

```bssh
```

# サンプルの出典

サンプルデータは、以下のサイトから持ってきたものを NKF を使って文字コードを utf-8 に変換した。また最後の２行は削除した。

政府統計の総合窓口(e-Stat)　https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200521&tstat=000001011777&cycle=0&tclass1=000001094741&tclass2val=0

https://www.e-stat.go.jp/terms-of-use