import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Dermalyze AI", layout="wide", page_icon="🔬")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    if os.path.exists("skincare_data.csv"):
        try:
            df = pd.read_csv("skincare_data.csv")
            # Standardize column names
            df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
            return df
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return None
    return None

df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔐 User Access")
    u_name = st.text_input("Name")
    u_email = st.text_input("Email")
    u_health = st.radio("Stomach/Internal Health", ["Healthy", "Occasional Bloating", "Frequent Acidity/Acne"])
    
    st.divider()
    if st.button("Download History"):
        if os.path.exists("user_data_logs.csv"):
            with open("user_data_logs.csv", "rb") as f:
                st.download_button("Click to Download", f, "my_data.csv")
        else:
            st.warning("No logs found.")

# --- MAIN INTERFACE ---
st.title("🔬 Dermalyze: AI Recommendation Engine")

if not u_name or not u_email:
    st.warning("👈 Please enter Name and Email in the sidebar.")
else:
    img_file = st.camera_input("Scan your skin profile")

    if img_file:
        # 1. LOGIC
        detected_type = "Oily" if u_health != "Healthy" else "Dry"
        
        # 2. SAVE LOGS
        log_file = "user_data_logs.csv"
        log_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), u_name, u_email, detected_type, u_health]], 
                                columns=["Timestamp", "Name", "Email", "Analysis", "Internal_Health"])
        log_entry.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)
        
        # 3. DISPLAY RESULTS
        st.subheader(f"Analysis Report for {u_name}")
        st.info(f"Detected Skin Category: **{detected_type}**")
        
        # 4. RECOMMENDATIONS
        if df is not None:
            st.divider()
            st.write("### 🧪 Chemical-Matched Recommendations")
            
            # Find the right column
            search_col = None
            for col in ['label', 'skin_type', 'category', 'type']:
                if col in df.columns:
                    search_col = col
                    break
            
            if search_col:
                recs = df[df[search_col].str.contains(detected_type, case=False, na=False)].head(6)
                
                if not recs.empty:
                    cols = st.columns(3)
                    for i, (idx, row) in enumerate(recs.iterrows()):
                        with cols[i % 3]:
                            p_name = row.get('name', row.get('product_name', 'Product'))
                            p_brand = row.get('brand', row.get('product_brand', 'Premium'))
                            
                            # Simple clean display
                            st.success(f"**{p_name}**")
                            st.write(f"Brand: {p_brand}")
                            st.markdown(f"[🔍 Price Check](https://www.google.com/search?q={p_name.replace(' ', '+')})")
                else:
                    st.warning("No direct matches found in dataset.")
            else:
                st.error("Column 'label' not found in CSV.")
        else:
            st.error("skincare_data.csv not found on GitHub!")
