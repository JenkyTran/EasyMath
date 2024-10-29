import streamlit as st
import math
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt import get_response

# Hàm tính tổ hợp
def combination(n, k):
    return math.comb(n, k)

# Hàm tính chỉnh hợp
def permutation(n, k):
    return math.perm(n, k)

st.set_page_config(layout="wide")
st.sidebar.markdown("<h1 style='text-align: center; color: #FF6347;'>Tính Toán Vui!</h1>", unsafe_allow_html=True)


st.sidebar.markdown("<h4 style='text-align: center; color: #4682B4;'>Chọn một tính năng:</h4>", unsafe_allow_html=True)

# Lưu trạng thái của tính năng đã chọn vào session_state
if "type_math" not in st.session_state:
    st.session_state.type_math = ""

# Sử dụng các button lớn hơn cho các tính năng
col1, col2, col3 = st.sidebar.columns([1, 1, 1])
with col1:
    if st.button("🎲 Hoán vị", key="hoan_vi"):
        st.session_state.type_math = "hv"
with col2:
    if st.button("🔢 Tổ hợp", key="to_hop"):
        st.session_state.type_math = "th"
with col3:
    if st.button("📐 Chỉnh hợp", key="chinh_hop"):
        st.session_state.type_math = "ch"

# Giao diện chính với hai cột
col_main, col_chat, col_pad = st.columns([1, 5, 1])

# Nội dung cột bên phải (nơi hiển thị chat và giới thiệu hệ thống)
with col_chat:
    st.markdown("<h1 style='text-align: center; color: #4682B4;'>Chào mừng đến với Hệ Thống Tính Toán!</h1>",
                unsafe_allow_html=True)
    # Nút giới thiệu hệ thống và thông điệp chào mừng
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.button("📢 Giới Thiệu Hệ Thống"):
        st.write(
            "Chào các bạn! Đây là hệ thống giúp bạn tính toán hoán vị, tổ hợp và chỉnh hợp một cách dễ dàng và vui nhộn.")

    # Nhập số lượng phần tử
    n = st.number_input("Nhập số lượng phần tử (n)", min_value=1, step=1)
    if st.session_state.type_math != "hv":
        # Nhập số phần tử chọn
        k = st.number_input("Nhập số phần tử chọn (k)", min_value=1, max_value=n, step=1)
    else:
        k = None
    if st.session_state.type_math == "th":
        st.write(f"Tính C({n}, {k}) ") #{combination(n, k)}
    if st.session_state.type_math == "hv":
        st.write(f"Tính P({n}) ")
    if st.session_state.type_math == "ch":
        st.write(f"Tính A({n}, {k})")

    # Nút mô tả để lấy kết quả mô tả từ hệ thống ChatGoogleGenerativeAI
    gen_des = st.button("Mô tả", key="mota")
    if gen_des:
        response = get_response(st.session_state.type_math, n, k)
        st.write(response)

# Hiển thị nội dung hướng dẫn trong sidebar dựa trên tính năng đã chọn
if st.session_state.type_math == "hv":
    st.sidebar.write("# Bạn đã chọn tính năng Hoán vị 🎲")
    st.sidebar.markdown("### Hoán Vị")
    st.sidebar.markdown("- Hoán vị là cách sắp xếp các phần tử.")
    st.sidebar.markdown("Số hoán vị của n phần tử:")
    st.sidebar.latex(r'''
        P(n) = n!
    ''')
    result = math.factorial(n)
    st.sidebar.write(f"Kết quả: Hoán vị của {n} phần tử là: {result}")
elif st.session_state.type_math == "th":
    st.sidebar.write("# Bạn đã chọn tính năng Tổ hợp 🔢")
    st.sidebar.markdown("### Tổ Hợp")
    st.sidebar.markdown("- Tổ hợp là cách chọn các phần tử mà không quan tâm đến thứ tự.")
    st.sidebar.markdown("Tổ hợp của n phần tử chọn k phần tử:")
    st.sidebar.latex(r'''
        C(n, k) = \binom{n}{k} = \frac{n!}{k!(n-k)!}
    ''')
    result = combination(n, k)
    st.sidebar.write(f"Kết quả: Tổ hợp của {n} phần tử chọn {k} là: {result}")
elif st.session_state.type_math == "ch":
    st.sidebar.write("# Bạn đã chọn tính năng Chỉnh hợp 📐")
    st.sidebar.markdown("### Chỉnh Hợp")
    st.sidebar.markdown("- Chỉnh hợp là cách chọn các phần tử mà có quan tâm đến thứ tự.")
    st.sidebar.markdown("Chỉnh hợp của n phần tử chọn k phần tử:")
    st.sidebar.latex(r'''
        A(n, k) = \frac{n!}{(n-k)!}
    ''')
    result = permutation(n, k)
    st.sidebar.write(f"Kết quả: Chỉnh hợp của {n} phần tử chọn {k} là: {result}")