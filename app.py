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
            ("식케이 - LOV3", "https://youtu.be/oCvA-i9OTyg?si=nibW9SxH1YIU33Hr"),
            ("염따 - 더콰이엇", "https://youtu.be/BcXaRfuBgko?si=D_GCZt_UK4rJKznX"),
            ("오케이션 - lalala", "https://youtu.be/4VrMjTrT5UI?si=XMUsKOgd2fxUIfap"),
        ],
        "한국 발라드 🎶": [
            ("폴킴 - 커피 한 잔 할래요", "https://youtu.be/l7PgoVBZpc8?si=vPBAEX_v__L22oX4"),
            ("아이유 - 좋은 날", "https://youtu.be/V6WWJNpIJN4?si=2sOjajQRCRujw3MH"),
        ],
        "팝 🎧": [
            ("Pharrell Williams - Happy", "https://youtu.be/ZbZSe6N_BXs?si=Uo2N0FB0Eze8_uH4"),
            ("Dua Lipa - Levitating", "https://youtu.be/TUVcZfQe-Kw?si=exq_r_PCQyD0L4-Y"),
            ("Ed Sheeran - 2 step", "https://youtu.be/Z_MvkyuOJgk?si=YEIdvmXvGCgXYi-3"),
            ("Clay and friends - Going up the coast", "https://youtu.be/D1v3_8xVha8?si=HArAuIz1Ob6fPTtm"),
        ],
        "인디 🌿": [
            ("혁오 - Tomboy", "https://youtu.be/w3-AKITQMi0?si=icJZ33bNhL-cY8-j"),
            ("우효 - 민들레", "https://youtu.be/Kaq4LFM47I0?si=aiIb2IfNY1nQbzZi"),
        ],
    },
    "슬픔 😢": {
        "한국 힙합 🔥": [
            ("이센스 - 비행", "https://youtu.be/Guul8Df7HfU?si=r3dFcUaZSM5kaLXP"),
            ("식케이 - See You In Every Party", "https://www.youtube.com/watch?v=QtbSjkl4IAg"),
            ("최엘비 - 독립음악", "https://youtu.be/SLWpFHwq820?si=NOFdPn_qlnQThKSL"),
        ],
        "한국 발라드 🎶": [
            ("폴킴 - 모든 날, 모든 순간", "https://youtu.be/nq0BYGyH2Do?si=OMQ2kjHDXzv3KZ1k"),
            ("이하이 - 한숨", "https://youtu.be/5iSlfF8TQ9k?si=1m_8HsjRXekW7w2S"),
        ],
        "팝 🎧": [
            ("Adele - Easy On Me", "https://youtu.be/X-yIEMduRXk?si=n-11JO8PcCDZ1RQK"),
            ("Sam Smith - Too Good at Goodbyes", "https://youtu.be/J_ub7Etch2U?si=d3n5tdISCewt9lHk"),
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
            ("키드밀리 - 25", "https://youtu.be/ARAdXfIWDWU?si=IG6-g6czSw9qY1Iz"),
            ("이센스 - Gas", "https://youtu.be/Gj-pHxO2K4Y?si=Kg_lgB2SgeIXT2yK"),
            ("나플라 - Wu", "https://youtu.be/TZquZFXS9Zk?si=fU3aOV0X3wl6371i"),
            ("김하온 - 꼴통","https://youtu.be/9QMaUl26Qzk?si=t3KlFyxJS60IKXFx"),
        ],
        "한국 발라드 🎶": [
            ("김필 - 다시 사랑한다면", "https://youtu.be/YyKSZARBcGo?si=MEaACPouwv-y8zIF"),
            ("윤하 - 사건의 지평선", "https://youtu.be/BBdC1rl5sKY?si=HRvOrTUdtH43dfHF"),
        ],
        "팝 🎧": [
            ("Eminem - Lose Yourself", "https://youtu.be/xFYQQPAOz7Y?si=5DnRvsBAwAGJXWh-"),
            ("Imagine Dragons - Believer", "https://youtu.be/7wtfhZwyrcc?si=B6W6ZPcEV5fjHlS0"),
        ],
        "인디 🌿": [
            ("검정치마 - EVERYTHING", "https://youtu.be/Aq_gsctWHtQ?si=Ct0sSIA5qhpJnUKd"),
            ("새소년 - 난춘", "https://youtu.be/KsznX5j2oQ0?si=ZpZ6KS_V4vQz2ZwT"),
        ],
    },
    "외로움 🥺": {
        "한국 힙합 🔥": [
            ("비프리 - INDO", "https://youtu.be/jFwo4fJ3NKk?si=C9Tcs0Ta04eu_GAC"),
            ("boycold - Trail", "https://youtu.be/e0Pmr2cFOQc?si=w7o64a41ZNP3rmaR"),
            ("양홍원- SAHARA", "https://youtu.be/Na3NTn9KQ4Y?si=nzj_WDcozuZzPRM1"),
            ("노엘 - 영원히", "https://youtu.be/Qpvg00jJqQk?si=aHOBqIx5egb8TIQ5"),
        ],
        "한국 발라드 🎶": [
            ("정승환 - 너였다면", "https://youtu.be/7L3F9EEvidE?si=xQOVr4Tyge0TY_Hf"),
            ("아이유 - 밤편지", "https://youtu.be/BzYnNdJhZQw?si=q5YVCrNiUYoUZMlS"),
        ],
        "팝 🎧": [
            ("Coldplay - Fix You", "https://youtu.be/k4V3Mo61fJM?si=Jz1K6za6mNR8nJTz"),
            ("Ed Sheeran - Photograph", "https://youtu.be/nSDgHBxUbVQ?si=h5iM2nOAdXg4lZzp"),
        ],
        "인디 🌿": [
            ("잔나비 - 주저하는 연인들을 위해", "https://youtu.be/GpQ222I1ULc?si=1daFmny9sRNbyoLN"),
            ("카더가든 - 명동콜링", "https://youtu.be/wPpbuE1bjsY?si=Hd7bCB3HqSuEFuRU"),
            ("볼빨간사춘기 - blue", "https://youtu.be/t1yHpqup87M?si=MZrONgQ74krv2KKW"),
            ("나의 노래 메모장 - coffee", "https://youtu.be/1H0kSoG6htU?si=4RcAI9SY75ULbZ5A"),
            ("결 - 사랑 없이 사는게 왜 그렇게 어려울까요", "https://youtu.be/_XFuXLliXlY?si=WNt5ggiwmL5HJDlq"),
        ],
    },
    "힐링 🌿": {
        "한국 힙합 🔥": [
            ("염따 - IE러니", "https://youtu.be/VFA2hMu4cpU?si=p_O1Vm1w4eMiuKDY"),
            ("빈지노 - Always Awake", "https://youtu.be/nOZEth-6mrc?si=maYRl7kkyOfbbvzQ"),
            ("빈지노 - Aqua man", "https://youtu.be/08h8u8Z9iJQ?si=ODx61xgvn1WLBKMK"),
            ("빈지노 - 아까워", "https://youtu.be/ppudgIu2TaM?si=ZBZ-gS3ZrGuZrPDW"),
        ],
        "한국 발라드 🎶": [
            ("로이킴 - 봄봄봄", "https://youtu.be/k3-BDy55tq4?si=kgsq9O5nqkGUjWtb"),
            ("폴킴 - 초록빛", "https://youtu.be/xWL29QHZ_mA?si=DANglhuwzG7Aj-NV"),
        ],
        "팝 🎧": [
            ("Lauv - Paris in the Rain", "https://youtu.be/kOCkne-Bku4?si=fBdQOa__UVrQtLUC"),
            ("Daniel Caesar - Best Part", "https://youtu.be/vBy7FaapGRo?si=DNpJhgGozswYy_dR"),
        ],
        "인디 🌿": [
            ("검정치마 - 기다린 만큼, 더", "https://youtu.be/uG2se-8-BzE?si=D0fx2b2XvGLiEdUn"),
            ("데이식스 - 한 페이지가 될 수 있게", "https://youtu.be/vnS_jn2uibs?si=IxKF2YiVppfT5CTI"),
            ("한로로 - 사랑하게 될 거야", "https://youtu.be/h0KIWaUEIgQ?si=1qeNghJlZEgd8hYl"),
            ("너드 커넥션 - 좋은 잠 좋은 꿈", "https://youtu.be/g-rZeTNIw7E?si=kwlR-va5cD6nomkJ"),
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
opinion = st.text_area("특정한 감정을 느꼈을 때 듣고싶은 노래와 그 특정한 감정을 적어주세요:", height=150, placeholder="여기에 작성하세요...")

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












