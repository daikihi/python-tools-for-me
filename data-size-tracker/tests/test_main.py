"""
Data Size Tracker のテストスイート

DataSizeTrackerクラスの機能をテストします。
"""

import unittest
import tempfile
import csv
import os
from pathlib import Path
from datetime import datetime
from io import StringIO
import sys

# テスト対象モジュールのインポート
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import DataSizeTracker


class TestDataSizeTrackerInitialization(unittest.TestCase):
    """DataSizeTrackerの初期化に関するテスト"""
    
    def setUp(self):
        """各テストの前に実行"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
    
    def tearDown(self):
        """各テストの後に実行"""
        self.temp_dir.cleanup()
    
    def test_init_with_valid_directory(self):
        """✓ 有効なディレクトリで初期化できる"""
        tracker = DataSizeTracker(str(self.test_dir))
        # パスの正規化を考慮
        self.assertEqual(tracker.target_dir, Path(self.test_dir).resolve())
    
    def test_init_with_nonexistent_directory(self):
        """✗ 存在しないディレクトリで初期化するとエラー"""
        with self.assertRaises(FileNotFoundError):
            DataSizeTracker("/nonexistent/path/to/directory")
    
    def test_init_with_file_instead_of_directory(self):
        """✗ ファイルパスでは初期化できない"""
        test_file = self.test_dir / "test.txt"
        test_file.write_text("test content")
        
        with self.assertRaises(NotADirectoryError):
            DataSizeTracker(str(test_file))
    
    def test_custom_log_file_path(self):
        """✓ カスタムログファイルパスを設定できる"""
        log_path = self.test_dir / "custom_log.csv"
        tracker = DataSizeTracker(str(self.test_dir), str(log_path))
        self.assertEqual(tracker.log_file, log_path)


class TestGetDirectorySize(unittest.TestCase):
    """ディレクトリサイズ計測のテスト"""
    
    def setUp(self):
        """各テストの前に実行"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
        self.tracker = DataSizeTracker(str(self.test_dir))
    
    def tearDown(self):
        """各テストの後に実行"""
        self.temp_dir.cleanup()
    
    def test_empty_directory(self):
        """✓ 空のディレクトリではファイル数0、サイズ0"""
        file_count, total_size = self.tracker.get_directory_size()
        self.assertEqual(file_count, 0)
        self.assertEqual(total_size, 0)
    
    def test_single_file(self):
        """✓ ファイルが1つ存在する場合"""
        test_content = "Hello, World!"
        test_file = self.test_dir / "test.txt"
        test_file.write_text(test_content)
        
        file_count, total_size = self.tracker.get_directory_size()
        self.assertEqual(file_count, 1)
        self.assertEqual(total_size, len(test_content.encode('utf-8')))
    
    def test_multiple_files(self):
        """✓ 複数のファイルが正しく計測される"""
        files_content = {
            "file1.txt": "content1",
            "file2.txt": "content2",
            "file3.txt": "content3",
        }
        
        expected_size = 0
        for filename, content in files_content.items():
            file_path = self.test_dir / filename
            file_path.write_text(content)
            expected_size += len(content.encode('utf-8'))
        
        file_count, total_size = self.tracker.get_directory_size()
        self.assertEqual(file_count, 3)
        self.assertEqual(total_size, expected_size)
    
    def test_nested_directories(self):
        """✓ ネストされたディレクトリも再帰的に計測"""
        # ディレクトリ構造を作成
        subdir1 = self.test_dir / "subdir1"
        subdir2 = self.test_dir / "subdir2" / "nested"
        subdir1.mkdir()
        subdir2.mkdir(parents=True)
        
        # ファイルを配置
        (self.test_dir / "file1.txt").write_text("content1")
        (subdir1 / "file2.txt").write_text("content2")
        (subdir2 / "file3.txt").write_text("content3")
        
        file_count, total_size = self.tracker.get_directory_size()
        self.assertEqual(file_count, 3)
        
        expected_size = sum(len(c.encode('utf-8')) for c in ["content1", "content2", "content3"])
        self.assertEqual(total_size, expected_size)
    
    def test_handles_permission_errors(self):
        """✓ アクセス不可ファイルもスキップして続行"""
        # アクセス可能なファイル
        (self.test_dir / "readable.txt").write_text("readable content")
        
        # アクセス不可ファイル
        unreadable_file = self.test_dir / "unreadable.txt"
        unreadable_file.write_text("unreadable content")
        
        # ファイルのパーミッションを変更（アクセス不可）
        os.chmod(str(unreadable_file), 0o000)
        
        try:
            # エラーが発生せずに実行される
            file_count, total_size = self.tracker.get_directory_size()
            # readableファイルが計測されている（unreadableはスキップ）
            self.assertGreaterEqual(file_count, 1)
        finally:
            # テスト後、パーミッションを戻して削除可能に
            os.chmod(str(unreadable_file), 0o644)


class TestLogFileOperations(unittest.TestCase):
    """ログファイル操作のテスト"""
    
    def setUp(self):
        """各テストの前に実行"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
        self.log_file = Path(self.temp_dir.name) / "test_log.csv"
        self.tracker = DataSizeTracker(str(self.test_dir), str(self.log_file))
    
    def tearDown(self):
        """各テストの後に実行"""
        self.temp_dir.cleanup()
    
    def test_log_file_creation(self):
        """✓ ログファイルが作成される"""
        self.assertFalse(self.log_file.exists())
        self.tracker._init_log_file()
        self.assertTrue(self.log_file.exists())
    
    def test_log_file_has_header(self):
        """✓ ログファイルヘッダーが正しい"""
        self.tracker._init_log_file()
        
        with open(self.log_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
        
        expected_header = [
            "timestamp",
            "file_count",
            "total_size_bytes",
            "total_size_mb",
            "target_directory"
        ]
        self.assertEqual(header, expected_header)
    
    def test_track_single_execution(self):
        """✓ 1回の実行でログが記録される"""
        # テストファイルを作成
        (self.test_dir / "file.txt").write_text("test content")
        
        # キャビチャー出力
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            self.tracker.track()
        finally:
            sys.stdout = sys.__stdout__
        
        # ログファイルに1行のデータが記録されている
        with open(self.log_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            data_rows = list(reader)
        
        self.assertEqual(len(data_rows), 1, "ログに1行のデータが記録されるべき")
        
        # 記録されたデータを検証
        row = data_rows[0]
        self.assertEqual(len(row), 5, "各行は5つのカラムを持つべき")
        
        # 個別のカラムを検証
        timestamp_str = row[0]
        file_count_str = row[1]
        total_size_bytes_str = row[2]
        total_size_mb_str = row[3]
        target_dir = row[4]
        
        # タイムスタンプはISO形式
        datetime.fromisoformat(timestamp_str)  # エラーが発生しない
        
        # ファイル数とサイズは数値（1以上あることを確認）
        file_count = int(file_count_str)
        self.assertGreaterEqual(file_count, 1)
        total_bytes = int(total_size_bytes_str)
        self.assertGreater(total_bytes, 0)
        # MB値は計算結果として記録される（小さいファイルは0.00になる可能性あり）
        self.assertGreaterEqual(float(total_size_mb_str), 0)
        
        # ディレクトリパス（正規化を考慮）
        self.assertEqual(Path(target_dir).resolve(), Path(self.test_dir).resolve())
    
    def test_track_multiple_executions(self):
        """✓ 複数回の実行でデータが追記される"""
        (self.test_dir / "file.txt").write_text("test")
        
        # 1回目の実行
        captured_output = StringIO()
        sys.stdout = captured_output
        self.tracker.track()
        sys.stdout = sys.__stdout__
        
        # 2回目の実行
        captured_output = StringIO()
        sys.stdout = captured_output
        self.tracker.track()
        sys.stdout = sys.__stdout__
        
        # ログにヘッダー + 2行のデータがある
        with open(self.log_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            data_rows = list(reader)
        
        self.assertEqual(len(data_rows), 2, "ログに2行のデータが追記されるべき")
    
    def test_csv_format_validity(self):
        """✓ CSVファイルのフォーマットが有効"""
        (self.test_dir / "file.txt").write_text("test")
        
        captured_output = StringIO()
        sys.stdout = captured_output
        self.tracker.track()
        sys.stdout = sys.__stdout__
        
        # CSVファイルが正常に読み込める（フォーマットエラーなし）
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        self.assertEqual(len(rows), 1)
        row = rows[0]
        
        # すべてのキーが存在
        required_keys = [
            "timestamp",
            "file_count",
            "total_size_bytes",
            "total_size_mb",
            "target_directory"
        ]
        for key in required_keys:
            self.assertIn(key, row)
            self.assertIsNotNone(row[key])


class TestDataFormatting(unittest.TestCase):
    """データフォーマットのテスト"""
    
    def setUp(self):
        """各テストの前に実行"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
        self.log_file = Path(self.temp_dir.name) / "test_log.csv"
        self.tracker = DataSizeTracker(str(self.test_dir), str(self.log_file))
    
    def tearDown(self):
        """各テストの後に実行"""
        self.temp_dir.cleanup()
    
    def test_size_mb_calculation(self):
        """✓ MBサイズが正しく計算される"""
        # 1MB相当のファイルを作成
        one_mb_bytes = 1024 * 1024
        test_file = self.test_dir / "large_file.bin"
        test_file.write_bytes(b'0' * one_mb_bytes)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        self.tracker.track()
        sys.stdout = sys.__stdout__
        
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            row = next(reader)
        
        total_size_bytes = int(row['total_size_bytes'])
        total_size_mb = float(row['total_size_mb'])
        
        # バイト数とMB数の関係が正しい
        calculated_mb = total_size_bytes / (1024 * 1024)
        self.assertAlmostEqual(float(total_size_mb), calculated_mb, places=2)
    
    def test_timestamp_format(self):
        """✓ タイムスタンプがISO 8601形式"""
        captured_output = StringIO()
        sys.stdout = captured_output
        self.tracker.track()
        sys.stdout = sys.__stdout__
        
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            row = next(reader)
        
        timestamp = row['timestamp']
        
        # ISO形式として解析できる
        dt = datetime.fromisoformat(timestamp)
        self.assertIsInstance(dt, datetime)


class TestEdgeCases(unittest.TestCase):
    """エッジケースのテスト"""
    
    def setUp(self):
        """各テストの前に実行"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
        self.log_file = Path(self.temp_dir.name) / "test_log.csv"
        self.tracker = DataSizeTracker(str(self.test_dir), str(self.log_file))
    
    def tearDown(self):
        """各テストの後に実行"""
        self.temp_dir.cleanup()
    
    def test_empty_file(self):
        """✓ サイズ0のファイルも計測対象"""
        (self.test_dir / "empty.txt").write_text("")
        
        file_count, total_size = self.tracker.get_directory_size()
        self.assertEqual(file_count, 1)
        self.assertEqual(total_size, 0)
    
    def test_special_characters_in_filename(self):
        """✓ 特殊文字を含むファイル名でも動作"""
        (self.test_dir / "file with spaces.txt").write_text("content")
        (self.test_dir / "ファイル.txt").write_text("内容")
        
        file_count, total_size = self.tracker.get_directory_size()
        self.assertEqual(file_count, 2)
        self.assertGreater(total_size, 0)
    
    def test_deeply_nested_directories(self):
        """✓ 深くネストされたディレクトリを処理"""
        # 深いディレクトリ構造を作成
        deep_path = self.test_dir / "a" / "b" / "c" / "d" / "e" / "f"
        deep_path.mkdir(parents=True)
        (deep_path / "deep_file.txt").write_text("deep content")
        
        file_count, total_size = self.tracker.get_directory_size()
        self.assertEqual(file_count, 1)
        self.assertGreater(total_size, 0)


class TestCommandLineInterface(unittest.TestCase):
    """コマンドラインインターフェースのテスト"""
    
    def setUp(self):
        """各テストの前に実行"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
        self.log_file = Path(self.temp_dir.name) / "test_log.csv"
    
    def tearDown(self):
        """各テストの後に実行"""
        self.temp_dir.cleanup()
    
    def test_output_format(self):
        """✓ コンソール出力フォーマットが正しい"""
        (Path(self.test_dir) / "file.txt").write_text("test")
        tracker = DataSizeTracker(str(self.test_dir), str(self.log_file))
        
        captured_output = StringIO()
        sys.stdout = captured_output
        tracker.track()
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        
        # 出力に必要な情報が含まれている
        self.assertIn("✓ ログを記録しました", output)
        self.assertIn("タイムスタンプ:", output)
        self.assertIn("ファイル数:", output)
        self.assertIn("合計サイズ:", output)
        self.assertIn("対象ディレクトリ:", output)


if __name__ == "__main__":
    unittest.main()
