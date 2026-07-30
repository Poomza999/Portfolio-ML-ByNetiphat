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
    
    # ปุ่มย้อนกลับไปหน้าหลัก (แก้ Error ด้วย on_click ที่นี่ครับ!)
    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    st.button("⬅️ กลับหน้าหลัก", on_click=change_page, args=("🏠 หน้าหลัก (Home)",))
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
    render_model_page("K-Nearest Neighbor (KNN)", "🧮", "ระบบประเมินความเสี่ยงและอนุมัติสินเชื่อ (Loan Approval) ด้วย KNN", "#3B82F6")
    
    st.markdown("### 📋 1. กรอกข้อมูลผู้ขอสินเชื่อ")
    
    # สร้างฟอร์มกรอกข้อมูลแบบ 2 คอลัมน์
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("รายได้ต่อเดือน (บาท)", min_value=0, value=35000, step=1000)
        loan_amount = st.number_input("ยอดเงินที่ขอกู้ (บาท)", min_value=0, value=500000, step=10000)
    with col2:
        work_exp = st.number_input("อายุงาน (ปี)", min_value=0, max_value=100, value=3)
        credit_score = st.slider("คะแนนเครดิตบูโร (Credit Score)", min_value=300, max_value=850, value=650)
        st.markdown("<small style='color:gray;'>* 300=แย่มาก, 850=ดีเยี่ยม</small>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # ปุ่มกดเพื่อทำนาย
    if st.button("🚀 ประเมินความเสี่ยงสินเชื่อ", use_container_width=True):
        import pickle
        try:
            with st.spinner('กำลังเปรียบเทียบโปรไฟล์กับฐานข้อมูลลูกค้า...'):
                # เปลี่ยน Path ไปที่ Models/
                with open('Models/knn_loan_model.pkl', 'rb') as file:
                    model = pickle.load(file)
                
                input_data = [[income, loan_amount, work_exp, credit_score]]
                prediction = model.predict(input_data)
                
                st.success("ประมวลผลเสร็จสิ้น!")
                
                st.markdown("### 📊 ผลการประเมินเบื้องต้น")
                if prediction[0] == 1:
                    st.markdown("""
                    <div style='background-color: #d1fae5; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981; text-align: center;'>
                        <h2 style='color: #047857; margin: 0;'>🟢 อนุมัติสินเชื่อ (Approved)</h2>
                        <p style='color: #065f46; margin-top: 10px; font-size: 1.1rem;'>
                            โปรไฟล์มีความน่าเชื่อถือและมีความเสี่ยงต่ำ (ใกล้เคียงกับกลุ่มลูกค้าประวัติดี)
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background-color: #fee2e2; padding: 20px; border-radius: 10px; border-left: 5px solid #EF4444; text-align: center;'>
                        <h2 style='color: #b91c1c; margin: 0;'>🔴 ไม่อนุมัติ / ความเสี่ยงสูง (Rejected)</h2>
                        <p style='color: #991b1b; margin-top: 10px; font-size: 1.1rem;'>
                            โปรไฟล์มีความเสี่ยงสูง (ใกล้เคียงกับกลุ่มลูกค้าหนี้เสีย) แนะนำให้ลดวงเงินกู้หรือเพิ่มเครดิตสกอร์
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
        except FileNotFoundError:
            st.error("⚠️ ไม่พบไฟล์ 'Models/knn_loan_model.pkl' กรุณาตรวจสอบว่าได้สร้างโฟลเดอร์ Models และใส่ไฟล์ไว้แล้ว")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")

elif selected_page == "🌳 Decision Tree":
    render_model_page("Decision Tree", "🌳", "ระบบวิเคราะห์ความเสี่ยงพนักงานลาออก (HR Analytics) ด้วย Decision Tree", "#10B981")
    
    st.markdown("### 📋 1. กรอกข้อมูลโปรไฟล์พนักงาน")
    
    # สร้างฟอร์มกรอกข้อมูลแบบ 2 คอลัมน์
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("อายุพนักงาน (ปี)", min_value=18, max_value=80, value=30)
        income = st.number_input("เงินเดือน (บาท)", min_value=9000, value=30000, step=1000)
    with col2:
        overtime_input = st.selectbox("การทำงานล่วงเวลา (Overtime)", options=["ไม่ทำ (No)", "ทำ (Yes)"])
        satisfaction = st.slider("ระดับความพึงพอใจในงาน (1=แย่สุด, 4=ดีมาก)", min_value=1, max_value=4, value=3)
    
    # แปลงข้อความ Overtime เป็นตัวเลข (1 หรือ 0) เพื่อส่งให้โมเดล
    overtime_val = 1 if overtime_input == "ทำ (Yes)" else 0
        
    st.markdown("---")
    
    # ปุ่มกดเพื่อทำนาย
    if st.button("🚀 ประเมินความเสี่ยงการลาออก", use_container_width=True):
        import pickle
        try:
            with st.spinner('กำลังใช้ Decision Tree วิเคราะห์รูปแบบข้อมูล...'):
                # เปลี่ยน Path ไปที่ Models/
                with open('Models/dt_hr_model.pkl', 'rb') as file:
                    model = pickle.load(file)
                
                input_data = [[age, income, overtime_val, satisfaction]]
                prediction = model.predict(input_data)
                
                st.success("การวิเคราะห์เสร็จสิ้น!")
                
                st.markdown("### 📊 ผลการประเมิน")
                if prediction[0] == 1:
                    st.markdown("""
                    <div style='background-color: #fee2e2; padding: 20px; border-radius: 10px; border-left: 5px solid #EF4444; text-align: center;'>
                        <h2 style='color: #b91c1c; margin: 0;'>🔴 ความเสี่ยงสูง (High Risk of Attrition)</h2>
                        <p style='color: #991b1b; margin-top: 10px; font-size: 1.1rem;'>
                            พนักงานมีแนวโน้มที่จะ <b>ลาออก</b> สูง <br>
                            <i>ข้อแนะนำ HR: ควรเรียกคุยเพื่อสอบถามความพึงพอใจ หรือพิจารณาปรับฐานเงินเดือน/ลดภาระงาน OT</i>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background-color: #d1fae5; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981; text-align: center;'>
                        <h2 style='color: #047857; margin: 0;'>🟢 ความเสี่ยงต่ำ (Low Risk / Retained)</h2>
                        <p style='color: #065f46; margin-top: 10px; font-size: 1.1rem;'>
                            พนักงานมีแนวโน้มที่จะ <b>อยู่กับองค์กรต่อ</b> <br>
                            <i>สถานการณ์ปกติ พนักงานมีความพึงพอใจกับสมดุลการทำงานและรายได้</i>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
        except FileNotFoundError:
            st.error("⚠️ ไม่พบไฟล์ 'Models/dt_hr_model.pkl' กรุณาตรวจสอบว่าได้สร้างโฟลเดอร์ Models และใส่ไฟล์ไว้แล้ว")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")

elif selected_page == "⚡ Support Vector Machine (SVM)":
    render_model_page("Support Vector Machine (SVM)", "⚡", "ระบบประเมินความเสี่ยงและตรวจจับการทุจริตบัตรเครดิต (Fraud Detection)", "#F59E0B")
    
    st.markdown("### 💳 1. ข้อมูลการทำธุรกรรมล่าสุด")
    
    # สร้างฟอร์มกรอกข้อมูลแบบ 2 คอลัมน์
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("ยอดเงินที่ทำรายการ (บาท)", min_value=0.0, value=1500.0, step=500.0)
        distance = st.number_input("ระยะทางจากจุดใช้งานประจำ (กิโลเมตร)", min_value=0.0, value=5.0, step=1.0)
    with col2:
        intl_txn_input = st.selectbox("เป็นการทำรายการจากต่างประเทศหรือไม่?", options=["ไม่ใช่ (Domestic)", "ใช่ (International)"])
        failed_pin = st.number_input("จำนวนครั้งที่ใส่รหัส PIN ผิดก่อนหน้านี้", min_value=0, max_value=5, value=0)
        
    # แปลงข้อความเป็นตัวเลขให้โมเดล
    intl_txn = 1 if intl_txn_input == "ใช่ (International)" else 0
        
    st.markdown("---")
    
    # ปุ่มกดเพื่อทำนาย
    if st.button("🚀 ตรวจสอบความปลอดภัยของธุรกรรม", use_container_width=True):
        import pickle
        try:
            with st.spinner('กำลังใช้เทคโนโลยี SVM ตรวจสอบรูปแบบการทุจริต...'):
                # เปลี่ยน Path ไปที่ Models/
                with open('Models/svm_fraud_model.pkl', 'rb') as file:
                    model = pickle.load(file)
                
                input_data = [[amount, distance, intl_txn, failed_pin]]
                prediction = model.predict(input_data)
                
                st.success("ตรวจสอบข้อมูลเสร็จสิ้น!")
                
                st.markdown("### 📊 สถานะการทำรายการ")
                if prediction[0] == 1:
                    st.markdown("""
                    <div style='background-color: #fee2e2; padding: 20px; border-radius: 10px; border-left: 5px solid #EF4444; text-align: center;'>
                        <h2 style='color: #b91c1c; margin: 0;'>🔴 ระงับการทำรายการ (Suspicious / Fraud)</h2>
                        <p style='color: #991b1b; margin-top: 10px; font-size: 1.1rem;'>
                            ระบบตรวจพบพฤติกรรมการใช้งานที่ผิดปกติและมีความเสี่ยงสูงว่าอาจถูกมิจฉาชีพขโมยบัตร <br>
                            <i>ระบบได้ทำการบล็อกรายการนี้ชั่วคราว กรุณาติดต่อ Call Center เพื่อยืนยันตัวตน</i>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background-color: #d1fae5; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981; text-align: center;'>
                        <h2 style='color: #047857; margin: 0;'>🟢 อนุมัติการทำรายการ (Normal Transaction)</h2>
                        <p style='color: #065f46; margin-top: 10px; font-size: 1.1rem;'>
                            รูปแบบการทำรายการปกติตามประวัติการใช้งานของลูกค้า ระบบได้ทำการตัดเงินเรียบร้อยแล้ว <br>
                            <i>ทำรายการสำเร็จอย่างปลอดภัย</i>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
        except FileNotFoundError:
            st.error("⚠️ ไม่พบไฟล์ 'Models/svm_fraud_model.pkl' กรุณาตรวจสอบว่าได้สร้างโฟลเดอร์ Models และใส่ไฟล์ไว้แล้ว")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")

elif selected_page == "🌀 K-Means Clustering":
    render_model_page("K-Means Clustering", "🌀", "ระบบจัดกลุ่มลูกค้าบัตรเครดิตเพื่อเสนอโปรโมชั่น (Customer Segmentation)", "#8B5CF6")
    
    st.markdown("### 💳 1. กรอกข้อมูลพฤติกรรมการเงินของลูกค้า")
    
    col1, col2 = st.columns(2)
    with col1:
        income_val = st.number_input("รายได้เฉลี่ยต่อเดือน (บาท)", min_value=10000, max_value=500000, value=45000, step=5000)
    with col2:
        spending_val = st.number_input("ยอดใช้จ่ายผ่านบัตรเฉลี่ยต่อเดือน (บาท)", min_value=0, max_value=500000, value=15000, step=1000)
        
    st.markdown("---")
    
    if st.button("🚀 วิเคราะห์และจัดกลุ่มลูกค้า", use_container_width=True):
        import pickle
        import pandas as pd
        try:
            with st.spinner('กำลังให้ AI จัดกลุ่มเปรียบเทียบกับฐานข้อมูลลูกค้าทั้งหมด...'):
                # เปลี่ยน Path ไปที่ Models/
                with open('Models/kmeans_customer_model.pkl', 'rb') as file:
                    model = pickle.load(file)
                
                input_df = pd.DataFrame({'Income': [income_val], 'Spending': [spending_val]})
                cluster_id = model.predict(input_df)[0]
                
                kmeans_step = model.named_steps['kmeans']
                scaler_step = model.named_steps['scaler']
                
                centroid_scaled = kmeans_step.cluster_centers_[cluster_id]
                centroid_real = scaler_step.inverse_transform([centroid_scaled])[0]
                
                center_income = centroid_real[0]
                center_spending = centroid_real[1]
                
                if center_income >= 60000 and center_spending >= 30000:
                    persona = "💎 ลูกค้าระดับพรีเมียม (VIP / High Roller)"
                    desc = "รายได้สูงและยอดใช้จ่ายสูงมาก เป็นกลุ่มลูกค้าที่สร้างกำไรหลักให้บริษัท"
                    promo = "เสนอโปรโมชั่นบัตรเครดิตระดับพรีเมียม, สิทธิ์เข้าเลานจ์สนามบิน, หรือของรางวัลแบรนด์เนม"
                    bg_color, text_color = "#fdf4ff", "#86198f" 
                elif center_income >= 60000 and center_spending < 30000:
                    persona = "🛡️ กลุ่มมีกำลังซื้อแต่เน้นออม (Conservative)"
                    desc = "รายได้สูงแต่ระมัดระวังการใช้จ่าย (ยอดใช้จ่ายน้อยกว่าที่ควรจะเป็น)"
                    promo = "เสนอโปรโมชั่น Cash Back เงินคืน, แนะนำกองทุนรวม, หรือประกันสะสมทรัพย์"
                    bg_color, text_color = "#f0fdf4", "#166534" 
                elif center_income < 60000 and center_spending >= 20000:
                    persona = "🛍️ กลุ่มชอบใช้จ่าย (Trend Spender)"
                    desc = "รายได้ปานกลางถึงน้อย แต่มีพฤติกรรมการช้อปปิ้งและยอดใช้จ่ายสูง"
                    promo = "เสนอโปรโมชั่นผ่อน 0% นาน 10 เดือน, สินเชื่อส่วนบุคคล, หรือคะแนนสะสมคูณสอง"
                    bg_color, text_color = "#fff7ed", "#c2410c" 
                else:
                    persona = "🛒 กลุ่มใช้จ่ายตามความจำเป็น (Sensible Saver)"
                    desc = "รายได้ปานกลาง/น้อย และมียอดใช้จ่ายในระดับทั่วไป ไม่หวือหวา"
                    promo = "เสนอส่วนลดร้านสะดวกซื้อ, ซูเปอร์มาร์เก็ต, หรือโปรโมชั่นเติมน้ำมัน/จ่ายบิล"
                    bg_color, text_color = "#f0f9ff", "#0369a1" 
                
                st.success("จัดกลุ่มลูกค้าเสร็จสิ้น!")
                
                st.markdown(f"""
                <div style='background-color: {bg_color}; padding: 25px; border-radius: 12px; border-top: 5px solid {text_color}; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
                    <h2 style='color: {text_color}; margin-top: 0;'>{persona}</h2>
                    <p style='color: #475569; font-size: 1.1rem; margin-bottom: 5px;'><b>พฤติกรรม:</b> {desc}</p>
                    <hr style='border-color: {text_color}40; margin: 15px 0;'>
                    <p style='color: {text_color}; font-size: 1.1rem; margin: 0;'><b>💡 ข้อเสนอแนะทางการตลาด:</b> {promo}</p>
                </div>
                """, unsafe_allow_html=True)
                
        except FileNotFoundError:
            st.error("⚠️ ไม่พบไฟล์ 'Models/kmeans_customer_model.pkl' กรุณาตรวจสอบว่าได้สร้างโฟลเดอร์ Models และใส่ไฟล์ไว้แล้ว")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")

elif selected_page == "📈 Regression":
    render_model_page("Regression", "📈", "ระบบคาดการณ์ยอดขายรายเดือนและประเมินกำไรธุรกิจ (Revenue Forecasting)", "#EF4444")
    
    st.markdown("### 🏬 1. ระบุข้อมูลทำเลที่ตั้งสาขาใหม่")
    
    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input("ขนาดพื้นที่ร้าน (ตารางเมตร)", min_value=10, max_value=500, value=80)
        population = st.number_input("จำนวนประชากรในรัศมี 5 กม.", min_value=1000, max_value=500000, value=50000, step=5000)
    with col2:
        marketing = st.number_input("งบโฆษณา/ส่งเสริมการขาย (บาท/เดือน)", min_value=0, max_value=200000, value=15000, step=1000)
        competitor_dist = st.number_input("ระยะห่างจากร้านคู่แข่ง (กิโลเมตร)", min_value=0.1, max_value=50.0, value=3.5, step=0.5)
        
    st.markdown("---")
    
    if st.button("🚀 ประเมินยอดขายและการลงทุน", use_container_width=True):
        import pickle
        import pandas as pd
        try:
            with st.spinner('กำลังคำนวณและสร้างโมเดลคาดการณ์ทางการเงิน...'):
                # เปลี่ยน Path ไปที่ Models/
                with open('Models/regression_franchise_model.pkl', 'rb') as file:
                    model = pickle.load(file)
                
                input_df = pd.DataFrame({
                    'Area': [area],
                    'Population': [population],
                    'Marketing': [marketing],
                    'Competitor_Dist': [competitor_dist]
                })
                
                predicted_revenue = model.predict(input_df)[0]
                
                estimated_cost = predicted_revenue * 0.75
                net_profit = predicted_revenue - estimated_cost
                margin_percent = (net_profit / predicted_revenue) * 100
                
                st.success("การประเมินทางการเงินเสร็จสิ้น!")
                
                st.markdown("### 📊 รายงานคาดการณ์ทางการเงิน (ต่อเดือน)")
                
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("💰 คาดการณ์ยอดขายรวม", f"฿{predicted_revenue:,.2f}")
                m_col2.metric("📉 ต้นทุนประเมิน (75%)", f"฿{estimated_cost:,.2f}")
                
                if net_profit > 0:
                    m_col3.metric("📈 กำไรสุทธิคาดการณ์", f"฿{net_profit:,.2f}", f"{margin_percent:.1f}% Margin")
                    st.markdown(f"""
                    <div style='background-color: #f0fdf4; padding: 20px; border-radius: 10px; border-left: 5px solid #22c55e;'>
                        <h4 style='color: #166534; margin: 0;'>✅ สรุปความคุ้มค่าการลงทุน: น่าน่าลงทุน</h4>
                        <p style='color: #15803d; margin-top: 5px;'>ทำเลนี้มีศักยภาพในการทำกำไร สามารถพิจารณาเดินหน้าแผนธุรกิจหรือเพิ่มงบการตลาดเพื่อดันยอดขายได้</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    m_col3.metric("⚠️ ขาดทุนสุทธิคาดการณ์", f"฿{net_profit:,.2f}", f"{margin_percent:.1f}% Margin", delta_color="inverse")
                    st.markdown(f"""
                    <div style='background-color: #fef2f2; padding: 20px; border-radius: 10px; border-left: 5px solid #ef4444;'>
                        <h4 style='color: #991b1b; margin: 0;'>❌ สรุปความคุ้มค่าการลงทุน: มีความเสี่ยงสูง</h4>
                        <p style='color: #b91c1c; margin-top: 5px;'>ทำเลนี้อาจสร้างรายได้ไม่ครอบคลุมต้นทุน แนะนำให้พิจารณาหาพื้นที่ใหม่ หรือปรับโครงสร้างขนาดร้านเพื่อลดต้นทุน</p>
                    </div>
                    """, unsafe_allow_html=True)

        except FileNotFoundError:
            st.error("⚠️ ไม่พบไฟล์ 'Models/regression_franchise_model.pkl' กรุณาตรวจสอบว่าได้สร้างโฟลเดอร์ Models และใส่ไฟล์ไว้แล้ว")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")

elif selected_page == "🌲 Ensemble (Random Forest)":
    render_model_page("Ensemble (Random Forest)", "🌲", "AI ทำนายทิศทางหุ้นแบบ Real-time ด้วย Random Forest", "#06B6D4")
    
    st.markdown("### 📊 1. ระบุหุ้นที่ต้องการวิเคราะห์")
    
    ticker_input = st.text_input("กรอกสัญลักษณ์หุ้น (เช่น AAPL, TSLA หรือ PTT.BK สำหรับหุ้นไทย)", value="AAPL")
    
    st.markdown("---")
    
    if st.button("🚀 ดึงข้อมูลล่าสุด & วิเคราะห์แนวโน้ม", use_container_width=True):
        import pickle
        import yfinance as yf
        import pandas as pd
        
        try:
            with st.spinner(f'กำลังดึงข้อมูลหุ้น {ticker_input} จากตลาดหลักทรัพย์...'):
                # เปลี่ยน Path ไปที่ Models/
                with open('Models/stock_model.pkl', 'rb') as file:
                    model = pickle.load(file)
                
                ticker_data = yf.download(ticker_input, period="60d")
                
                if ticker_data.empty:
                    st.error("❌ ไม่พบข้อมูลหุ้นนี้ กรุณาตรวจสอบสัญลักษณ์ให้ถูกต้อง")
                else:
                    ticker_data['SMA_10'] = ticker_data['Close'].rolling(window=10).mean()
                    ticker_data['SMA_30'] = ticker_data['Close'].rolling(window=30).mean()
                    ticker_data['Volume_Change'] = ticker_data['Volume'].pct_change()
                    
                    latest_data = ticker_data.iloc[-1]
                    
                    def get_safe_float(column_name):
                        val = latest_data[column_name]
                        if isinstance(val, pd.Series):
                            return float(val.iloc[0])
                        return float(val)

                    latest_close = get_safe_float('Close')
                    latest_sma_10 = get_safe_float('SMA_10')
                    latest_sma_30 = get_safe_float('SMA_30')
                    latest_vol_change = get_safe_float('Volume_Change')
                    
                    input_features = [[latest_close, latest_sma_10, latest_sma_30, latest_vol_change]]
                    
                    prediction = model.predict(input_features)
                    
                    st.success(f"วิเคราะห์ข้อมูลหุ้น {ticker_input} สำเร็จ!")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("ราคาปิดล่าสุด", f"{latest_close:.2f}")
                    col2.metric("SMA 10 วัน", f"{latest_sma_10:.2f}")
                    col3.metric("SMA 30 วัน", f"{latest_sma_30:.2f}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if prediction[0] == 1:
                        st.markdown("<div style='background-color: #d1fae5; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981;'><h2 style='text-align: center; color: #047857; margin: 0;'>🟢 สัญญาณ: แนะนำให้ซื้อ (Buy)</h2><p style='text-align: center; color: #065f46; margin-top: 10px;'>โมเดลคาดการณ์ว่าแนวโน้มราคาในวันทำการถัดไปจะเป็นขาขึ้น</p></div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='background-color: #fee2e2; padding: 20px; border-radius: 10px; border-left: 5px solid #EF4444;'><h2 style='text-align: center; color: #b91c1c; margin: 0;'>🔴 สัญญาณ: แนะนำให้ขาย / รอดูสถานการณ์</h2><p style='text-align: center; color: #991b1b; margin-top: 10px;'>โมเดลคาดการณ์ว่าแนวโน้มราคาในวันทำการถัดไปจะปรับตัวลง</p></div>", unsafe_allow_html=True)

        except FileNotFoundError:
            st.error("⚠️ ไม่พบไฟล์ 'Models/stock_model.pkl' กรุณาตรวจสอบว่าได้สร้างโฟลเดอร์ Models และใส่ไฟล์ไว้แล้ว")
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")