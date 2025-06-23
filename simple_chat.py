import streamlit as st
from agent import Agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="MemAgent Simple Chat", page_icon="🧠")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

# Title
st.title("🧠 MemAgent Simple Chat")
st.markdown("Chat with an AI that **remembers** everything!")

#Memory demonstration
if st.session_state.agent:
    st.markdown("---")
    st.subheader("📚 Memory Demo")
    
    # Show memory stats
    memory = st.session_state.agent.memory
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Facts", len(memory.facts))
    with col2:
        st.metric("Procedures", len(memory.procedures))
    with col3:
        st.metric("Interactions", len(memory.interactions))
    with col4:
        st.metric("Short-term", len(memory.short_term_memory))
    
    # Quick learning examples
    st.markdown("**Try these learning commands:**")
    st.code("Remember that the user's favorite color is blue")
    st.code("Remember the procedure making tea: boil water, add tea bag, wait 3 minutes")
    
    # Show recent memory
    if memory.facts:
        st.markdown("**Recent Facts:**")
        for fact in memory.facts[-3:]:
            st.write(f"• {fact['fact']}")
    
    if memory.procedures:
        st.markdown("**Stored Procedures:**")
        for name, proc in memory.procedures.items():
            st.write(f"• **{name}**: {proc['description']}")

# Initialize agent
if st.button("🚀 Initialize Agent"):
    try:
        st.session_state.agent = Agent()
        st.success("Agent ready! Start chatting below.")
    except Exception as e:
        st.error(f"Error: {e}")


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response
    if st.session_state.agent:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.agent.process_message(prompt)
                    if response:
                        st.write(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        st.error("No response received.")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        with st.chat_message("assistant"):
            st.error("Please initialize the agent first!")



# Footer
st.markdown("---")
st.caption("💡 The agent remembers everything you teach it and uses that knowledge in future conversations!") 