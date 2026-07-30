import streamlit as st

# ตั้งค่าหน้าเว็บให้แสดงผลแบบกว้าง
st.set_page_config(page_title="ML Web Model Portfolio", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# จัดการ State สำหรับระบบนำทาง (Navigation)
# ==========================================
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 หน้าหลัก (Home)"

def change_page(page_name):
    st.session_state.current_page = page_name

# ---------------------------------------------------------
# กำหนดข้อมูลผู้พัฒนา
# ---------------------------------------------------------
developer_name = "นายเนติภัทร์ ใจเด็ด"
student_id = "664245020"
section = "66/43"

# ==========================================
# CSS ตกแต่งความสวยงาม
# ==========================================
st.markdown("""
    <style>
        /* ปุ่มของ Streamlit */
        div.stButton > button {
            background: linear-gradient(135deg, #00C6FF, #0072FF);
            color: white;
            border: none;
            border-radius: 30px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 114, 255, 0.3);
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 114, 255, 0.5);
            color: #ffffff;
        }
        
        /* ปุ่มย้อนกลับ (ปุ่มรอง) */
        .btn-secondary > div > button {
            background: #f1f5f9 !important;
            color: #475569 !important;
            box-shadow: none !important;
            border: 1px solid #cbd5e1 !important;
        }
        .btn-secondary > div > button:hover {
            background: #e2e8f0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# แถบด้านข้าง (Sidebar)
# ==========================================
pages = [
    "🏠 หน้าหลัก (Home)",
    "🧮 K-Nearest Neighbor (KNN)",
    "🌳 Decision Tree",
    "⚡ Support Vector Machine (SVM)",
    "🌀 K-Means Clustering",
    "📈 Regression",
    "🌲 Ensemble (Random Forest)"
]

with st.sidebar:
    # โปรไฟล์
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="https://cdn-icons-png.flaticon.com/512/4140/4140037.png" width="90" style="border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 10px;">
            <h3 style="margin: 0; color: #1E293B;">ผู้พัฒนา</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 10px; border-left: 4px solid #0072FF; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 0.9rem;"><b>ชื่อ:</b> {developer_name}</p>
            <p style="margin: 0; font-size: 0.9rem;"><b>รหัส:</b> {student_id}</p>
            <p style="margin: 0; font-size: 0.9rem;"><b>หมู่เรียน:</b> {section}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📌 เมนูนำทาง")
    
    # เมนูเลือกหน้า (เชื่อมกับ session_state)
    selected_page = st.radio("เลือกระบบที่ต้องการ:", pages, key="current_page")
    
    st.markdown("---")
    st.markdown("📈 **ความคืบหน้า**")
    st.progress(100)
    st.markdown("<div style='text-align: right; font-size: 0.8rem; color: #64748B;'>6 / 6 Models Deployed</div>", unsafe_allow_html=True)


# ==========================================
# ฟังก์ชันสร้างหน้าของแต่ละโมเดล (Template)
# ==========================================
def render_model_page(title, icon, description, color):
    st.markdown(f"""
        <div style="background: linear-gradient(120deg, {color}, #0F172A); padding: 40px; border-radius: 15px; color: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
            <h1 style="margin: 0; font-size: 2.5rem;">{icon} {title}</h1>
            <p style="margin-top: 10px; font-size: 1.1rem; opacity: 0.9;">{description}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ปุ่มย้อนกลับไปหน้าหลัก
    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    if st.button("⬅️ กลับหน้าหลัก"):
        change_page("🏠 หน้าหลัก (Home)")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ พื้นที่สำหรับใส่โค้ดโมเดล")
    st.info(f"คุณสามารถนำโค้ดสำหรับโมเดล **{title}** (เช่น การอัปโหลดไฟล์ CSV, การปรับ Hyperparameters, และส่วนของการทำ Prediction) มาใส่ในส่วนนี้ได้เลยครับ")

# ==========================================
# การแสดงผลเนื้อหาหลัก (Main Content Routing)
# ==========================================

if selected_page == "🏠 หน้าหลัก (Home)":
    # Hero Banner
    banner_html = f"""
    <div style="background: linear-gradient(120deg, #1E293B, #0F172A); padding: 40px 30px; border-radius: 20px; color: white; margin-bottom: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.15);">
        <p style="color: #38BDF8; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 5px;">MACHINE LEARNING PORTFOLIO</p>
        <h1 style="color: white; margin-top: 0; margin-bottom: 15px; font-size: 2.2rem;">รวมผลงานแอปพลิเคชัน 6 โมเดล</h1>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)

    st.markdown("### 🚀 Explore Applications")
    
    # Grid Layout สำหรับการ์ด
    col1, col2, col3 = st.columns(3)

    def create_card(col, icon, title, description, accent_color, page_target):
        with col:
            html_card = f"""
            <div style="background-color: white; border-radius: 15px; padding: 25px; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid {accent_color}; 
                        margin-bottom: 15px; height: 160px;">
                <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                    <div style="background-color: {accent_color}20; padding: 10px; border-radius: 12px; font-size: 1.5rem;">{icon}</div>
                    <h4 style="margin: 0; color: #1E293B; font-size: 1.1rem;">{title}</h4>
                </div>
                <p style="color: #64748B; font-size: 0.9rem; margin: 0;">{description}</p>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
            # เมื่อกดปุ่ม จะเรียกฟังก์ชันเปลี่ยนหน้า
            st.button(f"เปิดใช้งานโมเดล", key=f"btn_{title}", use_container_width=True, on_click=change_page, args=(page_target,))
            st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

    # แถวที่ 1
    create_card(col1, "🧮", "K-Nearest Neighbor", "Classification using KNN algorithm.", "#3B82F6", "🧮 K-Nearest Neighbor (KNN)")
    create_card(col2, "🌳", "Decision Tree", "Classification using Decision Tree algorithm.", "#10B981", "🌳 Decision Tree")
    create_card(col3, "⚡", "Support Vector Machine", "Classification using SVM algorithm.", "#F59E0B", "⚡ Support Vector Machine (SVM)")

    # แถวที่ 2
    create_card(col1, "🌀", "K-Means Clustering", "Unsupervised clustering using K-Means.", "#8B5CF6", "🌀 K-Means Clustering")
    create_card(col2, "📈", "Regression", "Regression prediction model for continuous data.", "#EF4444", "📈 Regression")
    create_card(col3, "🌲", "Random Forest", "Ensemble classification using Random Forest.", "#06B6D4", "🌲 Ensemble (Random Forest)")

elif selected_page == "🧮 K-Nearest Neighbor (KNN)":
    render_model_page("K-Nearest Neighbor (KNN)", "🧮", "Classification using the KNN algorithm.", "#3B82F6")

elif selected_page == "🌳 Decision Tree":
    render_model_page("Decision Tree", "🌳", "Classification using Decision Tree algorithm.", "#10B981")

elif selected_page == "⚡ Support Vector Machine (SVM)":
    render_model_page("Support Vector Machine (SVM)", "⚡", "Classification using SVM algorithm.", "#F59E0B")

elif selected_page == "🌀 K-Means Clustering":
    render_model_page("K-Means Clustering", "🌀", "Unsupervised clustering using K-Means.", "#8B5CF6")

elif selected_page == "📈 Regression":
    render_model_page("Regression", "📈", "Regression prediction model for continuous data.", "#EF4444")

elif selected_page == "🌲 Ensemble (Random Forest)":
    render_model_page("Ensemble (Random Forest)", "🌲", "Ensemble classification using Random Forest.", "#06B6D4")