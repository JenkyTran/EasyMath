import streamlit as st
import math
from prompt import get_response
from prompt import get_solve


# Hàm tính tổ hợp
def combination(n, k):
    return math.comb(n, k)

# Hàm tính chỉnh hợp
def permutation(n, k):
    return math.perm(n, k)

st.set_page_config(layout="wide")
st.sidebar.markdown("<h1 style='text-align: center; color: #FF6347;'></h1>", unsafe_allow_html=True)


st.sidebar.markdown("<h4 style='text-align: center; color: #4682B4;'>Chọn một tính năng:</h4>", unsafe_allow_html=True)
st.sidebar.markdown("1. Mô tả bài toán hoán vị")
st.sidebar.markdown("2. Mô tả bài toán tổ hợp")
st.sidebar.markdown("3. Mô tả bài toán chỉnh hợp")
st.sidebar.markdown("4. Hướng dẫn giải bài toán")
st.sidebar.markdown("")
st.sidebar.markdown("")
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

# Nút hướng dẫn được căn giữa
with st.sidebar:
    st.write("---")
    empty_col1, center_col, empty_col3 = st.columns([1, 2, 1])
    with center_col:
        if st.button("❓ Hướng dẫn giải bài", key="huong_dan"):
            st.session_state.type_math = "solve"


col_main, col_chat, col_pad = st.columns([1, 8, 1])

members = [
    {"name": "Huy", "class": "10A1", "school": "THCS", "image": "image/man-avatar-icon-free-vector.jpg"},
    {"name": "Quân", "class": "11B2", "school": "THCS", "image": "image/man-avatar-icon-free-vector.jpg"},
    {"name": "Khánh", "class": "12C3", "school": "THCS", "image": "image/man-avatar-icon-free-vector.jpg"},
]

with col_chat:
    st.markdown("<h1 style='text-align: center; color: #4682B4;'>Chào mừng đến với Easy Math!</h1>",
                unsafe_allow_html=True)
    # Nút giới thiệu hệ thống và thông điệp chào mừng
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    st.markdown("")
    if st.button(" Giới Thiệu"):
        st.write("""
            Easy Math là một công cụ học toán trực tuyến sử dụng công nghệ AI, giúp giải thích các công thức, bài toán phức tạp như hoán vị, tổ hợp và chỉnh hợp thành những mô tả dễ hiểu. Được phát triển bởi nhóm các bạn học sinh bằng công nghệ GenAI và ngôn ngữ lập trình Python, Easy Math giúp học sinh và giáo viên tiếp cận toán học một cách dễ dàng hơn, đồng thời tiết kiệm thời gian và nâng cao hiệu quả học tập. Truy cập Easy Math để trải nghiệm cách học toán mới mẻ, đơn giản và hiệu quả!
            """)
        # Tạo 3 cột
        col1, col2, col3 = st.columns(3)

        # Đặt mỗi thành viên vào một cột
        for col, member in zip([col1, col2, col3], members):
            with col:
                st.image(member["image"], use_column_width=True)
                st.write(f"### {member['name']}")
                st.write(f"**Lớp:** {member['class']}")
                st.write(f"**Trường:** {member['school']}")
    st.write("---")
    n = 1000
    if st.session_state.type_math == "hv" or st.session_state.type_math == "th" or st.session_state.type_math == "ch":
        n = st.number_input("Nhập số lượng phần tử (n)", min_value=1, step=1)
    if st.session_state.type_math == "hv":
        k = None
    elif st.session_state.type_math == "ch" or st.session_state.type_math == "th":
            k = st.number_input("Nhập số phần tử chọn (k)", min_value=1, max_value=n, step=1)

    answer = ""
    if st.session_state.type_math == "th":
        st.write(f"Tính C({n}, {k}) ") #{combination(n, k)}
        answer = combination(n, k)
    if st.session_state.type_math == "hv":
        st.write(f"Tính P({n}) ")
        answer = math.factorial(n)
    if st.session_state.type_math == "ch":
        st.write(f"Tính A({n}, {k})")
        answer = permutation(n, k)

    if st.session_state.type_math == "hv" or st.session_state.type_math == "th" or st.session_state.type_math == "ch":
        gen_des = st.button("Mô tả", key="mota")
        if gen_des:
            response = get_response(st.session_state.type_math, n, k)
            st.session_state.response = response  # Lưu response vào session_state
            st.write(response)

    # # Hiển thị nút "Đáp án" chỉ khi gen_des đã được nhấn
    if 'response' in st.session_state:
        key_ans = st.button("Đáp án")
        if key_ans:
            st.write(st.session_state.response)  # Hiển thị response đã lưu
            st.write("Đáp án: ", answer)  # Hiển thị đáp án
    if st.session_state.type_math == "solve":
        # Hộp nhập liệu cho người dùng
        user_message = st.text_input("Nhập đề bài: ", key="user_input", placeholder="Nhập nội dung tại đây...")
        if user_message:
            response = get_solve(user_message)
            st.session_state.response = response  # Lưu response vào session_state
            st.write(response)

# Hiển thị nội dung hướng dẫn trong sidebar dựa trên tính năng đã chọn
if st.session_state.type_math == "hv":
    st.sidebar.write("---")
    st.sidebar.write("# Bạn đã chọn tính năng Hoán vị 🎲")
    st.sidebar.markdown("### Hoán Vị")
    st.sidebar.markdown("- Hoán vị là cách sắp xếp các phần tử.")
    st.sidebar.markdown("Số hoán vị của n phần tử:")
    st.sidebar.latex(r'''
        P(n) = n!
    ''')
    result = math.factorial(n)
    # st.sidebar.write(f"Kết quả: Hoán vị của {n} phần tử là: {result}")
elif st.session_state.type_math == "th":
    st.sidebar.write("---")
    st.sidebar.write("# Bạn đã chọn tính năng Tổ hợp 🔢")
    st.sidebar.markdown("### Tổ Hợp")
    st.sidebar.markdown("- Tổ hợp là cách chọn các phần tử mà không quan tâm đến thứ tự.")
    st.sidebar.markdown("Tổ hợp của n phần tử chọn k phần tử:")
    st.sidebar.latex(r'''
        C(n, k) = \binom{n}{k} = \frac{n!}{k!(n-k)!}
    ''')
    result = combination(n, k)
    # st.sidebar.write(f"Kết quả: Tổ hợp của {n} phần tử chọn {k} là: {result}")
elif st.session_state.type_math == "ch":
    st.sidebar.write("---")
    st.sidebar.write("# Bạn đã chọn tính năng Chỉnh hợp 📐")
    st.sidebar.markdown("### Chỉnh Hợp")
    st.sidebar.markdown("- Chỉnh hợp là cách chọn các phần tử mà có quan tâm đến thứ tự.")
    st.sidebar.markdown("Chỉnh hợp của n phần tử chọn k phần tử:")
    st.sidebar.latex(r'''
        A(n, k) = \frac{n!}{(n-k)!}
    ''')
    result = permutation(n, k)
    # st.sidebar.write(f"Kết quả: Chỉnh hợp của {n} phần tử chọn {k} là: {result}")