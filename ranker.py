# # ranker.py

# from typing import List, Dict, Any
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# # === Load API Key và khởi tạo Gemini ===
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel("models/gemini-1.5-flash")

# # === Prompt mẫu cho đánh giá ===
# RANKER_TEMPLATE = """
# Truy vấn của người dùng: "{query}"

# Thông tin món ăn được đề xuất:
# - Tên món: {name}
# - Mô tả: {description}
# - Phong cách: {style}
# - Tags: {tags}
# - Lượng calo: {calories} kcal

# Yêu cầu:
# 1. Đánh giá mức độ phù hợp của món ăn với truy vấn người dùng (dựa trên chế độ ăn, phong cách, sở thích, v.v.). Cho điểm từ 1 đến 10.
# 2. Giải thích bằng tiếng Việt tại sao món này phù hợp hoặc không phù hợp.

# Định dạng phản hồi yêu cầu:
# Score: <số điểm>
# Explanation: <giải thích>
# """

# def build_prompt(query: str, item: Dict[str, Any]) -> str:
#     return RANKER_TEMPLATE.format(
#         query=query,
#         name=item.get("name", "(no name)"),
#         description=item.get("description", "(no description)"),
#         style=item.get("style", "(unknown)"),
#         tags=", ".join(item.get("tags", [])),
#         calories=item.get("calories", "N/A")
#     )

# def score_and_explain(item: Dict[str, Any], query: str) -> Dict[str, Any]:
#     if not isinstance(item, dict):
#         return {"item": item, "score": 0, "explanation": "Invalid item format"}

#     prompt = build_prompt(query, item)
#     try:
#         response = model.generate_content(prompt)
#         lines = response.text.strip().splitlines()
#         score = 0.0
#         explanation = "No explanation"
#         for line in lines:
#             if line.lower().startswith("score:"):
#                 try:
#                     score = float(line.split(":", 1)[1].strip())
#                 except ValueError:
#                     score = 0.0
#             elif line.lower().startswith("explanation:"):
#                 explanation = line.split(":", 1)[1].strip()
#         return {"item": item, "score": score, "explanation": explanation}
#     except Exception as e:
#         return {"item": item, "score": 0, "explanation": f"[Error] {str(e)}"}

# def rank_items(candidates: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
#     cleaned = [c for c in candidates if isinstance(c, dict)]
#     ranked = [score_and_explain(item, query) for item in cleaned]
#     return sorted(ranked, key=lambda x: x["score"], reverse=True)
from typing import List, Dict, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv

# === Load API Key và khởi tạo Gemini ===
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# === Prompt mẫu cho đánh giá ===
RANKER_TEMPLATE = """
Truy vấn của người dùng: "{query}"

Hồ sơ người dùng (nếu có):
{user_profile}

Thông tin món ăn được đề xuất:
- Tên món: {name}
- Mô tả: {description}
- Phong cách: {style}
- Tags: {tags}
- Lượng calo: {calories} kcal

Yêu cầu:
1. Đánh giá mức độ phù hợp của món ăn với truy vấn và hồ sơ người dùng. Cho điểm từ 1 đến 10.
2. Giải thích bằng tiếng Việt tại sao món này phù hợp hoặc không phù hợp.

Định dạng phản hồi yêu cầu:
Score: <số điểm>
Explanation: <giải thích>
"""

def build_prompt(query: str, item: Dict[str, Any], user_profile: Dict[str, Any] = None) -> str:
    profile_text = (
        f"- Tuổi: {user_profile.get('age')}\n"
        f"- Giới tính: {user_profile.get('gender')}\n"
        f"- Phong cách yêu thích: {', '.join(user_profile.get('preferred_styles', []))}\n"
        f"- Không ăn: {', '.join(user_profile.get('dietary_restrictions', []))}\n"
        f"- Mục tiêu: {', '.join(user_profile.get('goals', []))}\n"
        f"- Thích: {', '.join(user_profile.get('likes', []))}\n"
        f"- Không thích: {', '.join(user_profile.get('dislikes', []))}\n"
        if user_profile else "(Không có hồ sơ người dùng)"
    )

    return RANKER_TEMPLATE.format(
        query=query,
        user_profile=profile_text,
        name=item.get("name", "(no name)"),
        description=item.get("description", "(no description)"),
        style=item.get("style", "(unknown)"),
        tags=", ".join(item.get("tags", [])),
        calories=item.get("calories", "N/A")
    )

def score_and_explain(item: Dict[str, Any], query: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(item, dict):
        return {"item": item, "score": 0, "explanation": "Invalid item format"}

    prompt = build_prompt(query, item, user_profile)
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().splitlines()
        score = 0.0
        explanation = "No explanation"
        for line in lines:
            if line.lower().startswith("score:"):
                try:
                    score = float(line.split(":", 1)[1].strip())
                except ValueError:
                    score = 0.0
            elif line.lower().startswith("explanation:"):
                explanation = line.split(":", 1)[1].strip()
        return {"item": item, "score": score, "explanation": explanation}
    except Exception as e:
        return {"item": item, "score": 0, "explanation": f"[Error] {str(e)}"}

def rank_items(candidates: List[Dict[str, Any]], query: str, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    cleaned = [c for c in candidates if isinstance(c, dict)]
    ranked = [score_and_explain(item, query, user_profile) for item in cleaned]
    return sorted(ranked, key=lambda x: x["score"], reverse=True)
