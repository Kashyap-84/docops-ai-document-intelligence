import requests
import streamlit as st

API_URL = "http://localhost:8000/api/v1/extract"

st.set_page_config(page_title="DocOps AI", layout="wide")
st.title("DocOps AI: Document Intelligence MVP")
st.write("Upload a receipt or scanned document image to extract structured fields.")

uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "tiff", "bmp"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded document", use_container_width=True)

    if st.button("Extract Fields"):
        with st.spinner("Running OCR and extraction..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(API_URL, files=files, timeout=120)

        if response.status_code == 200:
            result = response.json()
            left, right = st.columns(2)
            with left:
                st.subheader("Structured Output")
                st.json({k: v for k, v in result.items() if k != "raw_text"})
            with right:
                st.subheader("Raw OCR Text")
                st.text_area("OCR Output", result.get("raw_text", ""), height=420)
        else:
            st.error(response.text)
