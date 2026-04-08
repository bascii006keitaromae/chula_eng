install streamlit google-generativeai
import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Course Assistant Bot", page_icon="🎓")
st.title("🎓 CSII Course Assistant")
st.markdown("Ask me anything about the **AI Integration For Digital Products and Services** course!")

# --- THE LOCAL KNOWLEDGE (Extracted from your PDF) ---
KNOWLEDGE_BASE = """
AI Integration For Digital Products and Services (Course 5607210) is a 3-credit elective
offered by the Chulalongkorn School of Integrated Innovation (CSII). Taught by Marko Niinimaki,
the course explores the practical application of Artificial Intelligence (AI) to enhance digital
products and services, from initial design to customer communication.

Core Objectives
The course aims to equip students with the ability to:
● Enhance Products: Explain how AI can improve digital products and services.
● Project Management: Apply AI tools to optimize project planning and execution.
● Design and Prototyping: Use AI to increase creativity and efficiency during the design phase.
● Content and Communication: Implement AI for content generation and professional communication.
● Ethical Awareness: Address the limitations, pitfalls, and ethical considerations of AI in a startup context.

Course Content & Key Topics
The curriculum moves from theoretical foundations to hands-on technical integration:
● Foundations: The history of AI, Machine Learning (supervised, unsupervised, and reinforcement learning), and the mechanics of Large Language Models (LLMs) and transformers.
● AI in Business: Segmenting AI use cases into customer interaction, intelligent products, and process automation.
● Prototyping: Integration of AI with physical prototyping, including 3D printing and laser cutting.
● Technical Integration: Developing "intelligent" software by adding AI services/models and vector databases to traditional software stacks.
● Advanced Concepts: Exploring agentic AI (software agents capable of autonomous action), AI-driven data analysis, and using APIs (like ClickUp or OpenAI) to automate workflows.

Schedule & Assessment
The course is structured around a semester-long project where students develop an actual digital product or service using AI tools.
● January: Introduction and foundational technologies.
● February: Focus on design, prototyping, and testing, culminating in midterm presentations.
● March: Customer communication and integrating AI into software.
● April: Ethics, avoiding over-reliance, and the final exam.
"""

# --- SIDEBAR ---
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    model_option = st.selectbox("Model:", ("gemini-2.5-flash", "gemini-2.5-pro"))
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- INITIALIZE CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- INITIALIZE GEMINI MODEL ---
def get_gemini_response(user_input, history):
    if not api_key:
        st.error("Please enter your API Key!")
        return None
    
    try:
        genai.configure(api_key=api_key)
        
        # System Instruction updated for the Course PDF
        model = genai.GenerativeModel(
            model_name=model_option,
            system_instruction=f"You are a helpful academic assistant for the Chulalongkorn School of Integrated Innovation (CSII). Use the following course syllabus to answer student questions: \n\n{KNOWLEDGE_BASE}\n\nIf the student asks something not covered in this syllabus, politely inform them that you do not have that information."
        )
        
        chat_session = model.start_chat(
            history=[
                {"role": m["role"], "parts": [m["content"]]} 
                for m in history if m["role"] != "system"
            ]
        )
        
        response = chat_session.send_message(user_input, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Ask a question about the syllabus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        response_stream = get_gemini_response(prompt, st.session_state.messages[:-1])
        
        if response_stream:
            for chunk in response_stream:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "model", "content": full_response})
