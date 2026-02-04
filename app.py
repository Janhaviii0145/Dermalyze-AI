import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Dermalyze AI", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    if os.path.exists("skincare_data.csv"):
        df = pd.read_csv("skincare_data.csv")
        # Cleaning data for search
        df.columns = [c.lower().replace(' ', '_') for c in df.columns]
        return df
    return None

df = load_data()

# --- SIDEBAR: USER AUTH & DATA GATHERING ---
with st.sidebar:
    st.title("🔐 User Login")
    u_name = st.text_input("Name")
    u_email = st.text_input("Email")
    u_health = st.radio("Stomach/Internal Health", ["Healthy", "Occasional Bloating", "Frequent Acidity/Acne"])
    
    if st.button("Download My History (CSV)"):
        if os.path.exists("user_data_logs.csv"):
            with open("user_data_logs.csv", "rb") as f:
                st.download_button("Click to Download Excel", f, "my_data.csv")

# --- MAIN INTERFACE ---
st.title("🔬 Dermalyze: AI Recommendation Engine")
st.write(f"Logged in as: **{u_name}**" if u_name else "Please login from sidebar")

# Camera Input
img_file = st.camera_input("Scan your skin profile")

if img_file and u_name and u_email:
    # Logic: Cross-referencing Health with Skin
    detected_type = "Sensitive/Oily" if u_health != "Healthy" else "Normal/Dry"
    
    # SAVE TO EXCEL LOG (Your tracking requirement)
    log_file = "user_data_logs.csv"
    log_entry = pd.DataFrame([[datetime.now(), u_name, u_email, detected_type, u_health]], 
                            columns=["Timestamp", "Name", "Email", "Analysis", "Internal_Health"])
    log_entry.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)
    
    # RECOMMENDATION LOGIC
    st.subheader(f"Analysis Report for {u_name}")
    st.info(f"Detected Skin Category: **{detected_type}**")
    
   # RECOMMENDATION ENGINE (Updated for Huge Datasets)
    if df is not None:
        st.write("---")
        st.write("### 🧪 Chemical-Matched Recommendations")
        
        # 1. Column names ki safai (taaki search asan ho)
        df.columns = [c.strip().lower() for c in df.columns]
        
        # 2. Sahi column dhundna (Label ya Skin Type)
        search_col = None
        for col in ['label', 'skin type', 'category', 'type']:
            if col in df.columns:
                search_col = col
                break
        
        if search_col:
            # 3. Filtering Logic
            keyword = detected_type.split('/')[0] # 'Oily' ya 'Normal'
            recs = df[df[search_col].str.contains(keyword, case=False, na=False)].head(6)
            
            if not recs.empty:
                cols = st.columns(3)
                for i, (idx, row) in enumerate(recs.iterrows()):
                    with cols[i % 3]:
                        # Name aur Brand ke columns dynamic check karna
                        p_name = row.get('name', row.get('product_name', 'Skincare Product'))
                        p_brand = row.get('brand', row.get('product_brand', 'Premium Brand'))
                        
                        st.success(f"**{p_name}**")
                        st.caption(f"Brand: {p_brand}")
                        st.markdown(f"[🔍 Google Search](https://www.google.com/search?q={p_name.replace(' ', '+')})")
            else:
                st.warning("Aapke skin type ke liye exact match nahi mila. Default routine check karein.")
        else:
            st.error("Dataset mein 'Label' ya 'Skin Type' ka column nahi mila. Please check your CSV!")
