# dialogue_manager.py

from typing import List, Dict, Union
from config import GOOGLE_API_KEY
import google.generativeai as genai

# === Cấu hình Gemini ===
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# === Mẫu prompt ===
TEMPLATE = """
Bạn là một trợ lý gợi ý món ăn thông minh và thân thiện.

Hồ sơ người dùng:
{user_profile}

Lịch sử hội thoại:
{dialogue_history}

Nhiệm vụ của bạn:

1. Tạo một phản hồi tự nhiên bằng tiếng Việt, thân thiện và phù hợp với ngữ cảnh hội thoại. Bắt đầu bằng: Response:

2. Nếu cần gợi ý món ăn, hãy tạo một dòng riêng bên dưới với: Request: <truy vấn tìm món ăn>
- Truy vấn này cần ngắn gọn, phản ánh chính xác các yêu cầu của người dùng được nói ra trong hội thoại (ví dụ: món Việt, không phở, ít calo…).
- Nếu hồ sơ người dùng có thông tin bổ sung (ví dụ: không ăn thịt bò, thích món Nhật...), bạn có thể kết hợp thêm nếu phù hợp và chưa được đề cập trong hội thoại.

Yêu cầu quan trọng:
- **Không được liệt kê tên món ăn cụ thể trong Request**
- Request phải là một **mô tả tổng quát**, dùng để tìm kiếm trong hệ thống món ăn có sẵn.
- Chỉ sử dụng thông tin thực tế từ hội thoại và hồ sơ người dùng.
- **Tuyệt đối không sáng tạo ra món ăn mới hoặc món ăn không có trong hệ thống.**

Kết quả đầu ra luôn có 2 dòng:
Response: <câu phản hồi bằng tiếng Việt>
Request: <truy vấn tìm món ăn>
"""
# === Format hồ sơ người dùng dạng text từ dictionary ===
def format_user_profile(profile: Dict[str, Union[str, int, List[str]]]) -> str:
    lines = []
    for key, value in profile.items():
        if isinstance(value, list):
            lines.append(f"- {key}: {', '.join(value)}")
        else:
            lines.append(f"- {key}: {value}")
    return "\n".join(lines)

# === Format toàn bộ context đưa vào prompt cho LLM ===
def format_context(dialogue: List[str], profile: Dict[str, Union[str, int, List[str]]]) -> str:
    dialogue_text = "\n".join(dialogue)
    profile_text = format_user_profile(profile) if profile else "(none)"
    return TEMPLATE.format(user_profile=profile_text, dialogue_history=dialogue_text)

def gemini_generate(context: str) -> str:
    try:
        response = model.generate_content(context)
        return response.text.strip()
    except Exception as e:
        print("[Gemini Error]", e)
        return "Response: Lỗi khi gọi Gemini API\nRequest: (none)"

# === Tách output thành dict gồm response và truy vấn request ===
def parse_output(output: str) -> Dict[str, str]:
    result = {}
    for line in output.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result

def dialogue_manager(dialogue: List[str], user_profile: List[str]) -> Dict[str, str]:
    context = format_context(dialogue, user_profile)
    output = gemini_generate(context)
    return parse_output(output)
