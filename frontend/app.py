import io
import os
import requests
import streamlit as st


st.set_page_config(page_title="Code Review Assistant", layout="wide")
st.title("Code Review Assistant")

backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


with st.sidebar:
    st.markdown("**Backend**")
    backend_url = st.text_input("API base URL", backend_url)


tab_upload, tab_history = st.tabs(["Upload & Review", "History"]) 

with tab_upload:
    st.subheader("Upload a file or paste code")
    uploaded = st.file_uploader("Choose a code file", type=None)
    filename = st.text_input("Filename (optional)")
    language = st.text_input("Language (optional)")
    code = st.text_area("Or paste code here", height=240)

    if st.button("Run Review", type="primary"):
        files = None
        data = {"filename": filename, "language": language}
        if uploaded is not None:
            files = {"file": (uploaded.name, uploaded.getvalue())}
        else:
            data["content"] = code

        try:
            resp = requests.post(f"{backend_url}/api/review", data=data, files=files, timeout=120)
            if resp.status_code == 200:
                review = resp.json()
                st.success("Review generated")
                st.markdown("### Report")
                st.markdown(review.get("report", ""))
            else:
                st.error(f"Error: {resp.status_code} - {resp.text}")
        except Exception as e:
            st.error(str(e))

with tab_history:
    st.subheader("Recent Reviews")
    if st.button("Refresh"):
        pass

    try:
        r = requests.get(f"{backend_url}/api/reviews", timeout=30)
        if r.status_code == 200:
            items = r.json()
            for item in items:
                with st.expander(f"{item['id']}: {item['filename']} ({item.get('language') or 'n/a'})"):
                    st.markdown("**Created**: " + item.get("created_at", ""))
                    st.markdown("**Report:**")
                    st.markdown(item.get("report", ""))
                    with st.popover("View code"):
                        st.code(item.get("content", ""))
        else:
            st.error(f"Error: {r.status_code} - {r.text}")
    except Exception as e:
        st.error(str(e))


