import streamlit as st
import requests

st.set_page_config(page_title="YouTube Viral Predictor")
st.title("📈 YouTube Viral Video Assistant")

with st.form("video_form"):
    title = st.text_input("🎬 Video Title")
    description = st.text_area("📝 Video Description")
    country = st.text_input("🌍 Video Trending Country")
    tags = st.text_input("🏷️ Video Tags (comma-separated)")
    submitted = st.form_submit_button("🔍 Analyze")

if submitted:
    video_data = {
        "video_title": title,
        "video_description": description,
        "video_trending_country": country,
        "video_tags": tags,
    }

    pred_response = requests.post("http://backend:8000/predict-viral/", json=video_data).json()
    gen_response = requests.post("http://backend:8000/generate/", json=video_data).json()

    if "is_viral" in pred_response:
        st.subheader("🧠 Prediction Result")
        st.success("🔥 Viral!" if pred_response["is_viral"] else "❄️ Not Viral")
    else:
        st.error("Prediction failed. Please check the backend logs.")

    st.subheader("🛠️ AI-Generated Content")
    st.markdown(f"**Optimized Title:** {gen_response['new_title']}")
    st.markdown(f"**Optimized Description:** {gen_response['new_description']}")
