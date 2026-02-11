# Data Size Tracker

指定されたディレクトリ以下の全ファイルのサイズを再帰的にチェックし、実行ごとにCSVファイルに追記記録するツール。

## 機能

- ディレクトリ以下のすべてのファイルサイズを再帰的に計測
- 実行時刻とともにCSVファイルに追記（履歴を保持）
- ファイルアクセス不可の場合はスキップして続行
- コンソールに計測結果を表示

## 使い方

```bash
# 基本的な使用方法
python main.py /path/to/target/directory

# ログファイル名を指定する場合
python main.py /path/to/target/directory ./custom_log.csv
```

## ログファイル形式

CSVファイルに以下の情報が行追記されます：

```
timestamp,file_count,total_size_bytes,total_size_mb,target_directory
2025-01-15T10:30:45.123456,150,1073741824,1024.00,/path/to/directory
2025-01-15T11:45:22.654321,152,1099511627776,1048576.00,/path/to/directory
```

| カラム | 説明 |
|--------|------|
| timestamp | 計測時刻（ISO 8601形式） |
| file_count | ファイル数 |
| total_size_bytes | 合計サイズ（バイト） |
| total_size_mb | 合計サイズ（MB） |
| target_directory | 対象ディレクトリのパス |

## 例

```bash
# 作業ディレクトリを毎日追跡する場合
python main.py ~/Documents

# 2回目の実行でログに新しい行が追加される
# size_log.csv にはすべての計測履歴が保存される
```

## 出力例

```
✓ ログを記録しました: size_log.csv
  タイムスタンプ: 2025-01-15T10:30:45.123456
  ファイル数: 150
  合計サイズ: 1024.00 MB (1073741824 bytes)
  対象ディレクトリ: /path/to/directory
```

## テスト

包括的なユニットテストが実装されています。

### テストの実行

```bash
# 全テストを実行
python3 -m pytest tests/ -v

# テストカバレッジを確認
python3 -m pytest tests/ --cov=main

# 特定のテストクラスのみ実行
python3 -m pytest tests/test_main.py::TestGetDirectorySize -v
```

### テスト内容

- **初期化テスト** - 有効なディレクトリ、存在しないパス、ファイルパスなどの処理
- **サイズ計測テスト** - 空のディレクトリ、複数ファイル、ネストされたディレクトリの計測
- **ログファイル操作** - ファイル作成、ヘッダー、追記、CSV形式の検証
- **データフォーマット** - MB計算、タイムスタンプ形式の検証
- **エッジケース** - 空ファイル、特殊文字ファイル名、深いディレクトリ構造
- **コマンドラインI/F** - コンソール出力フォーマットの検証

### テスト結果

```
============================== 20 passed in 0.04s ==============================
```

