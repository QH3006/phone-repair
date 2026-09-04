#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Sao Lưu & Phục Hồi Cơ Sở Dữ Liệu Tự Động (NFR-08: Database Backup & Recovery)
Đáp ứng tiêu chuẩn kỹ thuật KT1/KT2 cho dự án PhoneCare AI.
"""

import os
import sys
import shutil
import sqlite3
import argparse
from datetime import datetime
from typing import List, Dict, Any

# Hỗ trợ in tiếng Việt mượt mà trên Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Đường dẫn mặc định
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "phone_repair.db")
DEFAULT_BACKUP_DIR = os.path.join(BASE_DIR, "backups")


def ensure_backup_dir(backup_dir: str = DEFAULT_BACKUP_DIR) -> str:
    """Tạo thư mục lưu trữ bản sao lưu nếu chưa tồn tại."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def create_backup(db_path: str = DEFAULT_DB_PATH, backup_dir: str = DEFAULT_BACKUP_DIR) -> str:
    """
    Tạo bản snapshot sao lưu an toàn của file SQLite CSDL (sử dụng SQLite Backup API).
    Trả về đường dẫn file backup .bak đã tạo.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Không tìm thấy cơ sở dữ liệu tại: {db_path}")

    ensure_backup_dir(backup_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"phone_repair_{timestamp}.bak"
    backup_filepath = os.path.join(backup_dir, backup_filename)

    # Sử dụng SQLite Online Backup API để tránh bị lock bảng hoặc hỏng dữ liệu khi đang có ghi đồng thời
    src_conn = sqlite3.connect(db_path)
    dst_conn = sqlite3.connect(backup_filepath)
    try:
        with dst_conn:
            src_conn.backup(dst_conn, pages=100)
    finally:
        dst_conn.close()
        src_conn.close()

    file_size_kb = round(os.path.getsize(backup_filepath) / 1024, 2)
    print(f"[SUCCESS] Đã sao lưu CSDL thành công: {backup_filepath} ({file_size_kb} KB)")
    return backup_filepath


def list_backups(backup_dir: str = DEFAULT_BACKUP_DIR) -> List[Dict[str, Any]]:
    """Liệt kê danh sách các bản sao lưu hiện có trong thư mục backups/."""
    ensure_backup_dir(backup_dir)
    backups = []
    for f in os.listdir(backup_dir):
        if f.endswith(".bak"):
            full_path = os.path.join(backup_dir, f)
            stat = os.stat(full_path)
            backups.append({
                "filename": f,
                "path": full_path,
                "size_kb": round(stat.st_size / 1024, 2),
                "created_at": datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M:%S")
            })
    backups.sort(key=lambda x: x["filename"], reverse=True)
    return backups


def restore_backup(backup_filepath: str, target_db_path: str = DEFAULT_DB_PATH) -> bool:
    """
    Phục hồi cơ sở dữ liệu từ file backup .bak.
    Tạo bản lưu dự phòng của DB hiện tại trước khi đè dữ liệu.
    """
    if not os.path.exists(backup_filepath):
        raise FileNotFoundError(f"File backup không tồn tại: {backup_filepath}")

    # Kiểm tra tính toàn vẹn của file backup SQLite
    test_conn = sqlite3.connect(backup_filepath)
    try:
        cursor = test_conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        res = cursor.fetchone()
        if not res or res[0] != "ok":
            raise ValueError(f"File backup bị lỗi toàn vẹn: {res}")
    finally:
        test_conn.close()

    # Lưu bản tạm của DB hiện tại nếu đang có
    if os.path.exists(target_db_path):
        temp_safety_copy = f"{target_db_path}.safety_copy"
        shutil.copy2(target_db_path, temp_safety_copy)

    # Khôi phục file backup đè vào target_db_path
    shutil.copy2(backup_filepath, target_db_path)
    print(f"[SUCCESS] Đã phục hồi thành công CSDL từ: {backup_filepath}")
    return True


def main():
    parser = argparse.ArgumentParser(description="PhoneCare AI - Database Backup & Recovery Utility (NFR-08)")
    parser.add_argument("--backup", action="store_true", help="Tạo bản sao lưu snapshot mới")
    parser.add_argument("--list", action="store_true", help="Liệt kê danh sách các bản sao lưu")
    parser.add_argument("--restore", type=str, help="Đường dẫn file .bak để phục hồi CSDL")
    args = parser.parse_args()

    if args.list:
        backups = list_backups()
        if not backups:
            print("[INFO] Chưa có bản sao lưu nào trong thư mục backups/")
        else:
            print(f"=== DANH SÁCH BẢN SAO LƯU ({len(backups)} bản) ===")
            for idx, b in enumerate(backups, 1):
                print(f"{idx}. {b['filename']} | {b['size_kb']} KB | Thời gian: {b['created_at']}")
    elif args.restore:
        restore_backup(args.restore)
    else:
        # Mặc định tạo backup
        create_backup()


if __name__ == "__main__":
    main()
