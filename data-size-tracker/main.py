#!/usr/bin/env python3
"""
Data Size Tracker

指定されたディレクトリ以下のファイルサイズを再帰的に確認し、
実行ごとにログファイルに1行追記する
"""

import os
import sys
import csv
from datetime import datetime
from pathlib import Path
from typing import Tuple


class DataSizeTracker:
    """ディレクトリのデータサイズを追跡するクラス"""

    def __init__(self, target_dir: str, log_file: str = "size_log.csv"):
        """
        初期化
        
        Args:
            target_dir: サイズを計測したいディレクトリパス
            log_file: ログを保存するCSVファイルのパス
        """
        self.target_dir = Path(target_dir).resolve()
        self.log_file = Path(log_file)
        
        if not self.target_dir.exists():
            raise FileNotFoundError(f"ディレクトリが見つかりません: {self.target_dir}")
        
        if not self.target_dir.is_dir():
            raise NotADirectoryError(f"これはディレクトリではありません: {self.target_dir}")
    
    def get_directory_size(self) -> Tuple[int, int]:
        """
        ディレクトリ以下の全ファイルの合計サイズとファイル数を取得
        
        Returns:
            (ファイル数, 合計サイズ(バイト))
        """
        total_size = 0
        file_count = 0
        
        for file_path in self.target_dir.rglob("*"):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                    file_count += 1
                except (OSError, PermissionError):
                    # ファイルにアクセスできない場合はスキップ
                    print(f"警告: アクセスできません: {file_path}")
        
        return file_count, total_size
    
    def _init_log_file(self):
        """ログファイルが存在しない場合、ヘッダーを作成"""
        if not self.log_file.exists():
            with open(self.log_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "file_count",
                    "total_size_bytes",
                    "total_size_mb",
                    "target_directory"
                ])
    
    def track(self):
        """ディレクトリサイズを計測してログに記録"""
        # ログファイルの初期化
        self._init_log_file()
        
        # サイズ計測
        file_count, total_size = self.get_directory_size()
        total_size_mb = total_size / (1024 * 1024)
        
        # ログに追記
        timestamp = datetime.now().isoformat()
        with open(self.log_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                file_count,
                total_size,
                f"{total_size_mb:.2f}",
                str(self.target_dir)
            ])
        
        # コンソール出力
        print(f"✓ ログを記録しました: {self.log_file}")
        print(f"  タイムスタンプ: {timestamp}")
        print(f"  ファイル数: {file_count}")
        print(f"  合計サイズ: {total_size_mb:.2f} MB ({total_size:,} bytes)")
        print(f"  対象ディレクトリ: {self.target_dir}")


def main():
    """メイン処理"""
    if len(sys.argv) < 2:
        print("使い方: python main.py <target_directory> [log_file]")
        print("例: python main.py /path/to/dir")
        print("例: python main.py /path/to/dir ./my_log.csv")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    log_file = sys.argv[2] if len(sys.argv) > 2 else "size_log.csv"
    
    try:
        tracker = DataSizeTracker(target_dir, log_file)
        tracker.track()
    except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"予期しないエラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
