import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Backlink Status Checker", layout="wide")

st.title("🔗 Backlink Status Checker (Live & 404 Monitor)")

# Input form
with st.form("backlink_form"):
    st.write("### Enter your target website and backlink URLs")
    target_domain = st.text_input("Your website (e.g. getprolinks.com)", "getprolinks.com")
    backlink_input = st.text_area("Paste backlinks (one URL per line)", height=200)
    submitted = st.form_submit_button("Check Backlink Status")

if submitted:
    urls = [url.strip() for url in backlink_input.splitlines() if url.strip()]
    results = []

    progress = st.progress(0)
    for i, url in enumerate(urls):
        status = ""
        contains_link = "N/A"

        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            status = response.status_code

            if status == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                if target_domain.lower() in response.text.lower():
                    contains_link = "✅ Yes"
                else:
                    contains_link = "❌ No"
            else:
                contains_link = "❌ Page error"
        except Exception as e:
            status = "⚠️ Error"
            contains_link = str(e)

        results.append({
            "Backlink URL": url,
            "Status Code": status,
            "Link Present": contains_link
        })

        progress.progress((i + 1) / len(urls))

    df = pd.DataFrame(results)
    st.success("✅ Completed! Here's the backlink status report:")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name="backlink_status_report.csv", mime='text/csv')
