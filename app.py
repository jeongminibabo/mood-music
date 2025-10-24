import streamlit as st
import random

st.set_page_config(page_title="감정 + 장르 음악 추천기", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-size: cover;
        background-position: center;
        transition: background-image 1s ease-in-out;
    }
    .overlay {
        background-color: rgba(0,0,0,0.5);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
    }
    h1, h2, h3 {
        color: white;
        text-shadow: 1px 1px 2px black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎶 감정 + 장르 기반 음악 추천기")
st.write("기분과 장르를 선택하면 지금 당신에게 어울리는 노래를 추천해드려요 🌈")

# 감정과 장르 선택
mood = st.selectbox("현재 기분은 어떤가요?", ["기쁨 😀", "슬픔 😢", "분노 😡", "외로움 🥺", "힐링 🌿"])
genre = st.selectbox("어떤 장르의 음악을 듣고 싶나요?", ["한국 힙합 🔥", "한국 발라드 🎶", "팝 🎧", "인디 🌿"])

messages = {
    "기쁨 😀": "기분이 좋은 날엔 신나는 음악을 들어요 ☀️",
    "슬픔 😢": "마음을 위로해주는 음악이 필요하죠 🌧️",
    "분노 😡": "답답한 마음을 비트로 날려봐요 🔥",
    "외로움 🥺": "혼자일 땐 음악이 친구가 되어줄 거예요 💫",
    "힐링 🌿": "조용히 쉬어가요 🍃",
}

# 감정 + 장르별 음악 데이터 (노래, 유튜브 링크, 앨범커버 이미지)
music_data = {
    "기쁨 😀": {
        "한국 힙합 🔥": [
            ("식케이 - LOV3", "https://www.youtube.com/watch?v=6b8JlcRfC3U", "https://i.scdn.co/image/ab67616d0000b273c4c869ea56a9d8740a9c5e0b"),
            ("염따 - 더콰이엇", "https://www.youtube.com/watch?v=FC7S8vYhKmc", "https://i.scdn.co/image/ab67616d0000b2736b74cbba4f76cb414a65e5c2"),
        ],
        "한국 발라드 🎶": [
            ("폴킴 - 커피 한 잔 할래요", "https://www.youtube.com/watch?v=5q1R2zvY4fU", "https://i.scdn.co/image/ab67616d0000b273b784d97efc0b22d12f8fdb06"),
            ("아이유 - 좋은 날", "https://www.youtube.com/watch?v=jeqdYqsrsA0", "https://i.scdn.co/image/ab67616d0000b273bcfa53d32f6a4eac847aeac2"),
        ],
        "팝 🎧": [
            ("Pharrell Williams - Happy", "https://www.youtube.com/watch?v=ZbZSe6N_BXs", "https://i.scdn.co/image/ab67616d0000b2738949f2f870a26f6b9c78b93b"),
            ("Dua Lipa - Levitating", "https://www.youtube.com/watch?v=TUVcZfQe-Kw", "https://i.scdn.co/image/ab67616d0000b273b7a17eeb0d7b297c3b95b8a6"),
        ],
        "인디 🌿": [
            ("혁오 - Tomboy", "https://www.youtube.com/watch?v=ghfZcU6jBPM", "https://i.scdn.co/image/ab67616d0000b2733a3e6d9c9a1c507b7bb91cc4"),
            ("잔나비 - 주저하는 연인들을 위해", "https://www.youtube.com/watch?v=dp0F18FFCTE", "https://i.scdn.co/image/ab67616d0000b273ac6e567b3c2128b720e0c18a"),
        ],
    },
    "슬픔 😢": {
        "한국 힙합 🔥": [
            ("이센스 - 비행", "https://www.youtube.com/watch?v=ZsyqX-bpA1A", "https://i.scdn.co/image/ab67616d0000b27396706d4e9f7c35fa7a44cf83"),
            ("식케이 - See You In Every Party", "https://www.youtube.com/watch?v=QtbSjkl4IAg", "https://i.scdn.co/image/ab67616d0000b273ecf1f6a7e6ebec3ddcc0db5e"),
        ],
        "한국 발라드 🎶": [
            ("폴킴 - 모든 날, 모든 순간", "https://www.youtube.com/watch?v=OGgn4x4RlHo", "https://i.scdn.co/image/ab67616d0000b273b784d97efc0b22d12f8fdb06"),
            ("이하이 - 한숨", "https://www.youtube.com/watch?v=R6EdYfKPVUI", "https://i.scdn.co/image/ab67616d0000b273deed7e7f6816f2412b937ff8"),
        ],
        "팝 🎧": [
            ("Adele - Easy On Me", "https://www.youtube.com/watch?v=U3ASj1L6_sY", "https://i.scdn.co/image/ab67616d0000b273bfa99d7e1e2c16a315cf0ad5"),
            ("Sam Smith - Too Good at Goodbyes", "https://www.youtube.com/watch?v=J_ub7Etch2U", "https://i.scdn.co/image/ab67616d0000b27321b7a7ff0c664e8182b60b3f"),
        ],
        "인디 🌿": [
            ("10cm - 사랑은 은하수 다방에서", "https://www.youtube.com/watch?v=Hj5J4Rz76bM", "https://i.scdn.co/image/ab67616d0000b273a7da2a2532f68f9784c48db7"),
            ("검정치마 - 기다린 만큼, 더", "https://www.youtube.com/watch?v=U5pwsQ2Un2E", "https://i.scdn.co/image/ab67616d0000b273f8d1fda8c3b17e6dba8e64f0"),
        ],
    },
    "분노 😡": {
        "한국 힙합 🔥": [
            ("키드밀리 - 25", "https://www.youtube.com/watch?v=5Zz8yGnC6H8", "https://i.scdn.co/image/ab67616d0000b2736f4d2ed5ef4174a3b4a3b8f4"),
            ("이센스 - Gas", "https://www.youtube.com/watch?v=Urm7IVD2oO8", "https://i.scdn.co/image/ab67616d0000b27396706d4e9f7c35fa7a44cf83"),
            ("나플라 - Wu", "https://www.youtube.com/watch?v=spkAxv3DDEo", "https://i.scdn.co/image/ab67616d0000b27351eaa00374b7208e64fbcddc"),
        ],
        "한국 발라드 🎶": [
            ("김필 - 다시 사랑한다면", "https://www.youtube.com/watch?v=5bdFvYXm1tk", "https://i.scdn.co/image/ab67616d0000b273f48d92404f1b7df338424d24"),
            ("윤하 - 사건의 지평선", "https://www.youtube.com/watch?v=iqrMFNM8hOw", "https://i.scdn.co/image/ab67616d0000b273548cb4984b75c1eeb8b8ef8a"),
        ],
        "팝 🎧": [
            ("Eminem - Lose Yourself", "https://www.youtube.com/watch?v=_Yhyp-_hX2s", "https://i.scdn.co/image/ab67616d0000b27331a3c715e0ac5c5a2e799c5f"),
            ("Imagine Dragons - Believer", "https://www.youtube.com/watch?v=7wtfhZwyrcc", "https://i.scdn.co/image/ab67616d0000b273009c84b3bb1f1c9e8c13ebf8"),
        ],
        "인디 🌿": [
            ("검정치마 - EVERYTHING", "https://www.youtube.com/watch?v=f05h1Jj4p8M", "https://i.scdn.co/image/ab67616d0000b273f8d1fda8c3b17e6dba8e64f0"),
            ("새소년 - 난춘", "https://www.youtube.com/watch?v=KMNRkV6zEeE", "https://i.scdn.co/image/ab67616d0000b2734c936a4b9b43f013af665b29"),
        ],
    },
    "외로움 🥺": {
        "한국 힙합 🔥": [
            ("비프리 - INDO", "https://www.youtube.com/watch?v=6qDwAdM6w7s", "https://i.scdn.co/image/ab67616d0000b2732b4e1c0b53c3e828308e0f83"),
            ("boycold - Trail", "https://www.youtube.com/watch?v=znTbiuOHnp4", "https://i.scdn.co/image/ab67616d0000b273c31787046a9dfdb582a5da4d"),
        ],
        "한국 발라드 🎶": [
            ("정승환 - 너였다면", "https://www.youtube.com/watch?v=mf6U91VnP2A", "https://i.scdn.co/image/ab67616d0000b273e4fa9f2b812f51f7f79b65f3"),
            ("아이유 - 밤편지", "https://www.youtube.com/watch?v=BzYnNdJhZQw", "https://i.scdn.co/image/ab67616d0000b273267e97b6b7e87e0f58ef3f02"),
        ],
        "팝 🎧": [
            ("Coldplay - Fix You", "https://www.youtube.com/watch?v=k4V3Mo61fJM", "https://i.scdn.co/image/ab67616d0000b273dcb56b12a2047ed9cc2bc8b0"),
            ("Ed Sheeran - Photograph", "https://www.youtube.com/watch?v=nSDgHBxUbVQ", "https://i.scdn.co/image/ab67616d0000b2735c49b0a53bdb5075b83bb8e3"),
        ],
        "인디 🌿": [
            ("우효 - 민들레", "https://www.youtube.com/watch?v=qQ0tqtT0zGc", "https://i.scdn.co/image/ab67616d0000b27359e1570d1f3b2c718ff2eb8f"),
            ("카더가든 - 명동콜링", "https://www.youtube.com/watch?v=Z4TxqXqu5XI", "https://i.scdn.co/image/ab67616d0000b273ae8d24b5c3587ec7c6adbf1e"),
        ],
    },
    "힐링 🌿": {
        "한국 힙합 🔥": [
            ("염따 - IE러니", "https://www.youtube.com/watch?v=K5n88M1A4aU", "https://i.scdn.co/image/ab67616d0000b2739b2c38eae2f2d2d8e7a948f3"),
            ("빈지노 - Always Awake", "https://www.youtube.com/watch?v=vyvRAyxzt8w", "https://i.scdn.co/image/ab67616d0000b2738dc9a4a8b0a401cd58a2251d"),
        ],
        "한국 발라드 🎶": [
            ("로이킴 - 봄봄봄", "https://www.youtube.com/watch?v=9bZkp7q19f0", "https://i.scdn.co/image/ab67616d0000b27323e56d890c27cd0fa0f82ef1"),
            ("폴킴 - 초록빛", "https://www.youtube.com/watch?v=4nYkHKj8B7A", "https://i.scdn.co/image/ab67616d0000b273b784d97efc0b22d12f8fdb06"),
        ],
        "팝 🎧": [
            ("Lauv - Paris in the Rain", "https://www.youtube.com/watch?v=0bM0wVjU2-k", "https://i.scdn.co/image/ab67616d0000b273ac4cbf82a377ddf42b6bcb75"),
            ("Daniel Caesar - Best Part", "https://www.youtube.com/watch?v=iKkqKzZR9oA", "https://i.scdn.co/image/ab67616d0000b2738a772d3ccbb6204fb3f6b2e1"),
        ],
        "인디 🌿": [
            ("검정치마 - 기다린 만큼, 더", "https://www.youtube.com/watch?v=U5pwsQ2Un2E", "https://i.scdn.co/image/ab67616d0000b273f8d1fda8c3b17e6dba8e64f0"),
            ("데이식스 - 한 페이지가 될 수 있게", "https://www.youtube.com/watch?v=5f3L_oWfQBM", "https://i.scdn.co/image/ab67616d0000b273e9dc8a364b0a4a2a7964c8e8"),
        ],
    },
}

# 추천 버튼
if st.button("🎲 추천 받기"):
    if genre not in music_data[mood]:
        st.warning("해당 감정과 장르에 맞는 곡이 아직 준비되지 않았어요 😢")
    else:
        song, link, cover = random.choice(music_data[mood][genre])
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url('{cover}');
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown(f"<div class='overlay'><h2>{messages[mood]}</h2></div>", unsafe_allow_html=True)
        st.success(f"🎧 추천 곡: {song}")
        st.video(link)
