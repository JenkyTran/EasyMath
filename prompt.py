import os
import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',
    google_api_key="AIzaSyDUlZ7Ix0t7w3cjaVs48qwPM1QC69blmj8",
    temperature=0.9
)

def create_prompt(context):
    return prompt_template.format(context=context)


def create_prompt_solve(context):
    return prompt_template_solve.format(context=context)


prompt_template = """
    Bạn là một chuyên gia trong lĩnh vực hoán vị, tổ hợp, chỉnh hợp và bạn biết các kiến thức sau:
    -Hoán vị là cách sắp xếp các phần tử.
    -Tổ hợp là cách chọn các phần tử mà không quan tâm đến thứ tự.
    -Chỉnh hợp là cách chọn các phần tử mà có quan tâm đến thứ tự.
    ###
    Hãy mô tả một bài toán {context} bằng một câu chuyện sinh động và gần gũi với đời sống.
    Tham khảo và làm theo các ví dụ bên dưới.
    Chú ý chỉ mô tả chứ không giải ra đáp án. Mô tả ngắn gọn trong 1-3 câu.
    Trong câu chuyện cần kết lại để yêu cầu người đọc tính đáp án của bài toán (In ra theo cấu trúc:"Hãy tính X để tìm đáp án."; với X là: A(n, k) với bài toán chỉnh hợp, C(n, k) với bài tóan tổ hợp, P(n) với bài toán hoán vị) 
    ###
    Tham khảo ví dụ sau:
    1/Yêu cầu: Tính A(3, 2)
    Mô tả: 
    - Có bao nhiêu cách sắp xếp 3 bạn Khánh, Quân, Hùng vào 2 chỗ ngồi cho trước theo thứ tự. Hãy tính A(3, 2) để tìm đáp án
    2/Yêu cầu: Tính C(5,3)
    Mô tả: Một tổ có 5 bạn học sinh. Có bao nhiêu cách để chọn ra 3 bạn học sinh đi trực nhật
    """

prompt_template_solve = """
    Bạn là một chuyên gia trong lĩnh vực hoán vị, tổ hợp, chỉnh hợp và bạn biết các kiến thức sau:
    -Hoán vị là cách sắp xếp các phần tử.
    -Tổ hợp là cách chọn các phần tử mà không quan tâm đến thứ tự.
    -Chỉnh hợp là cách chọn các phần tử mà có quan tâm đến thứ tự.
    ####
    Đề bài: {context}
    ####
    Bạn hãy đưa ra hướng dẫn giải bài toán ở trên theo mẫu yêu cầu sau:
    1/ Xác định đây là bài toán hoán vị hay tổ hợp hay chỉnh hợp trong 1 câu.
    2/ Hướng dẫn các bước để giải bài toán (lưu ý không đưa đáp án cụ thể, không sử dụng công thức ở dạng latex, dùng ở dạng A(n, k); P(n); C(n, k)). Nếu có thể thì hướng dẫn giải bằng nhiều cách.
    ####
    Mẫu câu hỏi và câu trả lời tham khảo:
    a) Sắp xếp năm bạn học sinh An, Bình, Chi, Dũng, Lệ vào một chiếc ghế dài có 5 chỗ ngồi. Số cách sắp xếp sao cho bạn Chi luôn ngồi chính giữa là
    Giải: 
    1/ Đây là bài toán hoán vị 
    2/ Xếp bạn Chi ngồi giữa có 1 cách. Số cách xếp 4 bạn sinh An, Bình, Dũng, Lệ vào 4 chỗ còn lại là một hoán vị của 4 phần tử
    b) Có bao nhiêu cách xếp khác nhau cho 4 người ngồi vào 6 chỗ trên một bàn dài?
    Giải: 
    1/ Đây là bài toán chỉnh hợp 
    2/ Số cách xếp khác nhau cho 4 người ngồi vào 6 chỗ là một bài toán có quan tâm đến thứ tự (vị trí) nên đáp án sẽ là chỉnh hợp chập 4 của 6 phần tử
    c) Một lớp học có 40 học sinh gồm 25 nam và 15 nữ. Chọn 3 học sinh để tham gia vệ sinh công cộng toàn trường, hỏi có bao nhiêu cách chọn như trên?
    Giải: 
    1/ Đây là bài toán tổ hợp 
    2/ Nhóm học sinh 3 người được chọn (không phân biệt nam, nữ - công việc) là một tổ hợp chập 3 của 40 (học sinh).
    """


def get_response(type_math, n, k):
    if llm is None:
        raise ValueError("LLM not initialized. Check your API key and connection.")

    if type_math == 'th':
        context = f'tổ hợp C({n}, {k})'
    elif type_math == 'ch':
        context = f'chỉnh hợp P({n}, {k})'
    elif type_math == 'hv':
        context = f'hoán vị P({n})'
    else:
        raise ValueError("Invalid math type. Use 'th', 'ch', or 'hv'.")

    prompt = create_prompt(context)
    response = llm.invoke(prompt).content
    return response


def get_solve(context):
    if llm is None:
        raise ValueError("LLM not initialized. Check your API key and connection.")

    prompt = create_prompt_solve(context)
    response = llm.invoke(prompt).content
    return response


def create_prompt_quiz(quiz_type, num_questions=10):
    # Ánh xạ mã quiz sang mô tả dạng bài
    type_mapping = {
        "hv": "Hoán vị",
        "th": "Tổ hợp",
        "ch": "Chỉnh hợp",
        "mix": "Hỗn hợp"
    }

    if quiz_type not in type_mapping:
        raise ValueError("Invalid quiz_type. Expected one of: hv, th, ch, mix.")

    math_type = type_mapping[quiz_type]

    # Xác định mô tả bài toán dựa theo mã quiz
    if quiz_type == "hv":
        problem_description = "chỉ tạo bài toán hoán vị"
    elif quiz_type == "th":
        problem_description = "chỉ tạo bài toán tổ hợp"
    elif quiz_type == "ch":
        problem_description = "chỉ tạo bài toán chỉnh hợp"
    else:  # mix
        problem_description = "tạo bài toán hỗn hợp, phân bổ đều giữa hoán vị, tổ hợp và chỉnh hợp"

    prompt = f"""
    Bạn là một chuyên gia toán học, chuyên về hoán vị, tổ hợp và chỉnh hợp.
    Hãy tạo {num_questions} bài toán theo yêu cầu sau:
    - Nếu yêu cầu là "{math_type}" (code: {quiz_type}), {problem_description}.
    
    Các bài toán cần đáp ứng:
    1. Đề bài rõ ràng, sinh động và liên quan đến đời sống hàng ngày.
    2. Yêu cầu học sinh tính toán theo công thức phù hợp: P(n) cho bài toán hoán vị, C(n, k) cho bài toán tổ hợp, hoặc A(n, k) cho bài toán chỉnh hợp.
    3. Có đáp án chính xác (kết quả là số).
    
    Trả về kết quả duy nhất dưới dạng JSON với cấu trúc sau (không có thêm bất kỳ text nào khác):
    ```json
    [
      {{
        "question": "Đề bài toán 1",
        "answer": "Đáp án chính xác (số)",
        "explanation": "Giải thích ngắn gọn về cách giải, công thức được áp dụng và lý do vì sao",
        "type": "{math_type}"
      }},
      ...
    ]
    Chỉ trả về JSON, không có text khác.
    """
    return prompt


def get_quiz_questions(quiz_type, num_questions=10):
    """
    Tạo các câu hỏi bài kiểm tra dựa trên loại được chọn

    quiz_type: "hv" (Hoán vị), "th" (Tổ hợp), "ch" (Chỉnh hợp), hoặc "mix" (Hỗn hợp)
    """
    if llm is None:
        raise ValueError("LLM not initialized. Check your API key and connection.")

    prompt = create_prompt_quiz(quiz_type, num_questions)
    response = llm.invoke(prompt).content

    json_match = re.search(r'\[.*\]', response, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse JSON response from AI")
    else:
        raise ValueError("AI response does not contain JSON format")


def get_explanation_for_answer(question, user_answer, correct_answer):
    """
    Lấy giải thích chi tiết cho câu trả lời của người dùng
    """
    if llm is None:
        raise ValueError("LLM not initialized. Check your API key and connection.")

    prompt = f"""
    Bạn là một giáo viên toán chuyên về xác suất thống kê, hoán vị, tổ hợp, chỉnh hợp.

    Bài toán: {question}

    Đáp án của học sinh: {user_answer}
    Đáp án đúng: {correct_answer}

    Hãy giải thích chi tiết cách giải bài toán từng bước một:
    1. Xác định đây là bài toán gì (hoán vị, tổ hợp hay chỉnh hợp)
    2. Phân tích yêu cầu bài toán
    3. Áp dụng công thức phù hợp
    4. Tính toán để có kết quả

    Nếu học sinh trả lời sai, hãy chỉ ra lỗi sai và cách sửa.
    Giải thích ngắn gọn, dễ hiểu, phù hợp với học sinh cấp 2, cấp 3. Đưa ra giải thích ngắn gọn trong 5-10 câu. Chú ý trả về các biểu thức, công thức toán phù hợp để hiển thị trong streamlit
    """
    response = llm.invoke(prompt).content
    return response


# Optional: Uncomment to test
# print(get_response('th', 3, 2))