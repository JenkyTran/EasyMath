import streamlit as st
import math
from prompt import get_response, get_solve

# Hàm tính tổ hợp và chỉnh hợp
def combination(n, k):
    return math.comb(n, k)

def permutation(n, k):
    return math.perm(n, k)

# Cấu hình trang
st.set_page_config(
    page_title="EasyMath",
    page_icon="📊",
    layout="wide"
)

# Sidebar: tiêu đề và lựa chọn tính năng
st.sidebar.markdown("<h2 style='text-align: center; color: #FF6347;'>EasyMath</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: center; color: #4682B4;'>Chọn tính năng</h4>", unsafe_allow_html=True)
st.sidebar.markdown("1. Mô tả bài toán hoán vị")
st.sidebar.markdown("2. Mô tả bài toán tổ hợp")
st.sidebar.markdown("3. Mô tả bài toán chỉnh hợp")
st.sidebar.markdown("4. Hướng dẫn giải bài toán")
st.sidebar.markdown("---")

# Khởi tạo trạng thái của tính năng
if "type_math" not in st.session_state:
    st.session_state.type_math = ""

# Sử dụng 3 nút lớn cho tính năng
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    if st.button("🎲 Hoán vị", key="hoan_vi"):
        st.session_state.type_math = "hv"
with col2:
    if st.button("🔢 Tổ hợp", key="to_hop"):
        st.session_state.type_math = "th"
with col3:
    if st.button("📐 Chỉnh hợp", key="chinh_hop"):
        st.session_state.type_math = "ch"

# Nút hướng dẫn được căn giữa
with st.sidebar:
    if st.button("❓ Hướng dẫn giải bài", key="huong_dan"):
        st.session_state.type_math = "solve"

# Phần chính: tiêu đề và giới thiệu hệ thống
st.markdown("<h1 style='text-align: center; color: #4682B4;'>Chào mừng đến với Easy Math!</h1>", unsafe_allow_html=True)

# Hiển thị giới thiệu hệ thống khi nhấn nút "Giới Thiệu"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Giới Thiệu"):
    st.info("""
        Easy Math là công cụ học toán trực tuyến với công nghệ AI, giúp giải thích các bài toán phức tạp (hoán vị, tổ hợp, chỉnh hợp) thành những mô tả dễ hiểu.
        Phát triển bởi nhóm học sinh với GenAI và Python, Easy Math giúp tiết kiệm thời gian và nâng cao hiệu quả học tập.
    """)

    member = {
        "name": "Đặng Minh Quân",
        "class": "7A18",
        "school": "THCS Nghĩa Tân Quận Cầu Giấy",
        "image": "image/DuongMinhQuan.jpg"
    }
    st.image(member["image"], width=400)
    st.markdown(f"### {member['name']}")
    st.markdown(f"**Lớp:** {member['class']}")
    st.markdown(f"**Trường:** {member['school']}")

st.write("---")

# Vùng tính toán: nhập số liệu và hiển thị đáp án
if st.session_state.type_math in ["hv", "th", "ch"]:
    # Nhập n
    n = st.number_input("Nhập số lượng phần tử (n):", min_value=1, step=1, value=5)
    k = None
    if st.session_state.type_math in ["th", "ch"]:
        k = st.number_input("Nhập số phần tử chọn (k):", min_value=1, max_value=n, step=1, value=2)

    # Hiển thị biểu thức và tính toán
    if st.session_state.type_math == "hv":
        st.markdown(f"**Tính hoán vị:** P({n}) = {n}!")
        answer = math.factorial(n)
    elif st.session_state.type_math == "th":
        st.markdown(f"**Tính tổ hợp:** C({n}, {k})")
        answer = combination(n, k)
    elif st.session_state.type_math == "ch":
        st.markdown(f"**Tính chỉnh hợp:** A({n}, {k})")
        answer = permutation(n, k)

    # Nút "Mô tả" giải thích bài toán
    if st.button("Mô tả", key="mota"):
        response = get_response(st.session_state.type_math, n, k)
        st.session_state.response = response
        st.markdown("### Mô tả bài toán")
        st.write(response)

    # Nút hiển thị đáp án (sau khi mô tả được sinh ra)
    if "response" in st.session_state and st.button("Đáp án", key="dap_an"):
        st.markdown("### Đáp án")
        st.write(st.session_state.response)
        st.write("**Kết quả:**", answer)

# Vùng nhập đề bài cho tính năng "Hướng dẫn giải bài"
if st.session_state.type_math == "solve":
    st.markdown("### Nhập đề bài cần giải")
    user_message = st.text_input("Nhập đề bài:", key="user_input", placeholder="Nhập nội dung tại đây...")
    if user_message:
        response = get_solve(user_message)
        st.session_state.response = response
        st.markdown("### Hướng dẫn giải bài")
        st.write(response)

# Sidebar hiển thị hướng dẫn cho từng tính năng
if st.session_state.type_math == "hv":
    st.sidebar.markdown("---")
    st.sidebar.markdown("# Bạn đã chọn: Hoán vị 🎲")
    st.sidebar.markdown("**Hoán vị** là cách sắp xếp các phần tử. Công thức:")
    st.sidebar.latex(r"P(n) = n!")
elif st.session_state.type_math == "th":
    st.sidebar.markdown("---")
    st.sidebar.markdown("# Bạn đã chọn: Tổ hợp 🔢")
    st.sidebar.markdown("**Tổ hợp** là cách chọn các phần tử mà không quan tâm đến thứ tự. Công thức:")
    st.sidebar.latex(r"C(n, k) = \binom{n}{k} = \frac{n!}{k!(n-k)!}")
elif st.session_state.type_math == "ch":
    st.sidebar.markdown("---")
    st.sidebar.markdown("# Bạn đã chọn: Chỉnh hợp 📐")
    st.sidebar.markdown("**Chỉnh hợp** là cách chọn các phần tử có quan tâm đến thứ tự. Công thức:")
    st.sidebar.latex(r"A(n, k) = \frac{n!}{(n-k)!}")
