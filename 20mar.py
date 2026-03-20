import streamlit as st
import pandas as pd

# --- การตั้งค่าเบื้องต้น ---
st.set_page_config(page_title="กิจกรรมกระจกเงาใจ", layout="wide")

# จำลองฐานข้อมูล (ในใช้งานจริงควรเชื่อมต่อ Google Sheets หรือ SQL)
# สำหรับตัวอย่างนี้จะใช้ st.cache_resource เพื่อจำลองฐานข้อมูลที่ทุกคนเข้าถึงได้ในเครื่องเดียวกัน
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=['Nickname'] + [f'Q{i}' for i in range(1, 11)])

if 'admin_unlock' not in st.session_state:
    st.session_state.admin_unlock = False # ครูเป็นคนคุมปุ่มนี้

# --- ส่วนของครู (Admin Control) ---
with st.sidebar:
    st.header("👑 ส่วนของคุณครู")
    password = st.text_input("รหัสผ่านครู", type="password")
    if password == "1234": # ตั้งรหัสผ่านง่ายๆ
        if st.button("🚀 เปิดหน้า Dashboard ให้เด็กๆ"):
            st.session_state.admin_unlock = True
            st.success("เปิดระบบ Dashboard แล้ว!")
        if st.button("🔄 ล้างข้อมูลทั้งหมด"):
            st.session_state.db = pd.DataFrame(columns=['Nickname'] + [f'Q{i}' for i in range(1, 11)])
            st.session_state.admin_unlock = False
            st.rerun()

# --- ส่วนของนักเรียน ---
questions = [
    "1. เมื่อพูดถึง 'พลังบวก' ฉันนึกถึง...",
    "2. เมื่อพูดถึง 'นักแก้ปัญหา' ฉันนึกถึง...",
    "3. เมื่อพูดถึง 'ผู้ฟังที่ดีที่สุด' ฉันนึกถึง...",
    "4. เมื่อพูดถึง 'ความใจดี' ฉันนึกถึง...",
    "5. เมื่อพูดถึง 'สีสันของกลุ่ม' ฉันนึกถึง...",
    "6. เมื่อพูดถึง 'คนแรกที่นึกถึงเมื่อเห็นคำถามนี้' ฉันนึกถึง...",
    "7. เมื่อพูดถึง 'ตัวตึง ตัวป่วน' ฉันนึกถึง...",
    "8. เมื่อพูดถึง 'พ่อพระ แม่พระ' ฉันนึกถึง...",
    "9. เมื่อพูดถึง 'คนง่วง' ฉันนึกถึง...",
    "10. เมื่อพูดถึง 'ผู้ให้กำลัง' ฉันนึกถึง..."
]

if not st.session_state.admin_unlock:
    st.title("📝 กิจกรรม: ใครกันนะ?")
    
    # ขั้นตอนที่ 1: พิมพ์ชื่อเล่น
    if 'my_nickname' not in st.session_state:
        nickname = st.text_input("ก่อนเริ่ม... บอกชื่อเล่นของคุณหน่อยจ้า:", key="nick_input")
        if st.button("ตกลง"):
            if nickname:
                st.session_state.my_nickname = nickname
                st.session_state.current_q = 0
                st.session_state.my_answers = []
                st.rerun()
    
    # ขั้นตอนที่ 2: ตอบทีละข้อ
    elif st.session_state.current_q < 10:
        q_idx = st.session_state.current_q
        st.subheader(f"สวัสดีจ๊ะ {st.session_state.my_nickname} 😊")
        st.write(f"ข้อที่ {q_idx + 1} จาก 10")
        
        answer = st.text_input(questions[q_idx], key=f"ans_{q_idx}")
        
        if st.button("ส่งคำตอบ"):
            if answer:
                st.session_state.my_answers.append(answer)
                st.session_state.current_q += 1
                
                # ถ้าตอบครบ 10 ข้อ ให้บันทึกลง DB
                if st.session_state.current_q == 10:
                    new_data = [st.session_state.my_nickname] + st.session_state.my_answers
                    # บันทึกข้อมูล (ในที่นี้คือ append ลง dataframe จำลอง)
                    temp_df = pd.DataFrame([new_data], columns=st.session_state.db.columns)
                    st.session_state.db = pd.concat([st.session_state.db, temp_df], ignore_index=True)
                
                st.rerun()
            else:
                st.warning("กรุณาพิมพ์ชื่อเพื่อนก่อนนะ")

    else:
        st.success("ส่งคำตอบครบแล้วจ้า! 🎉")
        st.info("💡 ตอนนี้ข้อมูลของคุณถูกเก็บไว้แล้ว รอคุณครูเปิดหน้า Dashboard พร้อมกันนะ...")

# --- ส่วน Dashboard (จะปรากฏเมื่อครูกดปุ่มเท่านั้น) ---
else:
    st.title("📊 Dashboard สรุปความประทับใจ")
    st.balloons()
    
    if st.session_state.db.empty:
        st.write("ยังไม่มีข้อมูลส่งเข้ามาเลย...")
    else:
        # แสดงผลเป็นตารางหรือการ์ด
        for index, row in st.session_state.db.iterrows():
            with st.expander(f"🌟 ความประทับใจจาก: {row['Nickname']}"):
                cols = st.columns(2)
                for i in range(1, 11):
                    target_col = cols[0] if i <= 5 else cols[1]
                    target_col.write(f"**{questions[i-1].split('.')[1]}**")
                    target_col.info(f"👉 {row[f'Q{i}']}")
