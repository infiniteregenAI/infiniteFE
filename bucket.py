import streamlit as st
import openai
import time
from datetime import datetime
import os
import dotenv
from agents import ConversationAgent
from document_generator import generate_summary_doc, create_formatted_docx
from storage import AgentStorage

# Load environment variables and setup
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def display_agent_info(agent_data):
    """Display agent information in a formatted way"""
    st.markdown(f"### **{agent_data['name']}** {agent_data['avatar']}")
    st.markdown("""
    - Role: {}
    - Expertise areas: {}
    """.format(
        agent_data['role'].capitalize(),
        ', '.join(agent_data.get('expertise', ['AI Conversation']))
    ))

def generate_document(messages, goal, agent1_name, agent2_name):
    """Generate and offer document download"""
    st.success("💫 Conversation completed! Generating detailed summary...")
    
    with st.spinner("Generating summary document..."):
        summary = generate_summary_doc(messages, goal)
        if summary:
            # Create and save document
            doc_io = create_formatted_docx(summary, goal, messages, agent1_name, agent2_name)
            
            if doc_io:
                st.success("✅ Document generated successfully!")
                # Create download button in a more prominent location
                st.markdown("### Download Your Summary")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📥 Download Detailed Summary Document",
                    data=doc_io,
                    file_name=f"solution_summary_{timestamp}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            else:
                st.error("Failed to generate document. Please try again.")

def main():
    st.title("🌱 Web3 x Regenerative Future Bucket")
    
    # Initialize storage and get available agents
    storage = AgentStorage()
    available_agents = storage.get_all_agents()
    
    if not available_agents:
        st.warning("No agents available. Please create some agents in the Agent Management page first!")
        return
    
    # Initialize session states
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_completed" not in st.session_state:
        st.session_state.conversation_completed = False
    
    # Conversation Setup Section
    st.header("Conversation Setup")
    
    # Agent Selection
    st.subheader("Select Participating Agents")
    col1, col2 = st.columns(2)
    
    selected_agents = []
    
    with col1:
        agent1_name = st.selectbox(
            "Select First Agent",
            options=[a['name'] for a in available_agents],
            key="agent1"
        )
        agent1_data = next(a for a in available_agents if a['name'] == agent1_name)
        selected_agents.append(agent1_data)
        display_agent_info(agent1_data)
    
    with col2:
        remaining_agents = [a['name'] for a in available_agents if a['name'] != agent1_name]
        agent2_name = st.selectbox(
            "Select Second Agent",
            options=remaining_agents,
            key="agent2"
        )
        if agent2_name:
            agent2_data = next(a for a in available_agents if a['name'] == agent2_name)
            selected_agents.append(agent2_data)
            display_agent_info(agent2_data)
    
    # Goal input
    st.subheader("Conversation Parameters")
    goal = st.text_input(
        "Enter an innovative goal:", 
        "Design a regenerative mechanism for funding public goods using quadratic funding and retroactive public goods funding"
    )
    
    # Conversation settings
    max_turns = st.slider("Number of Conversation Turns:", 5, 20, 10)
    
    # Chat Display Section
    st.header("Conversation")
    chat_container = st.container()
    
    # Display existing messages
    with chat_container:
        for message in st.session_state.messages:
            current_agent = next(
                a for a in selected_agents 
                if a['role'] == message["role"]
            )
            with st.chat_message(message["role"], avatar=current_agent['avatar']):
                st.markdown(f"**{current_agent['name']}**: {message['content']}")
    
    # Initialize agents
    if len(selected_agents) == 2:
        agent1 = ConversationAgent(
            name=selected_agents[0]['name'],
            role=selected_agents[0]['role'],
            personality=selected_agents[0]['personality']
        )
        agent2 = ConversationAgent(
            name=selected_agents[1]['name'],
            role=selected_agents[1]['role'],
            personality=selected_agents[1]['personality']
        )
        
        # Control buttons
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            start_button = st.button("Start Conversation")
        with col2:
            reset_button = st.button("Reset Conversation")
        with col3:
            if st.session_state.messages and not st.session_state.conversation_completed:
                generate_button = st.button("Generate Summary")
            
        if start_button:
            st.session_state.messages = []
            st.session_state.conversation_completed = False
            
            for turn in range(max_turns):
                # Determine current agent
                current_agent = agent1 if turn % 2 == 0 else agent2
                current_agent_data = selected_agents[0] if turn % 2 == 0 else selected_agents[1]
                
                # Generate and display response
                with st.chat_message(current_agent.role, avatar=current_agent_data['avatar']):
                    message_placeholder = st.empty()
                    full_response = ""
                    
                    # Initialize conversation with the goal if it's the first message
                    if len(st.session_state.messages) == 0:
                        conversation_starter = (
                            f"""Let's delve into this topic: {goal}.
                            To begin, let's explore the core principles, challenges, and potential strategies or innovations that could be applied."""
                        )
                        messages_with_context = [{"role": "user", "content": conversation_starter}]
                    else:
                        messages_with_context = st.session_state.messages
                    
                    # Stream the response
                    for chunk in current_agent.get_response(messages_with_context):
                        if hasattr(chunk.choices[0].delta, 'content'):
                            content = chunk.choices[0].delta.content
                            if content is not None:
                                full_response += content
                                message_placeholder.markdown(
                                    f"**{current_agent.name}**: {full_response}"
                                )
                    
                    # Add message to session state
                    st.session_state.messages.append({
                        "role": current_agent.role,
                        "content": full_response
                    })
                
                # Add slight delay between turns
                time.sleep(0.5)
            
            # Mark conversation as completed after all turns
            st.session_state.conversation_completed = True
            # Generate document after conversation completion
            agent1_doc_name = agent1_data['avatar'] + " " + agent1_data['name']
            agent2_doc_name = agent2_data['avatar'] + " " + agent2_data['name']
            generate_document(st.session_state.messages, goal, agent1_doc_name, agent2_doc_name)
        
        # Handle manual generation
        if 'generate_button' in locals() and generate_button:
            generate_document(st.session_state.messages, goal, agent1_doc_name, agent2_doc_name)
        
        if reset_button:
            st.session_state.messages = []
            st.session_state.conversation_completed = False
            st.rerun()

if __name__ == "__main__":
    main()