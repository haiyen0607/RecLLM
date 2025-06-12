from dialogue_manager import dialogue_manager
from retrieval import retrieve
from ranker import rank_items
from profile_store import update_profile

if __name__ == "__main__":
    # === Bước 1: Khai báo user_id và cập nhật hồ sơ người dùng ===
    user_id = "u1"
    new_info = {
        "age": 28,
        "gender": "nữ",
        "dietary_restrictions": ["Rong biển"],
        "preferred_styles": ["Nhật"],
        "goals": [],
        "likes": ["Ramen"],
        "dislikes": []
    }
    user_profile = update_profile(user_id, new_info)

    # === Bước 2: Đối thoại mẫu giữa người dùng và hệ thống ===
    dialogue = [
        "User: Tôi muốn ăn món Nhật vào bữa tối nay",
        "System: Bạn có yêu cầu gì về chế độ ăn không?",
        "User: Tôi không thích ăn Sushi"
    ]

    # === Bước 3: Gọi Dialogue Manager sinh phản hồi và truy vấn tìm món ăn ===
    llm_output = dialogue_manager(dialogue, user_profile)
    response = llm_output.get("Response", "")
    query = llm_output.get("Request", "")

    print("\n== RESPONSE ==\n", response)
    print("\n== REQUEST ==\n", query)

    # === Bước 4: Truy xuất item dựa hoàn toàn vào query (KHÔNG dùng user_profile ở đây) ===
    retrieved_items = retrieve(query)  # Không truyền user_profile

    print("\n== RETRIEVED ITEMS ==")
    for i, item in enumerate(retrieved_items, 1):
        print(f"{i}. {item['name']} - {item['description']}")

    # === Bước 5: Xếp hạng các món ăn dựa vào user_profile ===
    ranked = rank_items(retrieved_items, query, user_profile)

    print("\n== RANKED ITEMS ==")
    for idx, result in enumerate(ranked, 1):
        item = result["item"]
        print(f"{idx}. {item.get('name')} (Score: {result['score']})")
        print("   -> Explanation:", result["explanation"])

    # === Bước 6: In danh sách MENU GỢI Ý CUỐI CÙNG nếu điểm cao hơn ngưỡng ===
    MIN_SCORE = 5.0
    filtered_items = [r for r in ranked if r["score"] >= MIN_SCORE]

    print("\n== MENU GỢI Ý CUỐI CÙNG ==")
    if filtered_items:
        for i, r in enumerate(filtered_items, 1):
            item = r["item"]
            print(f"{i}. {item.get('name')} - {item.get('description')}")
    else:
        print("Không có món nào phù hợp vượt ngưỡng.")



# from dialogue_manager import dialogue_manager
# from retrieval import retrieve
# from ranker import rank_items
# from profile_store import update_profile, load_profile

# # Hàm lọc món ăn theo user_profile
# def filter_by_user_profile(items, profile):
#     preferred_styles = [s.lower() for s in profile.get("preferred_styles", [])]
#     dislikes = [d.lower() for d in profile.get("dislikes", [])]

#     filtered = []
#     for item in items:
#         style = item.get("style", "").lower()
#         name = item.get("name", "").lower()
#         description = item.get("description", "").lower()
#         tags = [t.lower() for t in item.get("tags", [])]

#         # Nếu có preferred_styles mà style không thuộc, thì loại
#         if preferred_styles and style not in preferred_styles:
#             continue

#         # Nếu name/description/tags chứa từ khóa bị dislike → loại
#         if any(d in name or d in description or d in " ".join(tags) for d in dislikes):
#             continue

#         filtered.append(item)
#     return filtered

# if __name__ == "__main__":
#     # === Khai báo user_id và cập nhật thông tin profile (nếu có mới) ===
#     # user_id = "u12345"
#     # new_info = {
#     #     "age": 28,
#     #     "gender": "nam",
#     #     "dietary_restrictions": ["không ăn thịt bò"],
#     #     "preferred_styles": ["Nhật"],
#     #     "goals": ["giảm cân"],
#     #     "likes": ["món nhẹ", "súp"],
#     #     "dislikes": ["đồ chiên"]
#     # }
#     user_id = "u1"
#     new_info = {
#         "age": 28,
#         "gender": "nữ",
#         "dietary_restrictions": [],
#         "preferred_styles": ["Việt"],
#         "goals": ["ít calo"],
#         "likes": [],
#         "dislikes": ["phở"]
#     }
#     user_profile = update_profile("u1", new_info)

#     # === Khai báo hội thoại của người dùng với hệ thống ===
#     dialogue = [
#         "User: Tôi muốn ăn món Việt vào bữa tối nay",
#         "System: Bạn có yêu cầu gì về chế độ ăn không?",
#         "User: Không"
#     ]

#     # === Block 1: Đối thoại + sinh truy vấn từ Gemini ===
#     llm_output = dialogue_manager(dialogue, user_profile)
#     response = llm_output.get("Response", "")
#     query = llm_output.get("Request", "")

#     print("\n== RESPONSE ==\n", response)
#     print("\n== REQUEST ==\n", query)

#     # === Block 2: Truy xuất các item phù hợp từ item corpus ===
#     retrieved_items = retrieve(query)
#     print("\n== RETRIEVED ITEMS ==")
#     for i, item in enumerate(retrieved_items, 1):
#         print(f"{i}. {item['name']} - {item['description']}")

#     # === Block 3: Xếp hạng và giải thích từng item ===
#     ranked = rank_items(retrieved_items, query)

#     print("\n== RANKED ITEMS ==")
#     for idx, result in enumerate(ranked, 1):
#         item = result["item"]
#         print(f"{idx}. {item.get('name')} (Score: {result['score']})")
#         print("   -> Explanation:", result["explanation"])

#     # === Lọc và in ra MENU GỢI Ý CUỐI CÙNG ===
#     MIN_SCORE = 5.0
#     filtered_items = [r for r in ranked if r["score"] >= MIN_SCORE]

#     print("\n== MENU GỢI Ý CUỐI CÙNG ==")
#     if filtered_items:
#         for i, r in enumerate(filtered_items, 1):
#             item = r["item"]
#             print(f"{i}. {item.get('name')} - {item.get('description')}")
#     else:
#         print("Không có món nào phù hợp vượt ngưỡng.")

