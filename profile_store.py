import os
import json
from typing import Dict, Any

# Thư mục lưu hồ sơ người dùng
PROFILE_DIR = "user_profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)

def get_profile_path(user_id: str) -> str:
    return os.path.join(PROFILE_DIR, f"{user_id}.json")

def load_profile(user_id: str) -> Dict[str, Any]:
    path = get_profile_path(user_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "user_id": user_id,
        "name": "",
        "age": 0,
        "gender": "",
        "goals": [],
        "dietary_restrictions": [],
        "preferred_styles": [],
        "likes": [],
        "dislikes": []
    }

def save_profile(user_id: str, profile: Dict[str, Any]) -> None:
    path = get_profile_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

def update_profile(user_id: str, new_info: Dict) -> Dict:
    os.makedirs("user_profiles", exist_ok=True)
    profile_path = f"user_profiles/{user_id}.json"

    # Nếu đã tồn tại hồ sơ, load lên
    if os.path.exists(profile_path):
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
    else:
        profile = {"user_id": user_id}

    # Ghi đè hoàn toàn các trường trong new_info (kể cả empty list)
    for key, value in new_info.items():
        profile[key] = value

    # Lưu lại
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    return profile

