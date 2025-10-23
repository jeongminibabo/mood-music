import streamlit as st
import random

st.set_page_config(page_title="감정 + 장르 음악 추천", layout="wide")
st.title("🎵 감정 + 장르 기반 음악 추천 웹사이트")

# 1️⃣ 감정 선택
mood = st.selectbox(
    "지금 기분은 어떤가요?",
    ["기쁨 😀", "슬픔 😢", "신남 🔥", "힐링 🌿"]
)

# 2️⃣ 장르 선택
genre_options = {
    "기쁨 😀": ["한국 힙합 🔥", "K-POP 댄스 💃"],
    "슬픔 😢": ["한국 발라드 😢", "인디 🌿"],
    "신남 🔥": ["한국 힙합 🔥", "K-POP 댄스 💃"],
    "힐링 🌿": ["인디 🌿", "한국 발라드 😢"]
}

genre = st.selectbox("듣고 싶은 장르는?", genre_options[mood])

# 3️⃣ 감정+장르 조합 추천 데이터 (리스트 여러 곡)
music_data = {
    ("기쁨 😀", "한국 힙합 🔥"): [
        ("BE'O - Counting Stars", "https://www.youtube.com/watch?v=kk1hfVaxTCI", "https://picsum.photos/800/400?coffee"),
        ("창모 - METEOR", "https://www.youtube.com/watch?v=J1Ov3jmH0gU", "https://picsum.photos/800/400?fire"),
    ],
    ("기쁨 😀", "K-POP 댄스 💃"): [
        ("BLACKPINK - How You Like That", "https://www.youtube.com/watch?v=ioNng23DkIM", "https://picsum.photos/800/400?dance"),
        ("IVE - I AM", "https://www.youtube.com/watch?v=6ZUIwj3FgUY", "https://picsum.photos/800/400?party"),
    ],
    ("슬픔 😢", "한국 발라드 😢"): [
        ("폴킴 - 모든 날, 모든 순간", "https://www.youtube.com/watch?v=OGgn4x4RlHo", "https://picsum.photos/800/400?room"),
        ("성시경 - 두 사람", "https://www.youtube.com/watch?v=2XBBfJxnNq0", "https://picsum.photos/800/400?relax"),
    ],
    ("슬픔 😢", "인디 🌿"): [
        ("검정치마 - EVERYTHING", "https://www.youtube.com/watch?v=f05h1Jj4p8M", "https://picsum.photos/800/400?nature"),
        ("장범준 - 흔들리는 꽃들 속에서", "https://www.youtube.com/watch?v=tLV83ndOw1A", "https://picsum.photos/800/400?nature"),
    ],
    ("신남 🔥", "한국 힙합 🔥"): [
        ("창모 - METEOR", "https://www.youtube.com/watch?v=J1Ov3jmH0gU", "https://picsum.photos/800/400?fire"),
        ("BE'O - Counting Stars", "https://www.youtube.com/watch?v=kk1hfVaxTCI", "https://picsum.photos/800/400?coffee"),
    ],
    ("신남 🔥", "K-POP 댄스 💃"): [
        ("BLACKPINK - How You Like That", "https://www.youtube.com/watch?v=ioNng23DkIM", "https://picsum.photos/800/400?dance"),
        ("IVE - I AM", "https://www.youtube.com/watch?v=6ZUIwj3FgUY", "https://picsum.photos/800/400?party"),
    ],
    ("힐링 🌿", "인디 🌿"): [
        ("장범준 - 흔들리는 꽃들 속에서", "https://www.youtube.com/watch?v=tLV83ndOw1A", "https://picsum.photos/800/400?nature"),
        ("검정치마 - EVERYTHING", "https://www.youtube.com/watch?v=f05h1Jj4p8M", "https://picsum.photos/800/400?nature"),
    ],
    ("힐링 🌿", "한국 발라드 😢"): [
        ("성시경 - 두 사람", "https://www.youtube.com/watch?v=2XBBfJxnNq0", "https://picsum.photos/800/400?relax"),
        ("폴킴 - 모든 날, 모든 순간", "https://www.youtube.com/watch?v=OGgn4x4RlHo", "https://picsum.photos/800/400?room"),
    ],
}

# 4️⃣ 랜덤 추천 버튼
if st.button("🎲 추천곡 바꾸기"):
    recommendations = music_data.get((mood, genre), [])
    if recommendations:
        song, url, image_url = random.choice(recommendations)
        st.subheader(f"추천: {song}")
        st.image(image_url, use_column_width=True)
        st.video(url)
    else:
        st.write("죄송해요 😢 추천 곡이 없습니다.")