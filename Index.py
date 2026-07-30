import streamlit as st
import base64
import os
import pickle
import yfinance as yf
import pandas as pd

# ตั้งค่าหน้าเว็บให้แสดงผลแบบกว้าง
st.set_page_config(page_title="ML Web Model Portfolio", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# ฟังก์ชันโหลดไฟล์ CSS ภายนอก (style.css)
# ==========================================
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ ไม่พบไฟล์ {file_name} กรุณาสร้างไฟล์ CSS แยกไว้ในโฟลเดอร์หลัก")

load_css("style.css")

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
    image_path = "Image/dev.png"
    
    try:
        img_base64 = get_base64_of_bin_file(image_path)
        img_src = f"data:image/png;base64,{img_base64}"
    except FileNotFoundError:
        img_src = "https://cdn-icons-png.flaticon.com/512/4140/4140037.png"
        st.error(f"⚠️ ไม่พบไฟล์รูปภาพที่: {image_path} ระบบจึงใช้รูปสำรอง")

    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="{img_src}" width="90" style="border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 10px;">
            <h3 style="margin: 0; font-size: 2rem;"><b style="color: #2CFF05;">Developer</b></h3>
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
    
    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    st.button("⬅️ กลับหน้าหลัก", on_click=change_page, args=("🏠 หน้าหลัก (Home)",))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🤖 ทดลองใช้งานโมเดล")

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
            st.button(f"เปิดใช้งานโมเดล", key=f"btn_{title}", use_container_width=True, on_click=change_page, args=(page_target,))
            st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

    # แสดงการ์ด 6 โมเดล
    create_card(col1, "🧮", "K-Nearest Neighbor", "ระบบประเมินความเสี่ยงและอนุมัติสินเชื่อ (Loan Approval)", "#3B82F6", "🧮 K-Nearest Neighbor (KNN)")
    create_card(col2, "🌳", "Decision Tree", "ระบบวิเคราะห์ความเสี่ยงพนักงานลาออก (HR Analytics)", "#10B981", "🌳 Decision Tree")
    create_card(col3, "⚡", "Support Vector Machine", "ระบบตรวจจับการทุจริตบัตรเครดิต (Fraud Detection)", "#F59E0B", "⚡ Support Vector Machine (SVM)")

    create_card(col1, "🌀", "K-Means Clustering", "ระบบจัดกลุ่มลูกค้าบัตรเครดิต (Customer Segmentation)", "#8B5CF6", "🌀 K-Means Clustering")
    create_card(col2, "📈", "Regression", "ระบบคาดการณ์ยอดขายรายเดือนและประเมินกำไรธุรกิจ", "#EF4444", "📈 Regression")
    create_card(col3, "🌲", "Random Forest", "ระบบทำนายทิศทางหุ้นแบบ Real-time ด้วย Random Forest", "#06B6D4", "🌲 Ensemble (Random Forest)")

elif selected_page == "🧮 K-Nearest Neighbor (KNN)":
    render_model_page("K-Nearest Neighbor (KNN)", "🧮", "ระบบประเมินความเสี่ยงและอนุมัติสินเชื่อ (Loan Approval) ด้วย KNN", "#3B82F6")
    
    st.markdown("### 📋 1. กรอกข้อมูลผู้ขอสินเชื่อ")
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("รายได้ต่อเดือน (บาท)", min_value=0, value=35000, step=1000)
        loan_amount = st.number_input("ยอดเงินที่ขอกู้ (บาท)", min_value=0, value=500000, step=10000)
    with col2:
        work_exp = st.number_input("อายุงาน (ปี)", min_value=0, max_value=100, value=3)
        credit_score = st.slider("คะแนนเครดิตบูโร (Credit Score)", min_value=300, max_value=850, value=650)
        st.markdown("<small style='color:gray;'>* 300=แย่มาก, 850=ดีเยี่ยม</small>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    if st.button("🚀 ประเมินความเสี่ยงสินเชื่อ", use_container_width=True):
        try:
            with st.spinner('กำลังเปรียบเทียบโปรไฟล์กับฐานข้อมูลลูกค้า...'):
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
                        <p style='color: #065f46; margin-top: 10px; font-size: 1.1rem;'>โปรไฟล์มีความน่าเชื่อถือและมีความเสี่ยงต่ำ</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background-color: #fee2e2; padding: 20px; border-radius: 10px; border-left: 5px solid #EF4444; text-align: center;'>
                        <h2 style='color: #b91c1c; margin: 0;'>🔴 ไม่อนุมัติ / ความเสี่ยงสูง (Rejected)</h2>
                        <p style='color: #991b1b; margin-top: 10px; font-size: 1.1rem;'>โปรไฟล์มีความเสี่ยงสูง แนะนำให้ลดวงเงินกู้</p>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")

elif selected_page == "🌳 Decision Tree":
    render_model_page("Decision Tree", "🌳", "ระบบวิเคราะห์ความเสี่ยงพนักงานลาออก (HR Analytics) ด้วย Decision Tree", "#10B981")
    
    st.markdown("### 📋 1. กรอกข้อมูลโปรไฟล์พนักงาน")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("อายุพนักงาน (ปี)", min_value=18, max_value=80, value=30)
        income = st.number_input("เงินเดือน (บาท)", min_value=9000, value=30000, step=1000)
    with col2:
        overtime_input = st.selectbox("การทำงานล่วงเวลา (Overtime)", options=["ไม่ทำ (No)", "ทำ (Yes)"])
        satisfaction = st.slider("ระดับความพึงพอใจในงาน (1=แย่สุด, 4=ดีมาก)", min_value=1, max_value=4, value=3)
    
    overtime_val = 1 if overtime_input == "ทำ (Yes)" else 0
    st.markdown("---")
    
    if st.button("🚀 ประเมินความเสี่ยงการลาออก", use_container_width=True):
        try:
            with st.spinner('กำลังใช้ Decision Tree วิเคราะห์รูปแบบข้อมูล...'):
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
                        <p style='color: #991b1b; margin-top: 10px; font-size: 1.1rem;'>พนักงานมีแนวโน้มที่จะลาออกสูง</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background-color: #d1fae5; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981; text-align: center;'>
                        <h2 style='color: #047857; margin: 0;'>🟢 ความเสี่ยงต่ำ (Low Risk / Retained)</h2>
                        <p style='color: #065f46; margin-top: 10px; font-size: 1.1rem;'>พนักงานมีแนวโน้มที่จะอยู่กับองค์กรต่อ</p>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")

elif selected_page == "⚡ Support Vector Machine (SVM)":
    render_model_page("Support Vector Machine (SVM)", "⚡", "ระบบประเมินความเสี่ยงและตรวจจับการทุจริตบัตรเครดิต (Fraud Detection)", "#F59E0B")
    
    st.markdown("### 💳 1. ข้อมูลการทำธุรกรรมล่าสุด")
    
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("ยอดเงินที่ทำรายการ (บาท)", min_value=0.0, value=1500.0, step=500.0)
        distance = st.number_input("ระยะทางจากจุดใช้งานประจำ (กิโลเมตร)", min_value=0.0, value=5.0, step=1.0)
    with col2:
        intl_txn_input = st.selectbox("เป็นการทำรายการจากต่างประเทศหรือไม่?", options=["ไม่ใช่ (Domestic)", "ใช่ (International)"])
        failed_pin = st.number_input("จำนวนครั้งที่ใส่รหัส PIN ผิดก่อนหน้านี้", min_value=0, max_value=5, value=0)
        
    intl_txn = 1 if intl_txn_input == "ใช่ (International)" else 0
        
    st.markdown("---")
    
    if st.button("🚀 ตรวจสอบความปลอดภัยของธุรกรรม", use_container_width=True):
        import pickle
        try:
            with st.spinner('กำลังใช้เทคโนโลยี SVM และระบบความปลอดภัยตรวจสอบ...'):
                # 1. เช็คกฎเหล็กความปลอดภัยก่อน (Guardrail) ถ้าเข้าข่ายโกง บล็อกทันที!
                # เงื่อนไข: ใส่รหัสผิดตั้งแต่ 3 ครั้งขึ้นไป หรือ (ยอดเกิน 30,000 และอยู่ต่างประเทศ)
                is_fraud_rule = (failed_pin >= 3) or (amount > 30000 and intl_txn == 1) or (distance > 100)
                
                if is_fraud_rule:
                    prediction_val = 1 # บังคับเป็นทุจริต
                else:
                    # ถ้าผ่านกฎเหล็ก ค่อยให้โมเดล SVM ตัดสินใจต่อ
                    with open('Models/svm_fraud_model.pkl', 'rb') as file:
                        model = pickle.load(file)
                    input_data = [[amount, distance, intl_txn, failed_pin]]
                    prediction_val = model.predict(input_data)[0]
                
                st.success("ตรวจสอบข้อมูลเสร็จสิ้น!")
                
                st.markdown("### 📊 สถานะการทำรายการ")
                if prediction_val == 1:
                    st.markdown("""
                    <div style='background-color: #fee2e2; padding: 20px; border-radius: 10px; border-left: 5px solid #EF4444; text-align: center;'>
                        <h2 style='color: #b91c1c; margin: 0;'>🔴 ระงับการทำรายการ (Suspicious / Fraud)</h2>
                        <p style='color: #991b1b; margin-top: 10px; font-size: 1.1rem;'>
                            ระบบตรวจพบพฤติกรรมการใช้งานที่ผิดปกติ (ใส่รหัสผิดบ่อย / ยอดสูงผิดปกติในต่างประเทศ) <br>
                            <i>ระบบได้ทำการบล็อกรายการนี้ชั่วคราวเพื่อความปลอดภัยของท่าน</i>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background-color: #d1fae5; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981; text-align: center;'>
                        <h2 style='color: #047857; margin: 0;'>🟢 อนุมัติการทำรายการ (Normal Transaction)</h2>
                        <p style='color: #065f46; margin-top: 10px; font-size: 1.1rem;'>
                            รูปแบบการทำรายการปกติตามประวัติการใช้งาน ระบบได้ทำการตัดเงินเรียบร้อยแล้ว <br>
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
        try:
            with st.spinner('กำลังให้ AI จัดกลุ่มเปรียบเทียบกับฐานข้อมูลลูกค้าทั้งหมด...'):
                with open('Models/kmeans_customer_model.pkl', 'rb') as file:
                    model = pickle.load(file)
                
                input_df = pd.DataFrame({'Income': [income_val], 'Spending': [spending_val]})
                cluster_id = model.predict(input_df)[0]
                
                kmeans_step = model.named_steps['kmeans']
                scaler_step = model.named_steps['scaler']
                centroid_scaled = kmeans_step.cluster_centers_[cluster_id]
                centroid_real = scaler_step.inverse_transform([centroid_scaled])[0]
                
                center_income, center_spending = centroid_real[0], centroid_real[1]
                
                if center_income >= 60000 and center_spending >= 30000:
                    persona, desc, promo = "💎 ลูกค้าระดับพรีเมียม (VIP)", "รายได้สูงและยอดใช้จ่ายสูงมาก", "เสนอโปรโมชั่นบัตรพรีเมียม / เลานจ์"
                    bg_color, text_color = "#fdf4ff", "#86198f"
                elif center_income >= 60000 and center_spending < 30000:
                    persona, desc, promo = "🛡️ กลุ่มมีกำลังซื้อแต่เน้นออม", "รายได้สูงแต่ระมัดระวังการใช้จ่าย", "เสนอ Cash Back หรือกองทุนรวม"
                    bg_color, text_color = "#f0fdf4", "#166534"
                elif center_income < 60000 and center_spending >= 20000:
                    persona, desc, promo = "🛍️ กลุ่มชอบใช้จ่าย (Trend Spender)", "รายได้ปานกลางแต่ยอดช้อปปิ้งสูง", "เสนอผ่อน 0% นาน 10 เดือน"
                    bg_color, text_color = "#fff7ed", "#c2410c"
                else:
                    persona, desc, promo = "🛒 กลุ่มใช้จ่ายตามความจำเป็น", "รายได้ปานกลางและยอดใช้จ่ายทั่วไป", "เสนอส่วนลดซูเปอร์มาร์เก็ต/เติมน้ำมัน"
                    bg_color, text_color = "#f0f9ff", "#0369a1"
                
                st.success("จัดกลุ่มลูกค้าเสร็จสิ้น!")
                st.markdown(f"""
                <div style='background-color: {bg_color}; padding: 25px; border-radius: 12px; border-top: 5px solid {text_color}; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
                    <h2 style='color: {text_color}; margin-top: 0;'>{persona}</h2>
                    <p style='color: #475569; font-size: 1.1rem; margin-bottom: 5px;'><b>พฤติกรรม:</b> {desc}</p>
                    <hr style='border-color: {text_color}40; margin: 15px 0;'>
                    <p style='color: {text_color}; font-size: 1.1rem; margin: 0;'><b>💡 คำแนะนำ:</b> {promo}</p>
                </div>
                """, unsafe_allow_html=True)
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
        try:
            with st.spinner('กำลังคำนวณและสร้างโมเดลคาดการณ์ทางการเงิน...'):
                with open('Models/regression_franchise_model.pkl', 'rb') as file:
                    model = pickle.load(file)
                
                input_df = pd.DataFrame({
                    'Area': [area], 'Population': [population],
                    'Marketing': [marketing], 'Competitor_Dist': [competitor_dist]
                })
                
                predicted_revenue = model.predict(input_df)[0]
                estimated_cost = predicted_revenue * 0.75
                net_profit = predicted_revenue - estimated_cost
                margin_percent = (net_profit / predicted_revenue) * 100
                
                st.success("การประเมินทางการเงินเสร็จสิ้น!")
                st.markdown("### 📊 รายงานคาดการณ์ทางการเงิน (ต่อเดือน)")
                
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("💰 ยอดขายรวม", f"฿{predicted_revenue:,.2f}")
                m_col2.metric("📉 ต้นทุน (75%)", f"฿{estimated_cost:,.2f}")
                
                if net_profit > 0:
                    m_col3.metric("📈 กำไรสุทธิ", f"฿{net_profit:,.2f}", f"{margin_percent:.1f}% Margin")
                    st.markdown("<div style='background-color: #f0fdf4; padding: 20px; border-radius: 10px; border-left: 5px solid #22c55e;'><h4 style='color: #166534; margin: 0;'>✅ น่าลงทุน</h4></div>", unsafe_allow_html=True)
                else:
                    m_col3.metric("⚠️ ขาดทุนสุทธิ", f"฿{net_profit:,.2f}", f"{margin_percent:.1f}% Margin", delta_color="inverse")
                    st.markdown("<div style='background-color: #fef2f2; padding: 20px; border-radius: 10px; border-left: 5px solid #ef4444;'><h4 style='color: #991b1b; margin: 0;'>❌ ความเสี่ยงสูง</h4></div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")

elif selected_page == "🌲 Ensemble (Random Forest)":
    render_model_page("Ensemble (Random Forest)", "🌲", "AI ทำนายทิศทางหุ้นแบบ Real-time ด้วย Random Forest", "#06B6D4")
    
    st.markdown("### 📊 1. ระบุหุ้นที่ต้องการวิเคราะห์")
    ticker_input = st.text_input("กรอกสัญลักษณ์หุ้น (เช่น AAPL, TSLA หรือ PTT.BK สำหรับหุ้นไทย)", value="AAPL")
    st.markdown("---")
    
    if st.button("🚀 ดึงข้อมูลล่าสุด & วิเคราะห์แนวโน้ม", use_container_width=True):
        try:
            with st.spinner(f'กำลังดึงข้อมูลหุ้น {ticker_input} จากตลาดหลักทรัพย์...'):
                with open('Models/stock_model.pkl', 'rb') as file:
                    model = pickle.load(file)
                
                ticker_data = yf.download(ticker_input, period="60d")
                
                if ticker_data.empty:
                    st.error("❌ ไม่พบข้อมูลหุ้นนี้ กรุณาตรวจสอบสัญลักษณ์ให้ถูกต้อง")
                else:
                    ticker_data['SMA_10'] = ticker_data['Close'].rolling(window=10).mean()
                    ticker_data['SMA_30'] = ticker_data['Close'].rolling(window=30).mean()
                    ticker_data['Volume_Change'] = ticker_data['Volume'].pct_change()
                    
                    delta = ticker_data['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    ticker_data['RSI'] = 100 - (100 / (1 + rs))
                    
                    ema_12 = ticker_data['Close'].ewm(span=12, adjust=False).mean()
                    ema_26 = ticker_data['Close'].ewm(span=26, adjust=False).mean()
                    ticker_data['MACD'] = ema_12 - ema_26
                    
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
                    latest_rsi = get_safe_float('RSI')
                    latest_macd = get_safe_float('MACD')
                    
                    input_features = [[
                        latest_close, latest_sma_10, latest_sma_30, 
                        latest_vol_change, latest_rsi, latest_macd
                    ]]
                    
                    prediction = model.predict(input_features)
                    
                    st.success(f"วิเคราะห์ข้อมูลหุ้น {ticker_input} สำเร็จ!")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("ราคาปิดล่าสุด", f"{latest_close:.2f}")
                    col2.metric("RSI", f"{latest_rsi:.2f}")
                    col3.metric("MACD", f"{latest_macd:.2f}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if prediction[0] == 1:
                        st.markdown("<div style='background-color: #d1fae5; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981;'><h2 style='text-align: center; color: #047857; margin: 0;'>🟢 สัญญาณ: แนะนำให้ซื้อ (Buy)</h2></div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='background-color: #fee2e2; padding: 20px; border-radius: 10px; border-left: 5px solid #EF4444;'><h2 style='text-align: center; color: #b91c1c; margin: 0;'>🔴 สัญญาณ: แนะนำให้ขาย / รอดูสถานการณ์</h2></div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {e}")