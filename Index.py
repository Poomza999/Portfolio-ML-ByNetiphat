import streamlit as st

# ตั้งค่าหน้าเว็บให้แสดงผลแบบกว้าง
st.set_page_config(page_title="ML Web Model Portfolio", layout="wide", initial_sidebar_state="expanded")

# ---------------------------------------------------------
# กำหนดข้อมูลผู้พัฒนา
# ---------------------------------------------------------
developer_name = "นายเนติภัทร์ ใจเด็ด"
student_id = "664245020"
section = "66/43"

# ==========================================
# ส่วนของการตกแต่งด้วย CSS (Custom Styling)
# ==========================================
st.markdown("""
    <style>
        /* ปรับแต่งปุ่มของ Streamlit ให้ดูทันสมัยขึ้น */
        div.stButton > button {
            background: linear-gradient(135deg, #00C6FF, #0072FF);
            color: white;
            border: none;
            border-radius: 30px;
            padding: 10px 24px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 114, 255, 0.3);
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 114, 255, 0.5);
            color: #ffffff;
            border: none;
        }
        
        /* ซ่อนเส้นคั่น default บางส่วนเพื่อให้ UI ดูสะอาด */
        hr {
            margin-top: 1em;
            margin-bottom: 2em;
            border: 0;
            border-top: 1px solid rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# แถบด้านข้าง (Sidebar) แบบ Clean Design
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://cdn-icons-png.flaticon.com/512/4140/4140037.png" width="100" style="border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 15px;">
            <h2 style="margin: 0; color: #1E293B; font-size: 1.5rem;">ผู้พัฒนา</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 10px; border-left: 4px solid #0072FF; margin-bottom: 20px;">
            <p style="margin: 0; color: #475569; font-size: 0.9rem;"><b>ชื่อ:</b> {developer_name}</p>
            <p style="margin: 0; color: #475569; font-size: 0.9rem;"><b>รหัส:</b> {student_id}</p>
            <p style="margin: 0; color: #475569; font-size: 0.9rem;"><b>หมู่เรียน:</b> {section}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.button("🎯 ML Portfolio", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("📈 **Portfolio Progress**")
    st.progress(100)
    st.markdown("<div style='text-align: right; font-size: 0.8rem; color: #64748B;'>6 / 6 Models Deployed</div>", unsafe_allow_html=True)

# ==========================================
# หน้าหลัก (Main Content)
# ==========================================

# Hero Banner แบบ Modern Gradient
banner_html = f"""
<div style="background: linear-gradient(120deg, #1E293B, #0F172A); padding: 50px 30px; border-radius: 20px; color: white; margin-bottom: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); position: relative; overflow: hidden;">
    <div style="position: relative; z-index: 2;">
        <p style="color: #38BDF8; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 5px; text-transform: uppercase;">Machine Learning Portfolio</p>
        <h1 style="color: white; margin-top: 0; margin-bottom: 20px; font-size: 2.5rem;">Interactive Web Models</h1>
        <div style="display: flex; gap: 15px; align-items: center; background: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 50px; width: fit-content; backdrop-filter: blur(10px);">
            <span style="font-size: 1.2rem;">👨‍💻</span>
            <span style="font-size: 1rem; color: #E2E8F0;">พัฒนาโดย <b>{developer_name}</b> ({student_id})</span>
        </div>
    </div>
    <!-- ตกแต่งพื้นหลัง Banner -->
    <div style="position: absolute; right: -50px; top: -50px; width: 200px; height: 200px; background: rgba(56, 189, 248, 0.2); border-radius: 50%; filter: blur(40px); z-index: 1;"></div>
</div>
"""
st.markdown(banner_html, unsafe_allow_html=True)

st.markdown("### 🚀 Explore Applications")
st.markdown("<p style='color: #64748B; margin-bottom: 30px;'>เลือกทดลองใช้งานโมเดล Machine Learning ทั้ง 6 รูปแบบด้านล่าง</p>", unsafe_allow_html=True)

# ฟังก์ชันสำหรับสร้าง Card โมเดล
def create_model_card(col, icon, title, description, accent_color):
    with col:
        # ใช้ HTML/CSS สร้าง Card เพื่อให้ปรับแต่งได้สวยงามกว่า st.container ธรรมดา
        html_card = f"""
        <div style="background-color: white; border-radius: 15px; padding: 25px; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid {accent_color}; 
                    margin-bottom: 15px; height: 160px; transition: transform 0.3s ease;">
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                <div style="background-color: {accent_color}20; padding: 10px; border-radius: 12px; font-size: 1.5rem;">
                    {icon}
                </div>
                <h4 style="margin: 0; color: #1E293B; font-size: 1.1rem;">{title}</h4>
            </div>
            <p style="color: #64748B; font-size: 0.9rem; margin: 0; line-height: 1.5;">{description}</p>
        </div>
        """
        st.markdown(html_card, unsafe_allow_html=True)
        st.button(f"เปิดใช้งานโมเดล", key=title, use_container_width=True)
        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# Grid Layout สำหรับการ์ด
col1, col2, col3 = st.columns(3)

# แถวที่ 1
create_model_card(col1, "🧮", "K-Nearest Neighbor", "Classification using KNN algorithm.", "#3B82F6") # สีน้ำเงิน
create_model_card(col2, "🌳", "Decision Tree", "Classification using Decision Tree algorithm.", "#10B981") # สีเขียว
create_model_card(col3, "⚡", "Support Vector Machine", "Classification using SVM algorithm.", "#F59E0B") # สีส้ม

# แถวที่ 2
create_model_card(col1, "🌀", "K-Means Clustering", "Unsupervised clustering using K-Means.", "#8B5CF6") # สีม่วง
create_model_card(col2, "📈", "Regression", "Regression prediction model for continuous data.", "#EF4444") # สีแดง
create_model_card(col3, "🌲", "Random Forest", "Ensemble classification using Random Forest.", "#06B6D4") # สีฟ้าอมเขียว