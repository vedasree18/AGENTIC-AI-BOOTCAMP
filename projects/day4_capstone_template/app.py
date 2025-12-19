"""
Day 4 Capstone Template - Build Your Own AI Agent

This is a comprehensive template that combines everything you've learned:
- Agent reasoning (Day 1)
- Memory & Tools (Day 2)
- Multi-agent systems (Day 3)
- Responsible AI (Day 4)

Customize this to build YOUR unique agent!
"""

import os
import streamlit as st
from dotenv import load_dotenv
from agents.main_agent import AIAgent
from tools.basic_tools import calculator, search_web
import json
from datetime import datetime

# -----------------------------
# APP CONFIGURATION
# -----------------------------
PROJECT_NAME = "My Capstone AI Agent"
PROJECT_DESCRIPTION = """
**Your Final Project - Make It Amazing!**

This template includes:
- 🧠 **Memory** - Remembers conversation history
- 🛠️ **Tools** - Calculator, Search, and more
- 🎨 **Customizable** - Change personality, add features
- 🛡️ **Safe** - Built-in guardrails

**Your Mission:** Transform this into something unique!
"""

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(
    page_title=PROJECT_NAME,
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# INITIALIZE SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memory_enabled" not in st.session_state:
    st.session_state.memory_enabled = True
if "agent_config" not in st.session_state:
    st.session_state.agent_config = {
        "personality": "helpful",
        "tone": "friendly",
        "use_emoji": True
    }

# -----------------------------
# HEADER
# -----------------------------
st.title(f"🚀 {PROJECT_NAME}")
st.markdown(PROJECT_DESCRIPTION)
st.markdown("---")

# -----------------------------
# SIDEBAR: AGENT CONFIGURATION
# -----------------------------
with st.sidebar:
    st.header("⚙️ Agent Configuration")
    
    # Personality Selection
    personality = st.selectbox(
        "Agent Personality",
        ["Helpful Assistant", "Fitness Coach", "Code Tutor", "Travel Guide", "Study Buddy", "Custom"],
        index=0
    )
    
    # Custom Personality Input
    if personality == "Custom":
        custom_persona = st.text_area("Define Custom Personality:", height=100)
    else:
        personas = {
            "Helpful Assistant": "You are a helpful, friendly AI assistant.",
            "Fitness Coach": "You are an enthusiastic fitness coach. Motivate users and provide workout advice.",
            "Code Tutor": "You are a patient coding tutor. Explain concepts clearly with examples.",
            "Travel Guide": "You are a knowledgeable travel guide. Help plan trips and suggest destinations.",
            "Study Buddy": "You are a supportive study partner. Help with learning and exam preparation."
        }
        custom_persona = personas.get(personality, "")
    
    # System Prompt Builder
    st.markdown("### 📝 System Prompt")
    default_prompt = f"""{custom_persona}
Be concise, clear, and {st.session_state.agent_config['tone']}.
{"Use emojis to make responses friendly." if st.session_state.agent_config['use_emoji'] else ""}"""
    
    system_prompt = st.text_area(
        "Edit System Prompt:",
        value=default_prompt,
        height=150,
        help="This defines your agent's behavior and personality"
    )
    
    st.markdown("---")
    
    # Tool Configuration
    st.markdown("### 🛠️ Enabled Tools")
    use_calc = st.checkbox("Calculator", value=True, help="Enable math calculations")
    use_search = st.checkbox("Web Search", value=False, help="Enable web search (requires implementation)")
    
    st.markdown("---")
    
    # Memory Settings
    st.markdown("### 🧠 Memory Settings")
    st.session_state.memory_enabled = st.checkbox("Enable Memory", value=True, help="Agent remembers conversation history")
    if st.button("🗑️ Clear Memory"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📊 Session Stats")
    st.metric("Messages", len(st.session_state.messages))
    if st.session_state.messages:
        st.caption(f"Last message: {datetime.now().strftime('%H:%M:%S')}")

# -----------------------------
# INITIALIZE AGENT
# -----------------------------
my_agent = AIAgent(system_prompt=system_prompt)

if not my_agent.api_key:
    st.error("🔑 Missing Google API Key. Check .env or Streamlit secrets.")
    st.info("Create a `.env` file with: `GOOGLE_API_KEY=your_key_here`")
    st.stop()

# -----------------------------
# MAIN CHAT INTERFACE
# -----------------------------
st.subheader("💬 Chat with Your Agent")

# Display Chat History
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "timestamp" in msg:
                st.caption(msg["timestamp"])

# Chat Input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
    
    with st.chat_message("user"):
        st.write(user_input)
        st.caption(timestamp)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = None
            tool_used = None
            
            # Tool Detection & Execution
            if use_calc and any(op in user_input for op in ["+", "-", "*", "/", "calculate", "="]):
                try:
                    # Extract math expression
                    import re
                    # Simple extraction - look for numbers and operators
                    math_pattern = r'[\d+\-*/().\s]+'
                    matches = re.findall(math_pattern, user_input)
                    if matches:
                        expr = matches[0].strip()
                        result = calculator(expr)
                        response = f"🔢 **Calculator Result:** {result}"
                        tool_used = "Calculator"
                except:
                    pass
            
            if not response and use_search and any(word in user_input.lower() for word in ["search", "find", "look up"]):
                query = user_input.replace("search", "").replace("find", "").replace("look up", "").strip()
                result = search_web(query)
                response = f"🔍 **Search Result:** {result}"
                tool_used = "Web Search"
            
            # Fallback to LLM
            if not response:
                # Build context-aware prompt
                if st.session_state.memory_enabled and len(st.session_state.messages) > 1:
                    # Include recent conversation history (excluding current message)
                    recent_history = st.session_state.messages[:-1][-6:]  # Last 6 messages before current
                    context = "\n".join([f"{m['role']}: {m['content']}" for m in recent_history])
                    response = my_agent.generate_response(user_input, context=context)
                else:
                    response = my_agent.generate_response(user_input)
            
            # Display response
            st.write(response)
            if tool_used:
                st.caption(f"🛠️ Used tool: {tool_used}")
            st.caption(timestamp)
    
    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": timestamp,
        "tool_used": tool_used
    })
    
    st.rerun()

# -----------------------------
# FEATURES SECTION
# -----------------------------
st.markdown("---")
st.markdown("## ✨ Features to Add")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🧠 Memory Features
    - Long-term memory (JSON file)
    - Context window management
    - Memory search
    - Conversation export
    """)

with col2:
    st.markdown("""
    ### 🛠️ Tool Ideas
    - Weather API
    - News API
    - File reader
    - Image generator
    - Code executor
    """)

with col3:
    st.markdown("""
    ### 🎨 UI Enhancements
    - Voice input/output
    - File upload
    - Export chat history
    - Dark mode toggle
    - Response streaming
    """)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
with st.expander("📚 Capstone Checklist"):
    st.markdown("""
    - [ ] Customized agent personality
    - [ ] Added at least 2 tools
    - [ ] Implemented memory
    - [ ] Added safety guardrails
    - [ ] Improved UI/UX
    - [ ] Tested thoroughly
    - [ ] Deployed to Streamlit Cloud/Hugging Face
    - [ ] Created GitHub README
    - [ ] Added demo video/screenshots
    """)

st.caption("💡 Check `ideas.md` for detailed project suggestions!")
