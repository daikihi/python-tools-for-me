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
from typing import Tuple, List
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


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


class DataSizeVisualizer:
    """サイズログをグラフ化するクラス"""
    
    def __init__(self, log_file: str = "size_log.csv"):
        """
        初期化
        
        Args:
            log_file: ログCSVファイルのパス
        """
        self.log_file = Path(log_file)
        
        if not self.log_file.exists():
            raise FileNotFoundError(f"ログファイルが見つかりません: {self.log_file}")
    
    def read_log_data(self) -> Tuple[List[datetime], List[float]]:
        """
        ログファイルからタイムスタンプとサイズを読み込む
        ヘッダーの有無に対応
        
        Returns:
            (タイムスタンプリスト, データサイズMBリスト)
        """
        timestamps = []
        sizes_mb = []
        
        with open(self.log_file, "r") as f:
            lines = f.readlines()
            
        if not lines:
            raise ValueError("ログファイルが空です")
        
        # ヘッダーを有するか判定（最初の行が ISO フォーマットの日時から始まるか）
        first_line = lines[0].strip()
        has_header = not first_line.startswith("2")  # タイムスタンプは通常 "2026-" など "2" で始まる
        
        start_idx = 1 if has_header else 0
        
        # CSVを行ごとに処理
        for line in lines[start_idx:]:
            if not line.strip():
                continue
            
            try:
                parts = line.strip().split(",")
                if len(parts) >= 4:
                    timestamp_str = parts[0]
                    size_mb_str = parts[3]
                    
                    ts = datetime.fromisoformat(timestamp_str)
                    timestamps.append(ts)
                    
                    size_mb = float(size_mb_str)
                    sizes_mb.append(size_mb)
            except (ValueError, IndexError) as e:
                print(f"警告: 行の解析に失敗しました: {e}")
                continue
        
        if not timestamps:
            raise ValueError("ログファイルにデータが見つかりません")
        
        return timestamps, sizes_mb
    
    def plot_size_trend(self, output_file: str = "size_trend.png"):
        """
        データサイズの推移を折れ線グラフで表示
        
        Args:
            output_file: グラフを保存するファイル名
        """
        timestamps, sizes_mb = self.read_log_data()
        
        # グラフの設定
        plt.figure(figsize=(12, 6))
        
        # 折れ線グラフをプロット
        plt.plot(timestamps, sizes_mb, marker="o", linestyle="-", linewidth=2, 
                markersize=6, color="#1f77b4", label="Data Size")
        
        # X軸の設定（時系列を明確に）
        ax = plt.gca()
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d %H:%M:%S"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha="right")
        
        # ラベルと タイトル
        plt.xlabel("Timestamp", fontsize=12, fontweight="bold")
        plt.ylabel("Data Size (MB)", fontsize=12, fontweight="bold")
        plt.title("Data Size Trend Over Time", fontsize=14, fontweight="bold")
        
        # グリッドを追加（時系列が分かりやすくするため）
        plt.grid(True, alpha=0.3, linestyle="--")
        
        # Y軸の最小値を0から開始（嘘のないグラフ）
        plt.ylim(bottom=0)
        
        # レジェンド
        plt.legend(loc="best")
        
        # レイアウトを調整
        plt.tight_layout()
        
        # ファイルに保存
        plt.savefig(output_file, dpi=100, bbox_inches="tight")
        print(f"✓ グラフを保存しました: {output_file}")


def main():
    """メイン処理"""
    if len(sys.argv) < 2:
        print("使い方:")
        print("  python main.py <target_directory> [log_file]  # ログに記録")
        print("  python main.py --plot [log_file]              # グラフを表示")
        print("")
        print("例:")
        print("  python main.py /path/to/dir")
        print("  python main.py /path/to/dir ./my_log.csv")
        print("  python main.py --plot")
        print("  python main.py --plot ./my_log.csv")
        sys.exit(1)
    
    # グラフ表示モード
    if sys.argv[1] == "--plot":
        log_file = sys.argv[2] if len(sys.argv) > 2 else "size_log.csv"
        try:
            visualizer = DataSizeVisualizer(log_file)
            visualizer.plot_size_trend()
        except (FileNotFoundError, ValueError) as e:
            print(f"エラー: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"予期しないエラー: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # ログ記録モード
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
