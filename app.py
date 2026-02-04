import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="Dermalyze AI", layout="wide", page_icon="🔬")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    if os.path.exists("skincare_data.csv"):
        df = pd.read_csv("skincare_data.csv")
        # Column names ko standardize karna (lowercase + no spaces)
        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
        return df
    return None

df = load_data()

# --- SIDEBAR: USER AUTH & DATA GATHERING ---
with st.sidebar:
    st.title("🔐 User Access")
    u_name = st.text_input("Name")
    u_email = st.text_input("Email")
    u_health = st.radio("Stomach/Internal Health", ["Healthy", "Occasional Bloating", "Frequent Acidity/Acne"])
    
    st.divider()
    if st.button("Download My History (CSV)"):
        if os.path.exists("user_data_logs.csv"):
            with open("user_data_logs.csv", "rb") as f:
                st.download_button("Click to Download Excel", f, "my_data.csv")
        else:
            st.warning("No logs found yet.")

# --- MAIN INTERFACE ---
st.title("🔬 Dermalyze: AI Recommendation Engine")

if not u_name or not u_email:
    st.warning("👈 Please enter your Name and Email in the sidebar to start.")
else:
    st.write(f"Logged in as: **{u_name}**")

    # Camera Input
    img_file = st.camera_input("Scan your skin profile")

    if img_file:
        # 1. LOGIC: Skin Type Calculation
        detected_type = "Sensitive/Oily" if u_health != "Healthy" else "Normal/Dry"
        
        # 2. SAVE TO EXCEL LOG (Data Persistence)
        log_file = "user_data_logs.csv"
        log_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"), u_name, u_email, detected_type, u_health]], 
                                columns=["Timestamp", "Name", "Email", "Analysis", "Internal_Health"])
        log_entry.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)
        
        # 3. DISPLAY RESULTS
        st.subheader(f"Analysis Report for {u_name}")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Detected Skin Category: **{detected_type}**")
        with col2:
            st.success(f"Internal Health Factor: **{u_health}**")
        
        # 4. RECOMMENDATION ENGINE
        if df is not None:
            st.divider()
            st.write("### 🧪 Chemical-Matched Recommendations")
            
            # Sahi column dhundna (dataset ke hisab se)
            search_col = None
            for col in ['label', 'skin_type', 'category', 'type']:
                if col in df.columns:
                    search_col = col
                    break
            
            if search_col:
                # 'Oily' ya 'Normal' keyword se search karna
                keyword = "Oily" if "Oily" in detected_type else "Dry"
                recs = df[df[search_col].str.contains(keyword, case=False, na=False)].head(6)
                
                if not recs.empty:
                    # Products ko grid mein dikhana
                    cols = st.columns(3)
                    for i, (idx, row) in enumerate(recs.iterrows()):
                        with cols[i % 3]:
                            # Column names handle karna (name/product_name)
                            p_name = row.get('name', row.get('product_name', 'Skincare Product'))
                            p_brand = row.get('brand', row.get('product_brand', 'Premium Brand'))
                            
                            st.markdown(f"""
                            <div style="border:1px solid #ddd; border-radius:10px; padding:10px; background-color:#f9f9f9; height:150px">
                                <strong>{p_name}</strong><br>
                                <small>Brand: {p_brand}</small><br><br>
                                <a href="https://www.google.com/search?q={p_name.replace(' ', '+')}" target="_blank" style="text-decoration:none; color:white; background-color:#ff4b4b; padding:5px 10px; border-radius:5px;">Check Price</a>
                            </div>
                            """, unsafe_allow_stdio=True, unsafe_allow_html=True)
                else:
                    st.warning("Aapke skin type ke liye match nahi mila.")
            else:
                st.error("Dataset check: Column 'label' ya 'skin_type' nahi mila!")
        else:
            st.error("Error: 'skincare_data.csv' file nahi mili. Please GitHub pe upload karein.")
