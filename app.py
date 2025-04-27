import streamlit as st
import math
import json
from prompt import get_response, get_solve, get_quiz_questions, get_explanation_for_answer


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
st.sidebar.markdown("---")
st.sidebar.markdown("<h4 style='text-align: center; color: #4682B4;'>Chọn tính năng</h4>", unsafe_allow_html=True)
with st.sidebar:
    # 1. Mô tả bài toán hoán vị
    col_text, col_button = st.columns([1, 1])
    col_text.markdown("1. Mô tả bài toán hoán vị")
    if col_button.button("🎲 Hoán vị", key="hoan_vi"):
        st.session_state.type_math = "hv"

    # 2. Mô tả bài toán tổ hợp
    col_text, col_button = st.columns([1, 1])
    col_text.markdown("2. Mô tả bài toán tổ hợp")
    if col_button.button("🔢 Tổ hợp", key="to_hop"):
        st.session_state.type_math = "th"

    # 3. Mô tả bài toán chỉnh hợp
    col_text, col_button = st.columns([1, 1])
    col_text.markdown("3. Mô tả bài toán chỉnh hợp")
    if col_button.button("📐 Chỉnh hợp", key="chinh_hop"):
        st.session_state.type_math = "ch"

    # 4. Hướng dẫn giải bài toán
    col_text, col_button = st.columns([1, 1])
    col_text.markdown("4. Hướng dẫn giải bài toán")
    if col_button.button("❓ Hướng dẫn giải bài", key="huong_dan"):
        st.session_state.type_math = "solve"

    # 5. Bài kiểm tra
    col_text, col_button = st.columns([1, 1])
    col_text.markdown("5. Bài kiểm tra")
    if col_button.button("📝 Tạo bài kiểm tra", key="quiz"):
        st.session_state.type_math = "quiz"
        # Reset quiz data when switching to quiz mode from another mode
        if "quiz_questions" in st.session_state:
            del st.session_state.quiz_questions
        if "user_answers" in st.session_state:
            del st.session_state.user_answers
        if "quiz_submitted" in st.session_state:
            del st.session_state.quiz_submitted
        if "quiz_score" in st.session_state:
            del st.session_state.quiz_score
        if "question_explanations" in st.session_state:
            del st.session_state.question_explanations

# Khởi tạo trạng thái của tính năng
if "type_math" not in st.session_state:
    st.session_state.type_math = ""

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
        "name": "Đặng Minh Quân và Nguyễn Nam Khánh",
        "image": "image/team.png"
    }
    cols = st.columns([1, 5, 1])
    with cols[1]:
        st.markdown(f"Tác giả")
        st.image(member["image"], width=600)
        st.markdown(f"### {member['name']}")

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
elif st.session_state.type_math == "solve":
    st.sidebar.markdown("---")
    st.sidebar.markdown("# Bạn đã chọn: Hướng dẫn giải bài ❓")
    st.sidebar.markdown("""
    **Hướng dẫn giải bài** giúp bạn giải các bài toán hoán vị, tổ hợp, chỉnh hợp.

    Nhập đề bài vào ô và nhận hướng dẫn giải chi tiết từ AI.
    """)
elif st.session_state.type_math == "quiz":
    st.sidebar.markdown("---")
    st.sidebar.markdown("# Bạn đã chọn: Bài kiểm tra 📝")
    st.sidebar.markdown("""
    **Bài kiểm tra** giúp bạn kiểm tra kiến thức về:
    - Hoán vị (P)
    - Tổ hợp (C)
    - Chỉnh hợp (A)

    Chọn loại bài kiểm tra, trả lời các câu hỏi và nhận điểm số cùng giải thích chi tiết.
    """)

if st.session_state.type_math == "quiz":
    st.markdown("### Bài kiểm tra")

    # Khởi tạo các session state cho quiz
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = None
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "question_explanations" not in st.session_state:
        st.session_state.question_explanations = {}

    # Chọn loại bài kiểm tra
    if not st.session_state.quiz_questions:
        col1, col2 = st.columns(2)
        with col1:
            quiz_type = st.selectbox(
                "Chọn loại bài kiểm tra:",
                options=[
                    ("Hoán vị", "hv"),
                    ("Tổ hợp", "th"),
                    ("Chỉnh hợp", "ch"),
                    ("Hỗn hợp", "mix")
                ],
                format_func=lambda x: x[0],
                index=0
            )[1]

        with col2:
            num_questions = st.slider("Số lượng câu hỏi:", min_value=5, max_value=15, value=10, step=1)

        # Nút tạo bài kiểm tra
        if st.button("Tạo bài kiểm tra"):
            with st.spinner("Đang tạo bài kiểm tra..."):
                try:
                    # Reset tất cả dữ liệu bài kiểm tra trước khi tạo mới
                    st.session_state.quiz_questions = None
                    st.session_state.user_answers = {}
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_score = 0
                    st.session_state.question_explanations = {}

                    # Tạo bài kiểm tra mới
                    st.session_state.quiz_questions = get_quiz_questions(quiz_type, num_questions)
                    st.success(f"Đã tạo bài kiểm tra với {len(st.session_state.quiz_questions)} câu hỏi!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Có lỗi xảy ra khi tạo bài kiểm tra: {str(e)}")

    # Hiển thị bài kiểm tra
    if st.session_state.quiz_questions and not st.session_state.quiz_submitted:
        st.write("### Trả lời các câu hỏi sau:")

        for i, q in enumerate(st.session_state.quiz_questions):
            st.write(f"**Câu {i + 1}:** {q['question']}")

            # Input đáp án
            answer_key = f"answer_{i}"
            user_answer = st.text_input(
                "Đáp án của bạn:",
                key=answer_key,
                value=st.session_state.user_answers.get(i, "")
            )

            # Lưu đáp án người dùng
            st.session_state.user_answers[i] = user_answer

            st.write("---")

        # Nút nộp bài
        if st.button("Nộp bài"):
            st.session_state.quiz_submitted = True

            # Tính điểm
            correct_count = 0
            for i, q in enumerate(st.session_state.quiz_questions):
                user_answer = st.session_state.user_answers.get(i, "").strip()
                correct_answer = str(q['answer']).strip()

                if user_answer == correct_answer:
                    correct_count += 1

            st.session_state.quiz_score = correct_count
            st.rerun()

    # Hiển thị kết quả sau khi nộp bài
    if st.session_state.quiz_questions and st.session_state.quiz_submitted:
        st.write(f"### Kết quả: {st.session_state.quiz_score}/{len(st.session_state.quiz_questions)} câu đúng")

        for i, q in enumerate(st.session_state.quiz_questions):
            user_answer = st.session_state.user_answers.get(i, "").strip()
            correct_answer = str(q['answer']).strip()

            # Xác định trạng thái đúng/sai
            is_correct = user_answer == correct_answer
            status_color = "green" if is_correct else "red"
            status_icon = "✓" if is_correct else "✗"

            st.write(f"**Câu {i + 1}:** {q['question']}")
            st.write(f"- Đáp án của bạn: **{user_answer}**")
            st.write(f"- Đáp án đúng: **{correct_answer}**")
            st.markdown(f"- Kết quả: <span style='color:{status_color}'>{status_icon}</span>", unsafe_allow_html=True)

            # Nút giải thích
            explanation_key = f"explain_{i}"
            if explanation_key not in st.session_state.question_explanations:
                if st.button(f"Xem giải thích", key=f"btn_explain_{i}"):
                    with st.spinner("Đang lấy giải thích..."):
                        explanation = get_explanation_for_answer(
                            q['question'],
                            user_answer,
                            correct_answer
                        )
                        st.session_state.question_explanations[explanation_key] = explanation
                        st.rerun()

            # Hiển thị giải thích nếu có
            if explanation_key in st.session_state.question_explanations:
                with st.expander("Xem giải thích", expanded=True):
                    st.write(st.session_state.question_explanations[explanation_key])

            st.write("---")

        # Nút làm bài kiểm tra mới
        if st.button("Làm bài kiểm tra mới"):
            # Reset tất cả dữ liệu bài kiểm tra khi làm bài mới
            st.session_state.quiz_questions = None
            st.session_state.user_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.session_state.question_explanations = {}
            st.rerun()