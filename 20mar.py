import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="กิจกรรมปัจฉิมสุดคูล", page_icon="🎓")

st.title("🎓 โหวต 'ที่สุดในรุ่น' (Class Awards)")
st.subheader("มาเลือกเพื่อนที่ครูและเพื่อนๆ ประทับใจกัน!")

# รายชื่อผู้เข้าชิง (ครูเปลี่ยนเป็นชื่อนักเรียนได้เลยครับ)
students = ["สมชาย", "สมหญิง", "ใจดี", "มานะ", "ชูใจ"]

# รายชื่อรางวัล
awards = [
    "🌟 เพื่อนที่พึ่งพาได้มากที่สุด",
    "🤣 ตัวตึงเน้นฮาประจำห้อง",
    "🏃‍♂️ นักสู้ (มาสายแต่มานะ)",
    "📚 ว่าที่ด็อกเตอร์คนต่อไป"
]

# สร้าง Dictionary เก็บผลโหวต (ในระบบจริงควรใช้ Database แต่ตัวอย่างนี้ใช้ Session State ครับ)
if 'votes' not in st.session_state:
    st.session_state.votes = {award: {name: 0 for name in students} for award in awards}

# ส่วนหน้าเว็บสำหรับเด็กๆ โหวต
with st.form("voting_form"):
    st.write("### 📝 ลงคะแนนโหวต")
    voter_name = st.text_input("ชื่อเล่นของคุณ (เพื่อยืนยันตัวตน)")
    
    selected_votes = {}
    for award in awards:
        selected_votes[award] = st.selectbox(f"เลือกใครดีสำหรับรางวัล: {award}", students, key=award)
    
    submitted = st.form_submit_button("ส่งผลโหวต")
    
    if submitted:
        if voter_name:
            for award, student in selected_votes.items():
                st.session_state.votes[award][student] += 1
            st.success(f"ขอบคุณนะ {voter_name}! บันทึกคะแนนเรียบร้อยแล้ว")
        else:
            st.warning("ใส่ชื่อเล่นหน่อยนะจ๊ะเด็กๆ")

# ส่วนแสดงผล (ครูอาจจะซ่อนไว้ก่อน แล้วค่อยเปิดโชว์ท้ายคาบ)
if st.checkbox("📊 ดูผลคะแนน (สำหรับคุณครูเปิดโชว์จอหน้าห้อง)"):
    st.write("---")
    st.header("🏆 ผลคะแนนล่าสุด")
    for award in awards:
        st.write(f"**{award}**")
        df = pd.DataFrame(st.session_state.votes[award].items(), columns=['ชื่อเพื่อน', 'คะแนน'])
        st.bar_chart(df.set_index('ชื่อเพื่อน'))