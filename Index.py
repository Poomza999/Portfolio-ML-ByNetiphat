import streamlit as st
import base64
import os
import pickle
import yfinance as yf
import pandas as pd

# ตั้งค่าหน้าเว็บให้แสดงผลแบบกว้าง
st.set_page_config(page_title="ML Web Model Portfolio", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# ฟังก์ชันสำหรับแปลงไฟล์รูปภาพเป็น Base64
# ==========================================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

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
    # จัดการรูปโปรไฟล์ด้วย Base64
    image_path = "Image/dev.png" # แนะนำให้ใช้ Forward Slash (/) ใน Python
    
    try:
        # ถ้าเจอไฟล์รูปภาพ ให้แปลงเป็น base64
        img_base64 = get_base64_of_bin_file(image_path)
        img_src = f"data:image/png;base64,{img_base64}"
    except FileNotFoundError:
        # ถ้าไม่เจอไฟล์รูปภาพ ให้ใช้รูป Default ไปก่อน
        img_src = "https://cdn-icons-png.flaticon.com/512/4140/4140037.png"
        st.error(f"⚠️ ไม่พบไฟล์รูปภาพที่: {image_path} ระบบจึงใช้รูปสำรอง")

    # โปรไฟล์
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="{img_src}" width="90" style="border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 10px;">
            <h3 style="margin: 0; font-size: 2rem; color: #00FF00;"><b style="color: #2CFF05;">Developer</b></h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="background-color: #F8FAFC; padding: 15px; border-radius: 10px; border-left: 4px solid #0072FF; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 0.9rem; color: #475569;"><b style="color: #1E293B;">ชื่อ:</b> {developer_name}</p>
            <p style="margin: 0; font-size: 0.9rem; color: #475569;"><b style="color: #1E293B;">รหัส:</b> {student_id}</p>
            <p style="margin: 0; font-size: 0.9rem; color: #475569;"><b style="color: #1E293B;">หมู่เรียน:</b> {section}</p>
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
    
    st.markdown("### 📥 1. ป้อนข้อมูลขนาดดอกไม้ (เซนติเมตร)")
    
    # สร้างช่องกรอกข้อมูล 4 ช่องตาม Dataset ของ Iris
    col1, col2 = st.columns(2)
    with col1:
        sepal_length = st.number_input("ความยาวกลีบเลี้ยง (Sepal Length)", min_value=0.0, value=5.1)
        petal_length = st.number_input("ความยาวกลีบดอก (Petal Length)", min_value=0.0, value=1.4)
    with col2:
        sepal_width = st.number_input("ความกว้างกลีบเลี้ยง (Sepal Width)", min_value=0.0, value=3.5)
        petal_width = st.number_input("ความกว้างกลีบดอก (Petal Width)", min_value=0.0, value=0.2)
        
    st.markdown("---")
    
    # ปุ่มกดเพื่อทำนาย
    if st.button("🚀 ทำนายสายพันธุ์ (Predict)", use_container_width=True):
        try:
            # 1. โหลดไฟล์โมเดลที่เราเทรนไว้
            with open('knn_model.pkl', 'rb') as file:
                model = pickle.load(file)
            
            # 2. นำข้อมูลที่ผู้ใช้กรอก ไปเข้าโมเดล
            input_data = [[sepal_length, sepal_width, petal_length, petal_width]]
            prediction = model.predict(input_data)
            
            # 3. แปลงผลลัพธ์จากตัวเลข (0,1,2) เป็นชื่อสายพันธุ์
            species = ['Setosa (เซโตซา)', 'Versicolor (เวอร์ซิคัลเลอร์)', 'Virginica (เวอร์จินิกา)']
            result = species[prediction[0]]
            
            # 4. แสดงผลลัพธ์บนหน้าเว็บ
            st.success("ประมวลผลสำเร็จ!")
            st.markdown(f"<h3 style='text-align: center; color: #10B981;'>🌸 ผลการทำนาย: ดอกไอริสสายพันธุ์ {result}</h3>", unsafe_allow_html=True)
            
        except FileNotFoundError:
            st.error("⚠️ ไม่พบไฟล์ 'knn_model.pkl' กรุณารันโค้ด Train โมเดลก่อนครับ")

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
    st.markdown("### 📊 1. ระบุหุ้นที่ต้องการวิเคราะห์")
    
    # ให้ผู้ใช้กรอกชื่อหุ้น
    ticker_input = st.text_input("กรอกสัญลักษณ์หุ้น (เช่น AAPL, TSLA หรือ PTT.BK สำหรับหุ้นไทย)", value="AAPL")
    
    st.markdown("---")
    
    if st.button("🚀 ดึงข้อมูลล่าสุด & วิเคราะห์แนวโน้ม", use_container_width=True):
        try:
            with st.spinner(f'กำลังดึงข้อมูลหุ้น {ticker_input} จากตลาดหลักทรัพย์...'):
                # 1. โหลดสมอง AI
                with open('stock_model.pkl', 'rb') as file:
                    model = pickle.load(file)
                
                # 2. ดึงข้อมูลหุ้นตัวนั้นย้อนหลัง 60 วัน 
                ticker_data = yf.download(ticker_input, period="60d")
                
                if ticker_data.empty:
                    st.error("❌ ไม่พบข้อมูลหุ้นนี้ กรุณาตรวจสอบสัญลักษณ์ให้ถูกต้อง")
                else:
                    # 3. คำนวณอินดิเคเตอร์
                    ticker_data['SMA_10'] = ticker_data['Close'].rolling(window=10).mean()
                    ticker_data['SMA_30'] = ticker_data['Close'].rolling(window=30).mean()
                    ticker_data['Volume_Change'] = ticker_data['Volume'].pct_change()
                    
                    # 4. ดึงข้อมูลวันล่าสุด
                    latest_data = ticker_data.iloc[-1]
                    latest_close = float(latest_data['Close'].iloc[0]) if isinstance(latest_data['Close'], pd.Series) else float(latest_data['Close'])
                    
                    input_features = [[
                        float(latest_data['Close']), 
                        float(latest_data['SMA_10']), 
                        float(latest_data['SMA_30']), 
                        float(latest_data['Volume_Change'])
                    ]]
                    
                    # 5. ทำนายผล
                    prediction = model.predict(input_features)
                    
                    # 6. แสดงผลลัพธ์
                    st.success(f"วิเคราะห์ข้อมูลหุ้น {ticker_input} สำเร็จ!")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("ราคาปิดล่าสุด", f"{latest_close:.2f}")
                    col2.metric("SMA 10 วัน", f"{float(latest_data['SMA_10']):.2f}")
                    col3.metric("SMA 30 วัน", f"{float(latest_data['SMA_30']):.2f}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if prediction[0] == 1:
                        st.markdown("<div style='background-color: #d1fae5; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981;'><h2 style='text-align: center; color: #047857; margin: 0;'>🟢 สัญญาณ: แนะนำให้ซื้อ (Buy)</h2><p style='text-align: center; color: #065f46; margin-top: 10px;'>โมเดลคาดการณ์ว่าแนวโน้มราคาในวันทำการถัดไปจะเป็นขาขึ้น</p></div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='background-color: #fee2e2; padding: 20px; border-radius: 10px; border-left: 5px solid #EF4444;'><h2 style='text-align: center; color: #b91c1c; margin: 0;'>🔴 สัญญาณ: แนะนำให้ขาย / รอดูสถานการณ์</h2><p style='text-align: center; color: #991b1b; margin-top: 10px;'>โมเดลคาดการณ์ว่าแนวโน้มราคาในวันทำการถัดไปจะปรับตัวลง</p></div>", unsafe_allow_html=True)

        except FileNotFoundError:
            st.error("⚠️ ไม่พบไฟล์ 'stock_model.pkl' กรุณาตรวจสอบให้แน่ใจว่าได้นำไฟล์มาใส่ในโฟลเดอร์เดียวกับโค้ดแล้ว")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")