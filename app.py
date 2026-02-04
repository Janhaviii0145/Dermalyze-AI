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
            # Cleaning column names (lowercase and no extra spaces)
            df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
            return df
        except Exception as e:
            st.error(f"CSV Error: {e}")
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
    if st.button("Download My History"):
        if os.path.exists("user_data_logs.csv"):
            with open("user_data_logs.csv", "rb") as f:
                st.download_button("Click to Download CSV", f, "my_data.csv")
        else:
            st.warning("No logs found yet.")

# --- MAIN INTERFACE ---
st.title("🔬 Dermalyze: AI Recommendation Engine")

if not u_name or not u_email:
    st.warning("👈 Please enter your details in the sidebar to start the scan.")
else:
    st.write(f"Logged in as: **{u_name}**")
    img_file = st.camera_input("Scan your skin profile")

    if img_file:
        # 1. AI Logic for Skin Category
        # Agar health healthy nahi hai toh 'Oily/Sensitive' recommend karega
        detected_type = "Oily" if u_health != "Healthy" else "Dry"
        
        # 2. Save Session to Excel/CSV Log
        log_file = "user_data_logs.csv"
        log_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), u_name, u_email, detected_type, u_health]], 
                                columns=["Timestamp", "Name", "Email", "Analysis", "Internal_Health"])
        log_entry.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)
        
        # 3. Results Display
        st.subheader(f"Analysis Report for {u_name}")
        st.info(f"Recommended Skin Routine for: **{detected_type} Skin** (based on {u_health} health)")

        # 4. Smart Recommendation Engine
        if df is not None:
            st.divider()
            st.write("### 🧪 Chemical-Matched Recommendations")
            
            # Smartly find the Skin Type column
            search_col = None
            for col in df.columns:
                if any(x in col for x in ['label', 'skin', 'type', 'category']):
                    search_col = col
                    break
            
            if search_col:
                # Filter data
                recs = df[df[search_col].str.contains(detected_type, case=False, na=False)].head(6)
                
                if not recs.empty:
                    cols = st.columns(3)
                    for i, (idx, row) in enumerate(recs.iterrows()):
                        with cols[i % 3]:
                            # Automatically pick Name and Brand columns based on position
                            p_name = row.get('name', row.get('product_name', row.iloc[1] if len(row)>1 else "Product"))
                            p_brand = row.get('brand', row.get('product_brand', row.iloc[0] if len(row)>0 else "Premium"))
                            
                            st.success(f"**{p_name}**")
                            st.caption(f"Brand: {p_brand}")
                            st.markdown(f"[🔍 Check Price](https://www.google.com/search?q={str(p_name).replace(' ', '+')})")
                else:
                    st.warning(f"Note: No specific matches for '{detected_type}' in the current batch. Here are our top general picks:")
                    st.dataframe(df.head(5))
            else:
                st.error("Wait! We couldn't find a 'Skin Type' column in your CSV. Please check the file.")
                st.write("Available columns in your file:", df.columns.tolist())
        else:
            st.error("Error: 'skincare_data.csv' not found. Please upload it to your GitHub.")