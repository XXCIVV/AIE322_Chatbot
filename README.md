# ⚽ Soccer Chatbot 🤖  
เป็นแชตบอทขนาดเล็กที่ถูกพัฒนาขึ้นเพื่อเรียนรู้และทดลองการใช้งาน LLM (Large Language Model) และการทำงานของ RAG (Retrieval Augmented Generation)  
ผ่านเครื่องมือ Framework ต่างๆ  

## 🛠️ Framework ที่ใช้ในงาน  
1. 🐍 Python  
2. 🏗️ FAISS  
3. 🌐 Flask API  
4. 🎨 HTML + CSS + JavaScript  

## 🚀 วิธีการใช้งานเบื้องต้น  
1. 📥 ติดตั้งไลบรารีที่จำเป็นโดยใช้คำสั่ง:
   ```bash
   pip install -r requirements.txt
   ```  
2. ▶️ รัน `FaissRun.py` เพื่อเตรียมข้อมูลสำหรับการค้นหา
   ```bash
   python FaissRun.py
   ```
3. ▶️ รัน `app.py` เพื่อเริ่ม Flask Server
   ```bash
   python app.py
   ```
4. 🔗 เข้าไปที่ลิ้งค์ [127.0.0.1:5000](http://127.0.0.1:5000)  
5. 🗨️ เมื่อเข้าไปจะเห็นหน้าแชทบอท 💬 ถามคำถามเกี่ยวกับฟุตบอลได้เลย!!  

### 🎯 ตัวอย่างคำถาม  
- 🏆 **How many goals did Messi score?**  
- ⚽ **What was the score of the last World Cup final?**  

🔥 สนุกกับการถามตอบเรื่องฟุตบอลกันเลย! 🎉  

## หมายเหตุ
โปรเจกต์นี้เป็นการทดลองและศึกษาเกี่ยวกับ LLM และ RAG สำหรับการดึงข้อมูลฟุตบอลแบบเรียลไทม์



