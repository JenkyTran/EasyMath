import os
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

# Optional: Uncomment to test
# print(get_response('th', 3, 2))