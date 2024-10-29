import os
from langchain_google_genai import ChatGoogleGenerativeAI

if 'GOOGLE_API_KEY' not in os.environ:
    os.environ['GOOGLE_API_KEY'] = "AIzaSyC6A1MJR-kk-KetpF3Llqna_GE4hulhwMU"

llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0.9)

def create_prompt(context):
    return prompt_template.format(context=context)

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

# print(get_response('th', 3, 2))
