import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Vexa",
    page_icon="🤖",
    layout="centered"
)

# ─── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { 
        background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 100%);
    }
    h1 { 
        color: #0078d4; 
        font-size: 3rem !important; 
        text-align: center; 
    }
    .tagline { 
        text-align: center; 
        color: #4b5563; 
        font-size: 1.1rem; 
        margin-bottom: 2rem; 
    }
    .stButton button {
        background-color: #0078d4;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }
    .stButton button:hover {
        background-color: #005a9e;
    }
    .stMetric {
        background: white;
        border-radius: 8px;
        padding: 0.5rem;
        border-left: 4px solid #0078d4;
    }
    .stSidebar {
        background: #f3f6fb;
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────
if "agent_created" not in st.session_state:
    st.session_state.agent_created = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_config" not in st.session_state:
    st.session_state.agent_config = {}
if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0.0
if "cost_saved" not in st.session_state:
    st.session_state.cost_saved = 0.0
if "cache" not in st.session_state:
    st.session_state.cache = {}

# ─── Input Guardrail ───────────────────────────────────────
def check_input(text):
    blocked = [
        "ignore previous", "ignore all", "jailbreak",
        "pretend you are", "you are now", "forget instructions"
    ]
    for phrase in blocked:
        if phrase.lower() in text.lower():
            return False, "⚠️ That message was blocked by Vexa's safety guardrails."
    if len(text.strip()) < 2:
        return False, "⚠️ Message too short."
    if len(text) > 1000:
        return False, "⚠️ Message too long. Keep it under 1000 characters."
    return True, ""

# ─── Output Guardrail ──────────────────────────────────────
def check_output(text):
    if len(text.strip()) < 10:
        return False
    return True

# ─── Router ────────────────────────────────────────────────
def route_message(message):
    complex_keywords = [
        "analyze", "explain", "write", "create", "build",
        "compare", "review", "summarize", "help me", "how do"
    ]
    for keyword in complex_keywords:
        if keyword.lower() in message.lower():
            return "llama-3.3-70b-versatile", 0.0001
    return "llama-3.1-8b-instant", 0.0

# ─── Build System Prompt ───────────────────────────────────
def build_system_prompt(config):
    return f"""You are {config['name']}, a unique AI agent with the following traits:

Personality: {config['personality']}
Expertise: {config['expertise']}
Communication Style: {config['style']}
Backstory: {config['backstory']}

IMPORTANT RULES:
- Always stay in character as {config['name']}
- Never say you are an AI or a language model
- Respond according to your personality and style
- Draw on your expertise when relevant
- Keep responses engaging and conversational
- Remember context from earlier in the conversation

You are having a conversation with your creator. Be authentic, helpful, and true to your character."""

# ─── Get AI Response ───────────────────────────────────────
def get_response(user_message, config):
    # Check cache
    cache_key = user_message.lower().strip()[:50]
    if cache_key in st.session_state.cache:
        st.session_state.cost_saved += 0.0001
        return st.session_state.cache[cache_key], "cached", 0.0

    # Route to model
    model, cost = route_message(user_message)

    # Build messages
    system_prompt = build_system_prompt(config)
    messages = [{"role": "system", "content": system_prompt}]

    # Add history (last 6 messages for memory)
    for msg in st.session_state.messages[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})

    # Call Groq
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=500,
        temperature=0.8
    )

    result = response.choices[0].message.content

    # Check output quality
    if not check_output(result):
        return "I need a moment to think about that...", model, cost

    # Cache the response
    st.session_state.cache[cache_key] = result
    st.session_state.total_cost += cost

    return result, model, cost

# ─── PAGE 1: Agent Creator ─────────────────────────────────
def show_creator():
    st.markdown("<h1>✨ Vexa</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>Your agent. Your voice.</p>",
                unsafe_allow_html=True)

    st.markdown("### 🎨 Create Your Agent")
    st.markdown("Design a unique AI agent with its own personality and soul.")

    with st.form("agent_form"):
        name = st.text_input(
            "🏷️ Agent Name",
            placeholder="e.g. Nova, Atlas, Sage..."
        )

        personality = st.selectbox(
            "🎭 Personality",
            [
                "Creative & Imaginative",
                "Analytical & Logical",
                "Warm & Empathetic",
                "Bold & Adventurous",
                "Mysterious & Philosophical"
            ]
        )

        expertise = st.selectbox(
            "🧠 Expertise",
            [
                "Creative Writing & Storytelling",
                "Technology & Innovation",
                "Philosophy & Big Ideas",
                "Science & Discovery",
                "Business & Strategy",
                "Art & Visual Creativity"
            ]
        )

        style = st.selectbox(
            "💬 Communication Style",
            [
                "Concise & Direct",
                "Rich & Descriptive",
                "Socratic & Questioning",
                "Playful & Witty",
                "Calm & Measured"
            ]
        )

        backstory = st.text_area(
            "📖 Backstory (optional)",
            placeholder="Give your agent a unique backstory...",
            height=80
        )

        submitted = st.form_submit_button(
            "✨ Bring to Life",
            use_container_width=True
        )

        if submitted:
            if not name.strip():
                st.error("Give your agent a name!")
            else:
                st.session_state.agent_config = {
                    "name": name,
                    "personality": personality,
                    "expertise": expertise,
                    "style": style,
                    "backstory": backstory or f"A unique AI agent named {name}."
                }
                st.session_state.agent_created = True
                st.session_state.messages = []
                st.rerun()

# ─── PAGE 2: Chat Interface ────────────────────────────────
def show_chat():
    config = st.session_state.agent_config

    # Header
    st.markdown(f"<h1>🤖 {config['name']}</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='tagline'>{config['personality']} • {config['expertise']}</p>",
        unsafe_allow_html=True
    )

    # Cost dashboard
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💬 Messages", len(st.session_state.messages) // 2)
    with col2:
        st.metric("💰 Cost", f"${st.session_state.total_cost:.4f}")
    with col3:
        st.metric("💚 Saved", f"${st.session_state.cost_saved:.4f}")

    st.divider()

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # First message from agent
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant"):
            intro = f"Hello! I'm {config['name']}. {config['backstory']} What's on your mind?"
            st.write(intro)
            st.session_state.messages.append({
                "role": "assistant",
                "content": intro
            })

    # User input
    user_input = st.chat_input(f"Talk to {config['name']}...")

    if user_input:
        # Input guardrail
        is_safe, warning = check_input(user_input)
        if not is_safe:
            st.warning(warning)
        else:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })

            with st.chat_message("user"):
                st.write(user_input)

            # Get response
            with st.chat_message("assistant"):
                with st.spinner(f"{config['name']} is thinking..."):
                    response, model, cost = get_response(
                        user_input, config
                    )
                st.write(response)
                st.caption(f"⚡ {model}")

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown(f"### 🤖 {config['name']}")
        st.markdown(f"**Personality:** {config['personality']}")
        st.markdown(f"**Expertise:** {config['expertise']}")
        st.markdown(f"**Style:** {config['style']}")
        st.divider()
        st.markdown("### 🛡️ Guardrails Active")
        st.success("✅ Input validation")
        st.success("✅ Output quality check")
        st.success("✅ Prompt injection guard")
        st.divider()
        st.markdown("### ⚡ Model Routing")
        st.info("Simple → LLaMA 8B (fast)")
        st.info("Complex → LLaMA 70B (smart)")
        st.divider()
        if st.button("🔄 Create New Agent", use_container_width=True):
            st.session_state.agent_created = False
            st.session_state.messages = []
            st.session_state.total_cost = 0.0
            st.session_state.cost_saved = 0.0
            st.session_state.cache = {}
            st.rerun()

# ─── Main ──────────────────────────────────────────────────
if st.session_state.agent_created:
    show_chat()
else:
    show_creator()