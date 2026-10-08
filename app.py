import streamlit as st
from datetime import datetime
import math


# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Ứng dụng tính lãi tiết kiệm",
    page_icon="🏦",
    layout="wide"
)


# ============================================================
# CSS GIAO DIỆN
# ============================================================

st.markdown("""
<style>

    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        background-color: #f8f9fa;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .receipt {
        border: 2px dashed #555;
        border-radius: 12px;
        padding: 25px;
        background-color: white;
        margin-top: 20px;
    }

    .receipt-title {
        text-align: center;
        font-size: 27px;
        font-weight: bold;
    }

    .receipt-center {
        text-align: center;
    }

    .money {
        font-size: 24px;
        font-weight: bold;
    }

    .success-text {
        color: green;
        font-weight: bold;
        font-size: 20px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.markdown(
    '<div class="main-title">🏦 ỨNG DỤNG TÍNH LÃI TIẾT KIỆM NGÂN HÀNG</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Tính tiền lãi cuối kỳ - Lãi đơn và lãi kép</div>',
    unsafe_allow_html=True
)


# ============================================================
# DỮ LIỆU LÃI SUẤT THAM KHẢO
# Đơn vị: %/năm
# ============================================================

lai_suat = {

    "SHB": {
        1: 4.75,
        3: 4.75,
        6: 7.70,
        9: 7.70,
        12: 7.80,
        18: 6.60,
        24: 6.70,
        36: 6.70
    },

    "BIDV": {
        1: 4.80,
        3: 4.80,
        6: 7.20,
        9: 7.20,
        12: 7.40,
        18: 6.60,
        24: 6.80,
        36: 6.80
    },

    "LPBank": {
        1: 4.40,
        3: 4.65,
        6: 7.00,
        9: 7.10,
        12: 7.20,
        18: 7.15,
        24: 7.20,
        36: 6.10
    },

    "Bắc Á Bank": {
        1: 4.75,
        3: 4.75,
        6: 7.05,
        9: 7.10,
        12: 7.10,
        18: 7.10,
        24: 7.10,
        36: 7.10
    },

    "OCB": {
        1: 4.75,
        3: 4.75,
        6: 6.70,
        9: 6.70,
        12: 7.00,
        18: 6.60,
        24: 6.80,
        36: 7.00
    },

    "VIB": {
        1: 4.40,
        3: 4.50,
        6: 5.70,
        9: 5.90,
        12: 7.00,
        18: 5.90,
        24: 6.00,
        36: 6.00
    },

    "Sacombank": {
        1: 4.80,
        3: 4.75,
        6: 6.80,
        9: 6.90,
        12: 7.00,
        18: 6.90,
        24: 6.90,
        36: 6.90
    },

    "PGBank": {
        1: 4.75,
        3: 4.75,
        6: 6.90,
        9: 6.90,
        12: 7.00,
        18: 6.80,
        24: 6.80,
        36: 6.80
    }
}


# ============================================================
# HÀM ĐỊNH DẠNG TIỀN
# ============================================================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ".replace(",", ".")


# ============================================================
# KHỞI TẠO SESSION STATE
# ============================================================

if "da_gui" not in st.session_state:
    st.session_state.da_gui = False

if "bien_lai" not in st.session_state:
    st.session_state.bien_lai = ""


# ============================================================
# NHẬP THÔNG TIN
# ============================================================

st.markdown("## 👤 Thông tin khách hàng")

col1, col2 = st.columns(2)

with col1:
    ho_ten = st.text_input(
        "Họ và tên khách hàng",
        placeholder="Ví dụ: Nguyễn Văn An"
    )

with col2:
    so_tien = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=100000.0,
        value=10000000.0,
        step=100000.0,
        format="%.0f"
    )


# ============================================================
# THÔNG TIN SỔ TIẾT KIỆM
# ============================================================

st.markdown("## 💰 Thông tin gửi tiết kiệm")

col1, col2, col3 = st.columns(3)

with col1:

    ngan_hang = st.selectbox(
        "🏦 Chọn ngân hàng",
        list(lai_suat.keys())
    )

with col2:

    ky_han = st.selectbox(
        "📅 Chọn kỳ hạn gửi",
        [1, 3, 6, 9, 12, 18, 24, 36],
        format_func=lambda x: f"{x} tháng"
    )

with col3:

    loai_lai = st.radio(
        "📈 Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ],
        horizontal=False
    )


# ============================================================
# LẤY LÃI SUẤT
# ============================================================

lai_suat_nam = lai_suat[ngan_hang][ky_han]

st.info(
    f"💡 Lãi suất tham khảo: **{lai_suat_nam:.2f}%/năm** "
    f"cho {ngan_hang}, kỳ hạn {ky_han} tháng."
)


# ============================================================
# CHO PHÉP NGƯỜI DÙNG ĐIỀU CHỈNH LÃI SUẤT
# ============================================================

st.markdown("### ⚙️ Lãi suất áp dụng")

dung_lai_suat_tham_khao = st.checkbox(
    "Sử dụng lãi suất tham khảo tự động",
    value=True
)

if dung_lai_suat_tham_khao:

    lai_suat_ap_dung = lai_suat_nam

else:

    lai_suat_ap_dung = st.number_input(
        "Nhập lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=float(lai_suat_nam),
        step=0.1
    )


# ============================================================
# TÍNH TOÁN
# ============================================================

so_nam = ky_han / 12

if loai_lai == "Lãi đơn":

    # Công thức:
    # Tiền lãi = Tiền gốc × lãi suất × thời gian

    tien_lai = (
        so_tien
        * (lai_suat_ap_dung / 100)
        * so_nam
    )

    tong_tien = so_tien + tien_lai

    cong_thuc = (
        "Tiền lãi = Tiền gốc × Lãi suất × Thời gian"
    )

else:

    # Lãi kép:
    # Lãi nhập gốc hàng tháng
    #
    # FV = P × (1 + r/12)^n

    so_ky = ky_han

    tong_tien = (
        so_tien
        * (
            1 + lai_suat_ap_dung / 100 / 12
        ) ** so_ky
    )

    tien_lai = tong_tien - so_tien

    cong_thuc = (
        "Tổng tiền = Tiền gốc × (1 + Lãi suất/12)^Số tháng"
    )


# ============================================================
# NÚT TÍNH LÃI
# ============================================================

st.markdown("---")

if st.button(
    "🧮 TÍNH TIỀN LÃI",
    use_container_width=True
):

    if ho_ten.strip() == "":
        st.error("❌ Vui lòng nhập họ tên khách hàng.")

    elif so_tien <= 0:
        st.error("❌ Số tiền gửi phải lớn hơn 0.")

    else:

        st.session_state.da_gui = False

        st.success("✅ Đã tính toán thành công!")


        # ====================================================
        # HIỂN THỊ KẾT QUẢ
        # ====================================================

        st.markdown("## 📊 Kết quả tính toán")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💰 Tiền gốc",
                dinh_dang_tien(so_tien)
            )

        with col2:
            st.metric(
                "📈 Tiền lãi",
                dinh_dang_tien(tien_lai)
            )

        with col3:
            st.metric(
                "💵 Tổng nhận cuối kỳ",
                dinh_dang_tien(tong_tien)
            )


        # ====================================================
        # CHI TIẾT
        # ====================================================

        st.markdown("### 📋 Chi tiết khoản tiền gửi")

        st.write(f"**Họ tên:** {ho_ten}")
        st.write(f"**Ngân hàng:** {ngan_hang}")
        st.write(f"**Số tiền gửi:** {dinh_dang_tien(so_tien)}")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")
        st.write(f"**Lãi suất:** {lai_suat_ap_dung:.2f}%/năm")
        st.write(f"**Hình thức:** {loai_lai}")
        st.write(f"**Tiền lãi:** {dinh_dang_tien(tien_lai)}")
        st.write(f"**Tổng tiền cuối kỳ:** {dinh_dang_tien(tong_tien)}")

        st.info(f"📌 Công thức: {cong_thuc}")


# ============================================================
# NÚT GỬI TIẾT KIỆM
# ============================================================

st.markdown("---")

st.markdown("## 🏦 Thực hiện gửi tiết kiệm")

if st.button(
    "💳 GỬI TIẾT KIỆM",
    type="primary",
    use_container_width=True
):

    if ho_ten.strip() == "":
        st.error("❌ Vui lòng nhập họ tên khách hàng.")

    elif so_tien <= 0:
        st.error("❌ Số tiền gửi phải lớn hơn 0.")

    else:

        st.session_state.da_gui = True

        # ----------------------------------------------------
        # MÃ GIAO DỊCH
        # ----------------------------------------------------

        ma_giao_dich = (
            "TK"
            + datetime.now().strftime("%Y%m%d%H%M%S")
        )

        ngay_gio = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        # ----------------------------------------------------
        # TẠO NỘI DUNG BIÊN LAI
        # ----------------------------------------------------

        bien_lai = f"""
========================================================
              NGÂN HÀNG ĐIỆN TỬ
                BIÊN LAI GỬI TIẾT KIỆM
========================================================

Mã giao dịch       : {ma_giao_dich}
Ngày giao dịch     : {ngay_gio}

--------------------------------------------------------
THÔNG TIN KHÁCH HÀNG
--------------------------------------------------------

Họ và tên          : {ho_ten}
Ngân hàng          : {ngan_hang}

--------------------------------------------------------
THÔNG TIN TIỀN GỬI
--------------------------------------------------------

Số tiền gửi        : {dinh_dang_tien(so_tien)}
Kỳ hạn             : {ky_han} tháng
Lãi suất           : {lai_suat_ap_dung:.2f}%/năm
Hình thức tính lãi : {loai_lai}

--------------------------------------------------------
KẾT QUẢ
--------------------------------------------------------

Tiền gốc           : {dinh_dang_tien(so_tien)}
Tiền lãi           : {dinh_dang_tien(tien_lai)}
Tổng tiền cuối kỳ  : {dinh_dang_tien(tong_tien)}

--------------------------------------------------------

Trạng thái         : GỬI TIẾT KIỆM THÀNH CÔNG

Lưu ý:
- Lãi suất trên ứng dụng mang tính tham khảo.
- Lãi suất thực tế phụ thuộc biểu lãi suất của ngân hàng.
- Đây là biên lai mô phỏng phục vụ mục đích học tập/demo.

========================================================
             CẢM ƠN QUÝ KHÁCH ĐÃ SỬ DỤNG
========================================================
"""

        st.session_state.bien_lai = bien_lai


# ============================================================
# HIỂN THỊ BIÊN LAI
# ============================================================

if st.session_state.da_gui:

    st.markdown("---")

    st.markdown(
        '<div class="receipt">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="receipt-title">🏦 BIÊN LAI GỬI TIẾT KIỆM</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="receipt-center">Giao dịch thành công</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.write(f"**👤 Khách hàng:** {ho_ten}")
        st.write(f"**🏦 Ngân hàng:** {ngan_hang}")
        st.write(f"**💳 Số tiền gửi:** {dinh_dang_tien(so_tien)}")
        st.write(f"**📅 Kỳ hạn:** {ky_han} tháng")

    with col2:

        st.write(
            f"**📈 Lãi suất:** {lai_suat_ap_dung:.2f}%/năm"
        )

        st.write(
            f"**💰 Hình thức:** {loai_lai}"
        )

        st.write(
            f"**💵 Tiền lãi:** {dinh_dang_tien(tien_lai)}"
        )

        st.write(
            f"**💎 Tổng nhận:** {dinh_dang_tien(tong_tien)}"
        )

    st.markdown("---")

    st.success(
        f"✅ Gửi tiết kiệm thành công! "
        f"Tổng số tiền nhận cuối kỳ: {dinh_dang_tien(tong_tien)}"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # TẢI BIÊN LAI
    # ========================================================

    st.download_button(
        label="📥 TẢI BIÊN LAI",
        data=st.session_state.bien_lai,
        file_name="bien_lai_gui_tiet_kiem.txt",
        mime="text/plain",
        use_container_width=True
    )


# ============================================================
# THÔNG TIN CUỐI TRANG
# ============================================================

st.markdown("---")

st.caption(
    "📌 Ứng dụng mô phỏng tính lãi tiền gửi tiết kiệm phục vụ mục đích học tập. "
    "Lãi suất cần được đối chiếu với biểu lãi suất chính thức của ngân hàng "
    "trước khi thực hiện giao dịch thực tế."
)
