from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from backend.app.db.database import get_db
from backend.app.db.models import (
    PhieuSuaChua, KhachHang, ThietBi, NguoiDung, LinhKien, DichVu, ChiTietSuaChua, HoaDon, BaoHanh
)
from backend.app.core.security import require_roles, get_current_user
from backend.app.schemas.schemas import (
    CreateRepairTicketRequest, UpdateRepairStatusRequest, AssignKTVRequest,
    RepairTicketOut, RepairDetailCreate, RepairDetailOut
)

router = APIRouter(prefix="/repairs", tags=["Quản lý Phiếu Sửa Chữa"])

@router.get("", response_model=List[RepairTicketOut])
def list_repairs(
    q: Optional[str] = Query(None, description="Tìm kiếm theo Mã phiếu, SĐT, Tên khách hoặc IMEI"),
    trang_thai: Optional[str] = Query(None, description="Lọc theo trạng thái"),
    ktv_id: Optional[int] = Query(None, description="Lọc theo KTV phụ trách"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user)
):
    """Lấy danh sách phiếu sửa chữa có tìm kiếm đa trường và bộ lọc."""
    query = db.query(PhieuSuaChua)
    
    if trang_thai:
        query = query.filter(PhieuSuaChua.trang_thai == trang_thai)
    if ktv_id:
        query = query.filter(PhieuSuaChua.ktv_id == ktv_id)
    if q:
        search = f"%{q.strip()}%"
        query = query.join(PhieuSuaChua.khach_hang).join(PhieuSuaChua.thiet_bi).filter(
            (PhieuSuaChua.ma_phieu.ilike(search)) |
            (KhachHang.ho_ten.ilike(search)) |
            (KhachHang.so_dien_thoai.ilike(search)) |
            (ThietBi.so_imei.ilike(search)) |
            (ThietBi.model_may.ilike(search))
        )
    
    repairs = query.order_by(PhieuSuaChua.id.desc()).offset(skip).limit(limit).all()
    
    result = []
    for r in repairs:
        # Build details list
        details = []
        for ct in r.chi_tiet:
            ten_muc = ct.linh_kien.ten_linh_kien if ct.linh_kien else (ct.dich_vu.ten_dich_vu if ct.dich_vu else "N/A")
            loai = "LinhKien" if ct.linh_kien else "DichVu"
            details.append(RepairDetailOut(
                id=ct.id,
                phieu_sua_chua_id=ct.phieu_sua_chua_id,
                linh_kien_id=ct.linh_kien_id,
                dich_vu_id=ct.dich_vu_id,
                ten_muc=ten_muc,
                loai=loai,
                so_luong=ct.so_luong,
                don_gia=ct.don_gia,
                thanh_tien=ct.thanh_tien
            ))

        result.append(RepairTicketOut(
            id=r.id,
            ma_phieu=r.ma_phieu,
            khach_hang_id=r.khach_hang_id,
            thiet_bi_id=r.thiet_bi_id,
            khach_hang={
                "id": r.khach_hang.id,
                "ho_ten": r.khach_hang.ho_ten,
                "so_dien_thoai": r.khach_hang.so_dien_thoai,
                "dia_chi": r.khach_hang.dia_chi
            },
            thiet_bi={
                "id": r.thiet_bi.id,
                "hang_san_xuat": r.thiet_bi.hang_san_xuat,
                "model_may": r.thiet_bi.model_may,
                "so_imei": r.thiet_bi.so_imei,
                "mat_khau_may": r.thiet_bi.mat_khau_may
            },
            mo_ta_loi_khach=r.mo_ta_loi_khach,
            ghi_chu_ky_thuat=r.ghi_chu_ky_thuat,
            hinh_anh=r.hinh_anh,
            ai_tom_tat_loi=r.ai_tom_tat_loi,
            ai_giai_thich_dv=r.ai_giai_thich_dv,
            trang_thai=r.trang_thai,
            tong_tien_du_kien=r.tong_tien_du_kien or 0.0,
            ktv_id=r.ktv_id,
            ktv_phu_trach=r.ktv.ho_ten if r.ktv else "Chưa phân công",
            le_tan_id=r.le_tan_id,
            le_tan_tiep_nhan=r.le_tan.ho_ten if r.le_tan else "Lễ tân",
            ngay_tiep_nhan=r.ngay_tiep_nhan.strftime("%d/%m/%Y %H:%M") if r.ngay_tiep_nhan else None,
            ngay_hen_tra=r.ngay_hen_tra.strftime("%d/%m/%Y %H:%M") if r.ngay_hen_tra else None,
            ngay_hoan_tat=r.ngay_hoan_tat.strftime("%d/%m/%Y %H:%M") if r.ngay_hoan_tat else None,
            chi_tiet=details,
            da_thanh_toan=True if r.hoa_don else False,
            co_bao_hanh=True if len(r.bao_hanh) > 0 else False
        ))
    return result

@router.get("/{phieu_id}", response_model=RepairTicketOut)
def get_repair_detail(phieu_id: int, db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    """Xem thông tin chi tiết một phiếu sửa chữa."""
    r = db.query(PhieuSuaChua).filter(PhieuSuaChua.id == phieu_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu sửa chữa.")

    details = []
    for ct in r.chi_tiet:
        ten_muc = ct.linh_kien.ten_linh_kien if ct.linh_kien else (ct.dich_vu.ten_dich_vu if ct.dich_vu else "N/A")
        loai = "LinhKien" if ct.linh_kien else "DichVu"
        details.append(RepairDetailOut(
            id=ct.id,
            phieu_sua_chua_id=ct.phieu_sua_chua_id,
            linh_kien_id=ct.linh_kien_id,
            dich_vu_id=ct.dich_vu_id,
            ten_muc=ten_muc,
            loai=loai,
            so_luong=ct.so_luong,
            don_gia=ct.don_gia,
            thanh_tien=ct.thanh_tien
        ))

    return RepairTicketOut(
        id=r.id,
        ma_phieu=r.ma_phieu,
        khach_hang_id=r.khach_hang_id,
        thiet_bi_id=r.thiet_bi_id,
        khach_hang={
            "id": r.khach_hang.id,
            "ho_ten": r.khach_hang.ho_ten,
            "so_dien_thoai": r.khach_hang.so_dien_thoai,
            "dia_chi": r.khach_hang.dia_chi
        },
        thiet_bi={
            "id": r.thiet_bi.id,
            "hang_san_xuat": r.thiet_bi.hang_san_xuat,
            "model_may": r.thiet_bi.model_may,
            "so_imei": r.thiet_bi.so_imei,
            "mat_khau_may": r.thiet_bi.mat_khau_may
        },
        mo_ta_loi_khach=r.mo_ta_loi_khach,
        ghi_chu_ky_thuat=r.ghi_chu_ky_thuat,
        hinh_anh=r.hinh_anh,
        ai_tom_tat_loi=r.ai_tom_tat_loi,
        ai_giai_thich_dv=r.ai_giai_thich_dv,
        trang_thai=r.trang_thai,
        tong_tien_du_kien=r.tong_tien_du_kien or 0.0,
        ktv_id=r.ktv_id,
        ktv_phu_trach=r.ktv.ho_ten if r.ktv else "Chưa phân công",
        le_tan_id=r.le_tan_id,
        le_tan_tiep_nhan=r.le_tan.ho_ten if r.le_tan else "Lễ tân",
        ngay_tiep_nhan=r.ngay_tiep_nhan.strftime("%d/%m/%Y %H:%M") if r.ngay_tiep_nhan else None,
        ngay_hen_tra=r.ngay_hen_tra.strftime("%d/%m/%Y %H:%M") if r.ngay_hen_tra else None,
        ngay_hoan_tat=r.ngay_hoan_tat.strftime("%d/%m/%Y %H:%M") if r.ngay_hoan_tat else None,
        chi_tiet=details,
        da_thanh_toan=True if r.hoa_don else False,
        co_bao_hanh=True if len(r.bao_hanh) > 0 else False
    )

@router.post("", status_code=status.HTTP_201_CREATED)
def create_repair_ticket(
    req: CreateRepairTicketRequest,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "LeTan"]))
):
    """Tạo mới hồ sơ Khách hàng + Thiết bị + Phiếu tiếp nhận sửa chữa."""
    # 1. Tìm hoặc tạo khách hàng
    phone = req.so_dien_thoai.strip()
    khach_hang = db.query(KhachHang).filter(KhachHang.so_dien_thoai == phone).first()
    if not khach_hang:
        khach_hang = KhachHang(
            ho_ten=req.ho_ten.strip(),
            so_dien_thoai=phone,
            dia_chi=req.dia_chi.strip() if req.dia_chi else None
        )
        db.add(khach_hang)
        db.flush()
    else:
        if req.ho_ten:
            khach_hang.ho_ten = req.ho_ten.strip()
        if req.dia_chi:
            khach_hang.dia_chi = req.dia_chi.strip()
        db.flush()

    # 2. Tạo thiết bị
    imei = req.so_imei.strip() if req.so_imei else f"IMEI-{int(datetime.utcnow().timestamp())}"
    thiet_bi = db.query(ThietBi).filter(ThietBi.so_imei == imei).first()
    if not thiet_bi:
        thiet_bi = ThietBi(
            khach_hang_id=khach_hang.id,
            hang_san_xuat=req.hang_san_xuat.strip(),
            model_may=req.model_may.strip(),
            so_imei=imei,
            mat_khau_may=req.mat_khau_may.strip() if req.mat_khau_may else None
        )
        db.add(thiet_bi)
        db.flush()

    # 3. Sinh mã phiếu tự động
    today_str = datetime.utcnow().strftime("%Y%m%d")
    count_today = db.query(PhieuSuaChua).filter(PhieuSuaChua.ma_phieu.like(f"PSC-{today_str}-%")).count()
    ma_phieu = f"PSC-{today_str}-{count_today + 1:03d}"

    # 4. Xác định người tiếp nhận & KTV
    le_tan_id = current_user.id if current_user else (req.le_tan_id or 1)
    
    ktv_id = req.ktv_id
    if not ktv_id:
        ktv_user = db.query(NguoiDung).filter(NguoiDung.vai_tro == "KyThuatVien").first()
        if ktv_user:
            ktv_id = ktv_user.id

    # 5. Tạo Phiếu
    phieu = PhieuSuaChua(
        ma_phieu=ma_phieu,
        khach_hang_id=khach_hang.id,
        thiet_bi_id=thiet_bi.id,
        le_tan_id=le_tan_id,
        ktv_id=ktv_id,
        mo_ta_loi_khach=req.mo_ta_loi_khach.strip(),
        ghi_chu_ky_thuat=req.ghi_chu_ky_thuat.strip() if req.ghi_chu_ky_thuat else None,
        hinh_anh=req.hinh_anh,
        trang_thai="TiepNhan",
        tong_tien_du_kien=req.tong_tien_du_kien or 0.0,
        ngay_tiep_nhan=datetime.utcnow(),
        ngay_hen_tra=req.ngay_hen_tra
    )
    db.add(phieu)
    db.commit()
    db.refresh(phieu)

    return {
        "success": True,
        "message": f"Tiếp nhận thành công phiếu {ma_phieu}!",
        "phieu_id": phieu.id,
        "ma_phieu": phieu.ma_phieu
    }

@router.patch("/{phieu_id}/status")
def update_repair_status(
    phieu_id: int,
    req: UpdateRepairStatusRequest,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "KyThuatVien", "LeTan", "ThuNgan"]))
):
    """Cập nhật trạng thái phiếu sửa chữa theo vòng đời 8 bước."""
    phieu = db.query(PhieuSuaChua).filter(PhieuSuaChua.id == phieu_id).first()
    if not phieu:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu sửa chữa.")

    valid_statuses = [
        "TiepNhan", "PhanCongKTV", "DangKiemTra", "BaoGia_ChoDuyet", 
        "DangSuaChua", "DaSuaXong", "DaThanhToan", "HoanTat_TraMay"
    ]
    if req.trang_thai not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Trạng thái không hợp lệ. Phải là một trong: {valid_statuses}")

    phieu.trang_thai = req.trang_thai
    if req.ghi_chu_ky_thuat is not None:
        phieu.ghi_chu_ky_thuat = req.ghi_chu_ky_thuat
    if req.ktv_id is not None:
        phieu.ktv_id = req.ktv_id
    if req.tong_tien_du_kien is not None:
        phieu.tong_tien_du_kien = req.tong_tien_du_kien
    if req.trang_thai == "DaSuaXong":
        phieu.ngay_hoan_tat = datetime.utcnow()

    db.commit()
    db.refresh(phieu)
    return {
        "success": True,
        "message": f"Đã cập nhật trạng thái phiếu {phieu.ma_phieu} sang '{phieu.trang_thai}'!",
        "phieu_id": phieu.id,
        "ma_phieu": phieu.ma_phieu,
        "trang_thai": phieu.trang_thai
    }

@router.put("/{phieu_id}/assign-ktv")
def assign_ktv(
    phieu_id: int,
    req: AssignKTVRequest,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "LeTan"]))
):
    """Phân công Kỹ thuật viên phụ trách sửa chữa máy."""
    phieu = db.query(PhieuSuaChua).filter(PhieuSuaChua.id == phieu_id).first()
    if not phieu:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu sửa chữa.")

    ktv = db.query(NguoiDung).filter(NguoiDung.id == req.ktv_id, NguoiDung.vai_tro == "KyThuatVien").first()
    if not ktv:
        raise HTTPException(status_code=404, detail="Không tìm thấy Kỹ thuật viên này.")

    phieu.ktv_id = ktv.id
    if phieu.trang_thai == "TiepNhan":
        phieu.trang_thai = "PhanCongKTV"

    db.commit()
    db.refresh(phieu)
    return {
        "success": True,
        "message": f"Đã phân công phiếu {phieu.ma_phieu} cho KTV {ktv.ho_ten}!",
        "ktv_phu_trach": ktv.ho_ten
    }

# ================= CHI TIẾT SỬA CHỮA (ITEMS / PARTS / SERVICES) =================
@router.post("/{phieu_id}/items", response_model=RepairDetailOut, status_code=status.HTTP_201_CREATED)
def add_item_to_repair(
    phieu_id: int,
    req: RepairDetailCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "KyThuatVien"]))
):
    """Thêm linh kiện thay thế hoặc dịch vụ công vào phiếu sửa chữa và tự động tính tổng tiền."""
    phieu = db.query(PhieuSuaChua).filter(PhieuSuaChua.id == phieu_id).first()
    if not phieu:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu sửa chữa.")

    if not req.linh_kien_id and not req.dich_vu_id:
        raise HTTPException(status_code=400, detail="Cần chọn linh kiện hoặc dịch vụ sửa chữa.")

    don_gia = 0.0
    ten_muc = ""
    loai = ""

    if req.linh_kien_id:
        lk = db.query(LinhKien).filter(LinhKien.id == req.linh_kien_id).first()
        if not lk:
            raise HTTPException(status_code=404, detail="Linh kiện không tồn tại.")
        if lk.so_luong_ton < req.so_luong:
            raise HTTPException(status_code=400, detail=f"Linh kiện '{lk.ten_linh_kien}' trong kho chỉ còn {lk.so_luong_ton}, không đủ {req.so_luong}.")
        
        # Giảm số lượng tồn kho
        lk.so_luong_ton -= req.so_luong
        don_gia = req.don_gia if req.don_gia is not None else lk.gia_ban
        ten_muc = lk.ten_linh_kien
        loai = "LinhKien"

    elif req.dich_vu_id:
        dv = db.query(DichVu).filter(DichVu.id == req.dich_vu_id).first()
        if not dv:
            raise HTTPException(status_code=404, detail="Dịch vụ không tồn tại.")
        don_gia = req.don_gia if req.don_gia is not None else dv.gia_cong
        ten_muc = dv.ten_dich_vu
        loai = "DichVu"

    thanh_tien = don_gia * req.so_luong
    item = ChiTietSuaChua(
        phieu_sua_chua_id=phieu.id,
        linh_kien_id=req.linh_kien_id,
        dich_vu_id=req.dich_vu_id,
        so_luong=req.so_luong,
        don_gia=don_gia,
        thanh_tien=thanh_tien
    )
    db.add(item)
    db.flush()

    # Cập nhật tổng tiền dự kiến của phiếu sửa chữa
    total_cost = sum(ct.thanh_tien for ct in phieu.chi_tiet)
    phieu.tong_tien_du_kien = total_cost

    db.commit()
    db.refresh(item)

    return RepairDetailOut(
        id=item.id,
        phieu_sua_chua_id=item.phieu_sua_chua_id,
        linh_kien_id=item.linh_kien_id,
        dich_vu_id=item.dich_vu_id,
        ten_muc=ten_muc,
        loai=loai,
        so_luong=item.so_luong,
        don_gia=item.don_gia,
        thanh_tien=item.thanh_tien
    )

@router.delete("/{phieu_id}/items/{item_id}")
def remove_item_from_repair(
    phieu_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy", "KyThuatVien"]))
):
    """Xóa mục linh kiện/dịch vụ khỏi phiếu sửa và hoàn lại số lượng tồn kho."""
    item = db.query(ChiTietSuaChua).filter(ChiTietSuaChua.id == item_id, ChiTietSuaChua.phieu_sua_chua_id == phieu_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục chi tiết này.")

    # Hoàn kho nếu là linh kiện
    if item.linh_kien_id:
        lk = db.query(LinhKien).filter(LinhKien.id == item.linh_kien_id).first()
        if lk:
            lk.so_luong_ton += item.so_luong

    db.delete(item)
    db.flush()

    # Cập nhật lại tổng tiền
    phieu = db.query(PhieuSuaChua).filter(PhieuSuaChua.id == phieu_id).first()
    if phieu:
        phieu.tong_tien_du_kien = sum(ct.thanh_tien for ct in phieu.chi_tiet)

    db.commit()
    return {"success": True, "message": "Đã xóa mục chi tiết và hoàn lại tồn kho thành công."}

@router.delete("/{phieu_id}")
def delete_repair(
    phieu_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_roles(["QuanLy"]))
):
    """Xóa phiếu sửa chữa (Chỉ Quản Lý)."""
    phieu = db.query(PhieuSuaChua).filter(PhieuSuaChua.id == phieu_id).first()
    if not phieu:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu sửa chữa.")

    db.delete(phieu)
    db.commit()
    return {"success": True, "message": f"Đã xóa phiếu sửa chữa {phieu.ma_phieu} thành công."}
