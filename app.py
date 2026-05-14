from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
IMAGE_DIR = BASE_DIR / "images"

st.set_page_config(
    page_title="티니핑 도감",
    page_icon="🩷",
    layout="wide"
)

def load_data():
    csv_path = DATA_DIR / "teenieping_data.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return pd.DataFrame(columns=[
        "name", "feature", "description", "season", "category", "image", "source", "memo", "status"
    ])

def resolve_image_path(image_value: str):
    if not image_value or str(image_value).strip() == "":
        placeholder = IMAGE_DIR / "placeholder.png"
        return str(placeholder) if placeholder.exists() else None

    image_path = BASE_DIR / str(image_value)
    if image_path.exists():
        return str(image_path)

    image_path = IMAGE_DIR / str(image_value)
    if image_path.exists():
        return str(image_path)

    placeholder = IMAGE_DIR / "placeholder.png"
    return str(placeholder) if placeholder.exists() else None

def inject_css():
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(180deg, #fff8fc 0%, #fffdfd 100%);
    }

    .title-box {
        background: linear-gradient(135deg, #ffb6d9, #ffd9ec);
        padding: 1.2rem 1rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 8px 20px rgba(255, 182, 217, 0.25);
    }

    .title-text {
        font-size: 2rem;
        font-weight: 800;
        color: #7a2c52;
        margin: 0;
    }

    .subtitle-text {
        font-size: 1rem;
        color: #8b4b6b;
        margin-top: 0.4rem;
    }

    .card {
        background: white;
        border-radius: 22px;
        padding: 1rem;
        box-shadow: 0 8px 24px rgba(255, 182, 217, 0.18);
        border: 2px solid #ffe3f1;
        margin-bottom: 1rem;
    }

    .ping-name {
        font-size: 1.35rem;
        font-weight: 800;
        color: #d63384;
        margin-top: 0.6rem;
        margin-bottom: 0.3rem;
    }

    .badge {
        display: inline-block;
        background: #ffe8f3;
        color: #a61e63;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        font-size: 0.85rem;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
    }

    .feature-box {
        background: #fff4fa;
        border-radius: 14px;
        padding: 0.7rem 0.8rem;
        color: #7a2c52;
        font-size: 0.98rem;
        margin-top: 0.6rem;
    }

    .footer-note {
        color: #9a6b84;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div class="title-box">
        <p class="title-text">🩷 티니핑 도감 🩷</p>
        <p class="subtitle-text">사진과 특징으로 티니핑 친구들을 찾아보세요!</p>
    </div>
    """, unsafe_allow_html=True)

def render_filters(df):
    st.sidebar.header("🔎 검색 / 필터")

    search = st.sidebar.text_input("이름 검색", placeholder="예: 하츄핑")

    seasons = ["전체"] + sorted([x for x in df["season"].dropna().unique().tolist() if str(x).strip() != ""]) if "season" in df.columns else ["전체"]
    categories = ["전체"] + sorted([x for x in df["category"].dropna().unique().tolist() if str(x).strip() != ""]) if "category" in df.columns else ["전체"]

    selected_season = st.sidebar.selectbox("시즌", seasons)
    selected_category = st.sidebar.selectbox("분류", categories)

    return search, selected_season, selected_category

def filter_data(df, search, selected_season, selected_category):
    filtered = df.copy()

    if search.strip():
        filtered = filtered[filtered["name"].astype(str).str.contains(search, case=False, na=False)]

    if selected_season != "전체" and "season" in filtered.columns:
        filtered = filtered[filtered["season"] == selected_season]

    if selected_category != "전체" and "category" in filtered.columns:
        filtered = filtered[filtered["category"] == selected_category]

    return filtered

def render_card(item):
    image_path = resolve_image_path(str(item.get("image", "")))

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if image_path:
            st.image(image_path, use_container_width=True)

        st.markdown(f'<div class="ping-name">{item.get("name", "이름 없음")}</div>', unsafe_allow_html=True)

        season = item.get("season", "")
        category = item.get("category", "")

        badge_html = ""
        if pd.notna(season) and str(season).strip():
            badge_html += f'<span class="badge">시즌: {season}</span>'
        if pd.notna(category) and str(category).strip():
            badge_html += f'<span class="badge">분류: {category}</span>'

        if badge_html:
            st.markdown(badge_html, unsafe_allow_html=True)

        feature = item.get("feature", "")
        if pd.notna(feature) and str(feature).strip():
            st.markdown(f'<div class="feature-box"><b>특징</b><br>{feature}</div>', unsafe_allow_html=True)

        description = item.get("description", "")
        if pd.notna(description) and str(description).strip():
            with st.expander("자세히 보기"):
                st.write(description)

        st.markdown('</div>', unsafe_allow_html=True)

def main():
    inject_css()
    render_header()

    df = load_data()

    if df.empty:
        st.warning("데이터 파일이 비어 있어요. data/teenieping_data.csv 파일을 채워주세요.")
        return

    required_columns = ["name", "feature", "description", "season", "category", "image", "source", "memo", "status"]
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""

    search, selected_season, selected_category = render_filters(df)
    filtered = filter_data(df, search, selected_season, selected_category)

    st.write(f"총 **{len(filtered)}명**의 티니핑을 찾았어요!")

    if len(filtered) == 0:
        st.info("검색 결과가 없어요. 다른 이름이나 필터를 선택해보세요.")
        return

    cols = st.columns(3)
    for idx, (_, row) in enumerate(filtered.iterrows()):
        with cols[idx % 3]:
            render_card(row)

    st.markdown('<div class="footer-note">우리 아이와 함께 보는 사랑스러운 티니핑 도감 ✨</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
