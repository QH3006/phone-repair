"""
Script tự động kích hoạt Cloudflare Tunnel và hiển thị đường link demo rõ ràng 100%.
- Tự động kiểm tra / khởi động Backend FastAPI (Port 8000).
- Kết nối Cloudflare Tunnel và trích xuất đường link HTTPS công khai.
- Tự động copy link vào Clipboard (Ctrl + V).
- Tự động lưu link vào file DUONG_DAN_DEMO_CLOUD.txt.
- Tự động mở trình duyệt web.
"""
import os
import sys
import time
import re
import subprocess
import webbrowser

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXE_PATH = os.path.join(PROJECT_ROOT, "cloudflared.exe")

def is_backend_running():
    import urllib.request
    try:
        urllib.request.urlopen("http://127.0.0.1:8000/docs", timeout=1.5)
        return True
    except Exception:
        return False

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 68)
    print("      PHONECARE AI - TRÌNH KÍCH HOẠT CLOUDFLARE CLOUD DEMO")
    print("=" * 68)
    print()

    # 1. Kiểm tra Backend
    backend_proc = None
    if not is_backend_running():
        print("[1/3] Đang khởi động Backend FastAPI tại cổng 8000...", flush=True)
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        env["PYTHONUNBUFFERED"] = "1"
        backend_proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"],
            cwd=PROJECT_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env
        )
        for _ in range(20):
            if is_backend_running():
                break
            time.sleep(0.5)
    
    print("[1/3] Backend FastAPI đã sẵn sàng tại http://127.0.0.1:8000.", flush=True)

    # 2. Kiểm tra file cloudflared.exe
    if not os.path.exists(EXE_PATH):
        print(f"[LỖI] Không tìm thấy file {EXE_PATH}!", flush=True)
        print("Vui lòng đảm bảo file cloudflared.exe nằm tại thư mục gốc dự án.", flush=True)
        return

    # 3. Chạy Cloudflare Tunnel
    print("[2/3] Đang kết nối tới mạng lưới toàn cầu Cloudflare...", flush=True)
    print("      (Quá trình này mất khoảng 5 - 10 giây, vui lòng đợi...)", flush=True)

    tunnel_proc = subprocess.Popen(
        [EXE_PATH, "tunnel", "--url", "http://localhost:8000"],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        cwd=PROJECT_ROOT
    )

    url = None
    start_time = time.time()
    while time.time() - start_time < 35:
        line = tunnel_proc.stderr.readline()
        if not line:
            time.sleep(0.2)
            continue
        match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
        if match:
            url = match.group(0)
            break

    if not url:
        print("[LỖI] Không bắt được đường link Cloudflare sau 30 giây. Vui lòng thử lại!")
        tunnel_proc.terminate()
        return

    # 4. Sao chép vào Clipboard & Lưu file
    tracking_url = f"{url}/tracking"
    try:
        subprocess.run("clip", input=tracking_url.encode("utf-8"), shell=True)
    except Exception:
        pass

    txt_file = os.path.join(PROJECT_ROOT, "DUONG_DAN_DEMO_CLOUD.txt")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write("===============================================================\n")
        f.write("      LINK DEMO CLOUD TRỰC TIẾP HỆ THỐNG PHONECARE AI          \n")
        f.write("===============================================================\n\n")
        f.write(f"1. Cổng Tra cứu Khách hàng (Mở trên thiết bị di động / Trải nghiệm khách hàng):\n")
        f.write(f"   --> {tracking_url}\n\n")
        f.write(f"2. Giao diện Quản trị Nội bộ (Admin / Lễ tân / KTV):\n")
        f.write(f"   --> {url}/\n\n")
        f.write(f"3. Dữ liệu tài khoản demo sẵn:\n")
        f.write(f"   - Lễ tân: letan / 123456\n")
        f.write(f"   - Kỹ thuật viên: ktv / 123456\n")
        f.write(f"   - Mã phiếu mẫu tra cứu: PSC-20260917-001 (hoặc PSC-20260915-002)\n")
        f.write(f"   - SĐT mẫu tra cứu: 0988123456\n")
        f.write(f"   - IMEI mẫu tra cứu: 354892091234567\n")

    # In ra terminal rõ ràng, nổi bật
    print()
    print("=" * 68)
    print("           🎉 ĐÃ TẠO THÀNH CÔNG ĐƯỜNG LINK CLOUD DEMO!")
    print("=" * 68)
    print()
    print(" 📱 CỔNG TRA CỨU KHÁCH HÀNG (Mở trên điện thoại):")
    print(f"    --> {tracking_url}")
    print()
    print(" 💻 TRANG QUẢN TRỊ NỘI BỘ (Trên máy tính):")
    print(f"    --> {url}/")
    print()
    print(" 📋 ĐẶC BIỆT:")
    print("    * Link tra cứu đã được TỰ ĐỘNG COPY vào bộ nhớ tạm (Clipboard)!")
    print("      Bạn chỉ cần bấm Ctrl + V vào Zalo/Tin nhắn để gửi sang điện thoại.")
    print(f"    * Link cũng đã được lưu vào file: DUONG_DAN_DEMO_CLOUD.txt")
    print()
    print("=" * 68)
    print(" * Cửa sổ này đang duy trì kết nối Cloud. KHÔNG ĐƯỢC ĐÓNG CỬA SỔ NÀY.")
    print(" * Khi nào muốn dừng Demo, hãy bấm Ctrl + C để thoát.")
    print("=" * 68)

    # Tự động mở trình duyệt
    try:
        webbrowser.open(tracking_url)
    except Exception:
        pass

    # Giữ tiến trình chạy cho đến khi user bấm Ctrl+C
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n--> Đang đóng Cloudflare Tunnel...")
        tunnel_proc.terminate()
        if backend_proc:
            backend_proc.terminate()
        print("--> Đã tắt kết nối an toàn.")

if __name__ == "__main__":
    main()
