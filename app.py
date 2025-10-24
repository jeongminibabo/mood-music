import streamlit as st
import random
import pandas as pd
import os


st.set_page_config(page_title="감정 + 장르 음악 추천기", layout="wide")

st.markdown(
    """
    <style>
    .overlay {
        background-color: rgba(0,0,0,0.6);
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
            ("식케이 - LOV3", "https://www.youtube.com/watch?v=6b8JlcRfC3U"),
            ("염따 - 더콰이엇", "https://youtu.be/BcXaRfuBgko?si=D_GCZt_UK4rJKznX"),
        ],
        "한국 발라드 🎶": [
            ("폴킴 - 커피 한 잔 할래요", "https://youtu.be/l7PgoVBZpc8?si=vPBAEX_v__L22oX4"),
            ("아이유 - 좋은 날", "https://youtu.be/V6WWJNpIJN4?si=2sOjajQRCRujw3MH"),
        ],
        "팝 🎧": [
            ("Pharrell Williams - Happy", "https://youtu.be/ZbZSe6N_BXs?si=Uo2N0FB0Eze8_uH4"),
            ("Dua Lipa - Levitating", "https://youtu.be/TUVcZfQe-Kw?si=exq_r_PCQyD0L4-Y"),
        ],
        "인디 🌿": [
            ("혁오 - Tomboy", "https://youtu.be/w3-AKITQMi0?si=icJZ33bNhL-cY8-j"),
            ("잔나비 - 주저하는 연인들을 위해", "https://youtu.be/GpQ222I1ULc?si=1daFmny9sRNbyoLN"),
        ],
    },
    "슬픔 😢": {
        "한국 힙합 🔥": [
            ("이센스 - 비행", "https://www.youtube.com/watch?v=ZsyqX-bpA1A"),
            ("식케이 - See You In Every Party", "https://www.youtube.com/watch?v=QtbSjkl4IAg"),
        ],
        "한국 발라드 🎶": [
            ("폴킴 - 모든 날, 모든 순간", "https://www.youtube.com/watch?v=OGgn4x4RlHo"),
            ("이하이 - 한숨", "https://www.youtube.com/watch?v=R6EdYfKPVUI"),
        ],
        "팝 🎧": [
            ("Adele - Easy On Me", "https://www.youtube.com/watch?v=U3ASj1L6_sY"),
            ("Sam Smith - Too Good at Goodbyes", "https://www.youtube.com/watch?v=J_ub7Etch2U"),
            ("Sam Smith - to die for", "https://youtu.be/POIK1H3L86k?si=-GtOGhj3eta256Ao"),
        ],
        "인디 🌿": [
            ("10cm - 사랑은 은하수 다방에서", "https://www.youtube.com/watch?v=Hj5J4Rz76bM"),
            ("검정치마 - 기다린 만큼, 더", "https://www.youtube.com/watch?v=U5pwsQ2Un2E"),
            ("wave to earth - seasons", "https://youtu.be/g19EuryzWbE?si=Epo7feUp2SPE5yXB"),
        ],
    },
    "분노 😡": {
        "한국 힙합 🔥": [
            ("키드밀리 - 25", "https://www.youtube.com/watch?v=5Zz8yGnC6H8"),
            ("이센스 - Gas", "https://www.youtube.com/watch?v=Urm7IVD2oO8"),
            ("나플라 - Wu", "https://www.youtube.com/watch?v=spkAxv3DDEo"),
        ],
        "한국 발라드 🎶": [
            ("김필 - 다시 사랑한다면", "https://www.youtube.com/watch?v=5bdFvYXm1tk"),
            ("윤하 - 사건의 지평선", "https://www.youtube.com/watch?v=iqrMFNM8hOw"),
        ],
        "팝 🎧": [
            ("Eminem - Lose Yourself", "https://www.youtube.com/watch?v=_Yhyp-_hX2s"),
            ("Imagine Dragons - Believer", "https://www.youtube.com/watch?v=7wtfhZwyrcc"),
        ],
        "인디 🌿": [
            ("검정치마 - EVERYTHING", "https://www.youtube.com/watch?v=f05h1Jj4p8M"),
            ("새소년 - 난춘", "https://www.youtube.com/watch?v=KMNRkV6zEeE"),
        ],
    },
    "외로움 🥺": {
        "한국 힙합 🔥": [
            ("비프리 - INDO", "https://www.youtube.com/watch?v=6qDwAdM6w7s"),
            ("boycold - Trail", "https://www.youtube.com/watch?v=znTbiuOHnp4"),
            ("양홍원- SAHARA", "https://youtu.be/Na3NTn9KQ4Y?si=kB7TG0sWlH2EZxbo"),
        ],
        "한국 발라드 🎶": [
            ("정승환 - 너였다면", "https://www.youtube.com/watch?v=mf6U91VnP2A"),
            ("아이유 - 밤편지", "https://www.youtube.com/watch?v=BzYnNdJhZQw"),
        ],
        "팝 🎧": [
            ("Coldplay - Fix You", "https://www.youtube.com/watch?v=k4V3Mo61fJM"),
            ("Ed Sheeran - Photograph", "https://www.youtube.com/watch?v=nSDgHBxUbVQ"),
        ],
        "인디 🌿": [
            ("우효 - 민들레", "https://www.youtube.com/watch?v=qQ0tqtT0zGc"),
            ("카더가든 - 명동콜링", "https://www.youtube.com/watch?v=Z4TxqXqu5XI"),
        ],
    },
    "힐링 🌿": {
        "한국 힙합 🔥": [
            ("염따 - IE러니", "https://www.youtube.com/watch?v=K5n88M1A4aU"),
            ("빈지노 - Always Awake", "https://www.youtube.com/watch?v=vyvRAyxzt8w"),
        ],
        "한국 발라드 🎶": [
            ("로이킴 - 봄봄봄", "https://www.youtube.com/watch?v=9bZkp7q19f0"),
            ("폴킴 - 초록빛", "https://www.youtube.com/watch?v=4nYkHKj8B7A"),
        ],
        "팝 🎧": [
            ("Lauv - Paris in the Rain", "https://www.youtube.com/watch?v=0bM0wVjU2-k"),
            ("Daniel Caesar - Best Part", "https://www.youtube.com/watch?v=iKkqKzZR9oA"),
        ],
        "인디 🌿": [
            ("검정치마 - 기다린 만큼, 더", "https://www.youtube.com/watch?v=U5pwsQ2Un2E"),
            ("데이식스 - 한 페이지가 될 수 있게", "https://www.youtube.com/watch?v=5f3L_oWfQBM"),
        ],
    },
}

# 추천 버튼
if st.button("🎲 추천 받기"):
    if genre not in music_data[mood]:
        st.warning("해당 감정과 장르에 맞는 곡이 아직 준비되지 않았어요 😢")
    else:
        song, link = random.choice(music_data[mood][genre])
        st.markdown(f"<div class='overlay'><h2>{messages[mood]}</h2></div>", unsafe_allow_html=True)
        st.success(f"🎧 추천 곡: {song}")
        st.video(link)
st.title("의견 작성 폼")

# 의견 입력란
opinion = st.text_area("추가 되었으면 하는 노래를 추천해주세요:", height=150, placeholder="여기에 작성하세요...")

# 의견 제출 버튼
if st.button("의견 제출"):
    if opinion.strip() == "":
        st.warning("의견을 작성해주세요.")
    else:
        st.success("의견이 제출되었습니다!")
        st.write("작성하신 의견:", opinion)

        # CSV 파일 경로
        file_path = "opinions.csv"

        # 기존 CSV 읽기 또는 새 데이터프레임 생성
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(columns=["의견"])

        # 새 의견 추가
        df = pd.concat([df, pd.DataFrame({"의견": [opinion]})], ignore_index=True)
        df.to_csv(file_path, index=False)

# ==============================
# 관리자용 의견 확인
# ==============================
st.sidebar.header("관리자 로그인")
password = st.sidebar.text_input("비밀번호를 입력하세요", type="password")

# 비밀번호 확인
if password == "hy120134":  # 여기에 원하는 비밀번호 입력
    st.sidebar.success("로그인 성공!")
    
    file_path = "opinions.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.subheader("모든 의견 확인 (관리자 전용)")
        st.dataframe(df)  # 테이블로 표시
    else:
        st.info("저장된 의견이 없습니다.")
elif password:
    st.sidebar.error("비밀번호가 틀렸습니다.")

