import streamlit as st
import pandas as pd
import time

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="โหวตที่สุดในรุ่น 🎓", page_icon="🎓", layout="centered")

# --- ส่วนของการจัดการข้อมูล ---
if 'votes' not in st.session_state:
    st.session_state.votes = {}
if 'total_voters' not in st.session_state:
    st.session_state.total_voters = 0
if 'voted_names' not in st.session_state:
    st.session_state.voted_names = []

# รายชื่อรางวัล
awards = [
    "🌟 เพื่อนที่พึ่งพาได้มากที่สุด",
    "🤣 ตัวตึงเน้นฮาประจำห้อง",
    "🏃‍♂️ นักสู้ (มาสายแต่มานะ)",
    "📚 ว่าที่ด็อกเตอร์คนต่อไป"
]

# --- Sidebar สำหรับคุณครู (ซ่อนไว้) ---
with st.sidebar:
    st.header("⚙️ เมนูคุณครู")
    teacher_pw = st.text_input("รหัสผ่านครู", type="password")
    
    if teacher_pw == "1234": # ครูเปลี่ยนรหัสตรงนี้ได้ครับ
        input_names = st.text_area("ใส่รายชื่อนักเรียน (คั่นด้วย ,)", 
                                  value="สมชาย, สมหญิง, มานะ, มานี")
        students = [s.strip() for s in input_names.split(",") if s.strip()]
        
        if st.button("✅ อัปเดตรายชื่อ/เริ่มใหม่"):
            st.session_state.votes = {award: {name: 0 for name in students} for award in awards}
            st.session_state.total_voters = 0
            st.session_state.voted_names = []
            st.success("รีเซ็ตระบบเรียบร้อย!")
    else:
        st.info("กรุณาใส่รหัสผ่านเพื่อตั้งค่า")
        students = ["กรุณาให้ครูตั้งค่ารายชื่อ"]

# --- หน้าหลัก (ที่เด็กๆ เห็น) ---
st.title("🎓 กิจกรรมปัจฉิมนิเทศ")
st.markdown(f"### 🗳️ ตอนนี้โหวตแล้ว: `{st.session_state.total_voters}` คน")

# ส่วนของการโหวต
with st.container():
    with st.form("voting_form"):
        st.write("---")
        voter_name = st.text_input("ชื่อเล่นของคุณ (เพื่อยืนยันตัวตน)")
        
        selected_votes = {}
        for award in awards:
            selected_votes[award] = st.selectbox(f"โหวตให้ใคร: {award}", students, key=f"v_{award}")
        
        submitted = st.form_submit_button("🗳️ ส่งผลโหวตลงหีบ")
        
        if submitted:
            if not voter_name:
                st.warning("ใส่ชื่อตัวเองหน่อยนะจ๊ะ")
            elif voter_name in st.session_state.voted_names:
                st.error("คุณโหวตไปแล้วนะจ๊ะ แบ่งให้เพื่อนคนอื่นบ้าง!")
            else:
                # บันทึกคะแนน
                for award, student in selected_votes.items():
                    if award in st.session_state.votes:
                        st.session_state.votes[award][student] += 1
                
                st.session_state.total_voters += 1
                st.session_state.voted_names.append(voter_name)
                st.balloons() # เอฟเฟกต์ลูกโป่งส่วนตัวของเด็ก
                st.success("บันทึกคะแนนเรียบร้อย! รอดูผลพร้อมกันบนจอนะ")

# --- ส่วนการแสดงผล (ต้องใส่รหัสครูถึงจะกดดูได้) ---
st.write("---")
if teacher_pw == "1234":
    if st.checkbox("📢 เปิดหน้าจอประกาศผล (โชว์บนโปรเจกเตอร์)"):
        st.header("🏆 ผลการโหวต 'ที่สุดในรุ่น'")
        st.snow() # เอฟเฟกต์หิมะฉลองบนจอใหญ่
        
        for award in awards:
            with st.expander(f"คลิกเพื่อดูผู้ชนะรางวัล: {award}", expanded=False):
                current_data = st.session_state.votes.get(award, {})
                if current_data:
                    df = pd.DataFrame(current_data.items(), columns=['ชื่อเพื่อน', 'คะแนน'])
                    # เรียงจากมากไปน้อย
                    df = df.sort_values(by='คะแนน', ascending=False)
                    st.bar_chart(df.set_index('ชื่อเพื่อน'))
                    
                    winner = df.iloc[0]['ชื่อเพื่อน']
                    winning_score = df.iloc[0]['คะแนน']
                    if winning_score > 0:
                        st.success(f"🎊 ยินดีกับ **{winner}** ได้ไปทั้งหมด {winning_score} คะแนน!")
