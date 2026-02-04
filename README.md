#  Dermalyze AI: Multimodal Diagnostic & Recommendation Engine

Dermalyze AI is a cutting-edge web application designed to personalize skincare routines by fusing **Computer Vision** with **Heuristic Health Data**. Instead of generic recommendations, it analyzes the user's skin profile alongside internal health indicators (like digestion and lifestyle) to suggest chemical-accurate products.



# Key Technical Features
- **Multimodal Data Fusion:** Combines unstructured image data (Camera Scan) with structured user input (Health Survey).
- **Big Data Processing:** Efficiently filters through a dataset of 10,000+ products in real-time.
- **Automated Data Logging:** Implements a persistent data-logging system that records user diagnostics into a CSV/Excel database for future analytics.
- **Responsive UI:** Built with a mobile-first approach using Streamlit for seamless browser execution.

#Tech Stack
- **Language:** Python 3.10+
- **Framework:** Streamlit (Web UI)
- **Data Handling:** Pandas, NumPy
- **Image Processing:** Pillow (PIL)
- **Database:** Flat-file CSV (User History Tracking)

#How It Works
1. **User Authentication:** User enters credentials and internal health status.
2. **Biometric Scan:** The system captures a real-time skin snapshot.
3. **Logic Engine:** A weighted algorithm determines the skin category by correlating health issues with visual cues.
4. **Recommendation:** The engine queries a massive skincare dataset to find products with matching chemical ingredients.
5. **Excel Logging:** Every session is saved in `user_data_logs.csv` for backend tracking.

#Installation & Usage
1. Clone the repo: `git clone https://github.com/your-username/Dermalyze-AI.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

---
*Developed for Internship/Placement Portfolio to demonstrate Full-Stack AI capabilities.*
