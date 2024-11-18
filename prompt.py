import os
from langchain_google_genai import ChatGoogleGenerativeAI

if 'GOOGLE_API_KEY' not in os.environ:
    os.environ['GOOGLE_API_KEY'] = "AIzaSyC6A1MJR-kk-KetpF3Llqna_GE4hulhwMU"

llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0.9)

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
    Trong câu chuyện cần kết lại để yêu cầu người đọc tính đáp án của bài toán.
    ###
    Tham khảo ví dụ sau:
    1/Yêu cầu: Tính A(3, 2)
    Mô tả: 
    - Có bao nhiêu cách sắp xếp 3 bạn Khánh, Quân, Hùng vào 2 chỗ ngồi cho trước.
    - Bạn Lan có 3 chiếc áo sơ mi màu trắng, xanh và vàng. Có bao nhiêu cách để bạn Lan chọn ra 2 chiếc áo sơ mi.
    - Bạn An có 3 quyển truyện tranh khác nhau: Doraemon, Pokemon và Thám Tử Lừng Danh Conan. An muốn chọn ra 2 quyển để mang theo đi du lịch. Vậy An có bao nhiêu cách chọn 2 quyển truyện tranh?
    - Bạn Mai có 3 loại hoa hồng: hồng đỏ, hồng trắng và hồng vàng. Mai muốn chọn ra 2 bông hồng để cắm vào lọ. Vậy Mai có bao nhiêu cách chọn 2 bông hồng từ 3 loại hoa hồng đó?
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
    if type_math == 'th':
        context = 'tổ hợp C(' + str(n) + ', ' + str(k) + ')'
    if type_math == 'ch':
        context = 'chỉnh hợp P(' + str(n) + ', ' + str(k) + ')'
    if type_math == 'hv':
        context = 'hoán  vị P(' + str(n) + ')'
    prompt = create_prompt(context)
    response = llm.invoke(prompt).content
    return response

def get_solve(context):
    prompt = create_prompt_solve(context)
    response = llm.invoke(prompt).content
    return response
# print(get_response('th', 3, 2))
