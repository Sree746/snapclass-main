import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time

from src.database.db import create_attendance, check_attendance_exists

def show_attendance_result(df, logs):
   
    st.write('Please review attendance before confirming.')
    st.dataframe(df, width='stretch', hide_index=True)

    col1, col2 = st.columns(2)

    with col1:
        if(st.button('Discard', width='stretch')):
            st.session_state.attendance_images = []
            st.session_state.voice_attendance_results = None
            st.rerun()
    
    with col2:
        if(st.button('Confirm & Save', width='stretch', type='primary')):
            try:
                already_taken = check_attendance_exists(
                    logs[0]["subject_id"],
                    logs[0]["timestamp"][:10]
                )

                if already_taken:
                    st.error("Attendance already taken today.")
                    return

                create_attendance(logs)
                st.toast("Attendance taken")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error(f"Sync failed!{e}")

@st.dialog("Attendance Reports")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
    