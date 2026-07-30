import pickle
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. โหลดข้อมูลชุดดอกไม้ Iris จาก Scikit-Learn
iris = load_iris()
X = iris.data  # ข้อมูลขนาดของดอกไม้ 4 ส่วน
y = iris.target # สายพันธุ์ของดอกไม้ (0=Setosa, 1=Versicolor, 2=Virginica)

# 2. แบ่งข้อมูลสำหรับ Train 80% และ Test 20%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. สร้างและสอน (Train) โมเดล KNN
knn_model = KNeighborsClassifier(n_neighbors=3)
knn_model.fit(X_train, y_train)

# 4. ทดสอบความแม่นยำให้ชื่นใจสักหน่อย (ไม่บังคับ)
y_pred = knn_model.predict(X_test)
print(f"✅ ความแม่นยำของโมเดล: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# 5. บันทึกโมเดลเป็นไฟล์ (หัวใจสำคัญ!)
with open('knn_model.pkl', 'wb') as file:
    pickle.dump(knn_model, file)

print("💾 บันทึกไฟล์ 'knn_model.pkl' สำเร็จ! นำไฟล์นี้ไปวางคู่กับโค้ด Streamlit ได้เลย")