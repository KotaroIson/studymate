# main.py — StudyMate Gemini Full Edition
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import datetime
import os
import time

# ---------- SETUP ----------
st.set_page_config(page_title="StudyMate — AI Study Assistant", page_icon="🎓", layout="centered")
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ---------- HEADER ----------
st.title("🎓 StudyMate — AI Study Assistant")
st.caption("Your personal AI-powered learning companion for smarter, faster studying.")

# ---------- DEFINE TABS ----------
tabs = st.tabs(["📘 Summary", "❓ Questions", "💬 Chat Tutor", "🗓️ Planner", "📤 Export"])

with st.sidebar:
    st.header("About StudyMate")
    st.write("StudyMate helps students summarize topics, create questions, and learn faster — using Gemini AI.")
    st.write("Tip: paste a short article or notes (200–800 words) for best results.")
    st.markdown("---")
    st.write("🌐 Created by **Insar Bekmukhanbetov**")
    st.write("🔗 [GitHub](https://github.com/kotaroIson) | [LinkedIn](https://www.linkedin.com/in/insar-bekmukhanbetov/)")


# ---------- SUMMARY TAB ----------
with tabs[0]:
    st.header("📘 Text Summarizer")
    text = st.text_area("Paste your text or notes below:", height=220)
    if st.button("✨ Summarize"):
        if not text.strip():
            st.warning("Please enter some text first!")
        else:
            with st.spinner("Summarizing using Gemini..."):
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"Summarize the following text in 5–7 concise sentences:\n\n{text}"
                response = model.generate_content(prompt)
                st.success("✅ Summary generated:")
                st.write(response.text.strip())

# ---------- QUESTIONS TAB ----------
with tabs[1]:
    st.header("❓ Practice Question Generator")
    q_text = st.text_area("Enter a topic or paragraph:", height=220)
    num_q = st.slider("How many questions?", 3, 10, 5)
    include_explanations = st.checkbox("Include short answer explanations", value=True)

    if st.button("🧠 Generate Questions"):
        if not q_text.strip():
            st.warning("Please enter text or topic first!")
        else:
            with st.spinner("Generating questions with Gemini..."):
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = f"""
                You are StudyMate, an academic AI tutor.
                Generate {num_q} study questions about the following topic or text.
                Each question should be unique, clear, and suitable for high school or university students.
                {'Also include 1–2 sentence explanations after each question.' if include_explanations else ''}
                Text:
                {q_text}
                """
                response = model.generate_content(prompt)
                st.success("✅ Here are your questions:")
                st.markdown(response.text.strip())

# ---------- CHAT TUTOR TAB ----------
with tabs[2]:
    st.header("💬 AI Chat Tutor")
    st.write("Ask StudyMate anything — from math and science to writing tips.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Your question:")
    if st.button("💭 Ask"):
        if not user_input.strip():
            st.warning("Type a question first!")
        else:
            model = genai.GenerativeModel("gemini-2.5-flash")
            with st.spinner("Thinking..."):
                response = model.generate_content(
                    f"You are a friendly AI tutor. Answer clearly and educationally: {user_input}"
                )
                answer = response.text.strip()
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("StudyMate", answer))

    # Display chat history
    for speaker, msg in st.session_state.chat_history[-6:]:
        st.markdown(f"**{speaker}:** {msg}")

# ---------- PLANNER TAB ----------
with tabs[3]:
    st.header("🗓️ Study Planner")
    subject = st.text_input("Subject:")
    goal = st.text_input("Goal (e.g., 'Finish Chapter 5')")
    date = st.date_input("Deadline", datetime.date.today())

    if "plan" not in st.session_state:
        st.session_state.plan = []

    if st.button("➕ Add to Planner"):
        if subject and goal:
            st.session_state.plan.append((subject, goal, date))
            st.success("✅ Added to planner!")
        else:
            st.warning("Please fill in both fields.")

    st.write("### 📚 Your Study Plan:")
    if st.session_state.plan:
        for s, g, d in st.session_state.plan:
            st.markdown(f"📘 **{s}** — {g} _(due {d})_")
    else:
        st.info("No plans yet. Add one above!")

# ---------- EXPORT TAB ----------
with tabs[4]:
    st.header("📤 Export Study Pack")
    if st.button("📥 Download Study Summary"):
        content = "StudyMate Export\n\n"

        # Add plans
        if "plan" in st.session_state:
            content += "Your Study Plans:\n"
            for s, g, d in st.session_state.plan:
                content += f"📘 {s} — {g} (by {d})\n"
            content += "\n"

        # Add chat
        if "chat_history" in st.session_state:
            content += "Chat History:\n"
            for speaker, msg in st.session_state.chat_history[-6:]:
                content += f"{speaker}: {msg}\n"

        st.download_button("Download as TXT", content, file_name="studymate_export.txt")
