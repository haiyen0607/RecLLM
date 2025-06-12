from typing import List, Dict
from rapidfuzz import process
import json

# === Load item corpus ===
def load_item_corpus(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f.readlines()]

# === Tạo chuỗi tìm kiếm từ item ===
def build_search_strings(items: List[Dict]) -> List[str]:
    search_strings = []
    for item in items:
        name = item.get("name", "")
        description = item.get("description", "")
        tags = " ".join(item.get("tags", []))
        style = item.get("style", "")
        combined = f"{name} ||| {style} ||| {description} ||| {tags}"  
        search_strings.append(combined)
    return search_strings

# === Truy xuất các ứng viên phù hợp theo fuzzy matching ===
def retrieve_candidates(query: str, items: List[Dict], k: int = 10) -> List[Dict]:
    search_strings = build_search_strings(items)
    results = []

    for idx, s in enumerate(search_strings):
        parts = s.split("|||")
        name, style, description, tags = [p.strip() for p in parts]

        # Tính điểm từng phần
        score_name = process.extractOne(query, [name])[1]
        score_style = process.extractOne(query, [style])[1]
        score_desc = process.extractOne(query, [description])[1]
        score_tags = process.extractOne(query, [tags])[1]

        # Weighted scoring: style và name quan trọng hơn
        total_score = (
            0.4 * score_name +
            0.3 * score_style +
            0.2 * score_desc +
            0.1 * score_tags
        )

        results.append((total_score, idx))

    results.sort(reverse=True)
    top_items = []
    for score, idx in results[:k]:
        item = items[idx].copy()
        item["retrieval_score"] = round(score, 2)
        top_items.append(item)

    return top_items


# === Hàm chính để truy xuất ===
def retrieve(query: str, corpus_path: str = "data/menu.jsonl", top_k: int = 10) -> List[Dict]:
    items = load_item_corpus(corpus_path)
    candidates = retrieve_candidates(query, items, top_k)
    return candidates


# from typing import List, Dict
# from rapidfuzz import process
# import json

# # Load item corpus (e.g. list of food items with metadata)
# def load_item_corpus(path: str) -> List[Dict]:
#     with open(path, "r", encoding="utf-8") as f:
#         return [json.loads(line) for line in f.readlines()]

# # Extract a search field from each item (e.g. name + description)
# def build_search_strings(items: List[Dict]) -> List[str]:
#     search_strings = []
#     for item in items:
#         name = item.get("name", "")
#         style = item.get("style", "")
#         description = item.get("description", "")
#         tags = " ".join(item.get("tags", [])) # tags là list
#         combined = f"{name} - {style} - {description} - {tags}"
#         search_strings.append(combined)
#     return search_strings

# # Perform fuzzy matching between query and item texts
# def retrieve_candidates(query: str, items: List[Dict], k: int = 5) -> List[Dict]:
#     search_strings = build_search_strings(items)
#     results = process.extract(query, search_strings, limit=k)

#     top_items = []
#     for match_text, score, idx in results:
#         item = items[idx]
#         # Giữ lại toàn bộ thông tin gốc của item và thêm trường "score"
#         item_with_score = dict(item)  # sao chép toàn bộ fields gốc
#         item_with_score["retrieval_score"] = score  # gán thêm score riêng biệt
#         top_items.append(item_with_score)
#     return top_items

# # Entry point: get query string and return recommendation slate
# def retrieve(query: str, corpus_path: str = "data/menu.jsonl", top_k: int = 10, user_profile: Dict = None) -> List[Dict]:
#     items = load_item_corpus(corpus_path)

#     # === [1] Lọc sơ bộ theo profile nếu có ===
#     if user_profile:
#         preferred_styles = user_profile.get("preferred_styles", [])
#         dislikes = user_profile.get("dislikes", [])

#         def is_suitable(item):
#             # Ưu tiên đúng phong cách
#             if preferred_styles and item.get("style") not in preferred_styles:
#                 return False
#             # Tránh món trong dislikes (tên món hoặc tags)
#             if any(d.lower() in item.get("name", "").lower() for d in dislikes):
#                 return False
#             if any(d.lower() in " ".join(item.get("tags", [])).lower() for d in dislikes):
#                 return False
#             return True

#         items = [item for item in items if is_suitable(item)]

#     # === [2] Thực hiện fuzzy search sau khi lọc ===
#     candidates = retrieve_candidates(query, items, top_k)
#     return candidates
