import streamlit as st
from storage import AgentStorage
import os
import tempfile
from document_processor import AgentDocumentProcessor

def render_agent_template():
    """Return a template for agent personality configuration."""
    return """Define the agent's personality and behavior:

1. CORE TRAITS:
- [List 3-4 key personality traits]
- [Describe behavioral characteristics]
- [Define key values and principles]

2. COMMUNICATION STYLE:
- [Describe how the agent communicates]
- [Define tone and language preferences]
- [Specify any unique speech patterns]

3. KNOWLEDGE BASE:
- [List primary areas of expertise]
- [Define experience level in each area]
- [Specify technical knowledge]

4. KEY PERSPECTIVES:
- [List main viewpoints on relevant topics]
- [Define approach to problem-solving]
- [Describe decision-making style]

5. INTERACTION RULES:
- [Define how to handle disagreements]
- [Specify collaboration style]
- [List any behavioral constraints]"""

def display_knowledge_base_status(agent_data):
    """Display the status of an agent's knowledge base."""
    if agent_data.get('has_knowledge_base', False):
        st.info(f"📚 Knowledge Base: {agent_data.get('document_count', 0)} documents processed")
    else:
        st.info("📚 No knowledge base documents")

def handle_document_upload(agent_id, uploaded_files):
    """Process uploaded documents for an agent."""
    if not uploaded_files:
        return True, "No documents to process"
    
    try:
        processor = AgentDocumentProcessor(
            agent_id=agent_id,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        results = []
        for file in uploaded_files:
            success, message = processor.add_document(file)
            results.append((success, message))
        
        # Check if any processing failed
        failures = [msg for success, msg in results if not success]
        if failures:
            return False, "\n".join(failures)
        
        return True, f"Successfully processed {len(uploaded_files)} documents"
    
    except Exception as e:
        return False, f"Error processing documents: {str(e)}"

def agent_management_page():
    st.title("🤖 Agent Management")
    
    # Initialize storage
    storage = AgentStorage()
    
    # Create new agent section
    st.header("Create New Agent")
    
    with st.form("new_agent_form", clear_on_submit=True):
        st.subheader("Basic Configuration")
        
        # Basic agent details
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Agent Name", placeholder="e.g., EcoTech Expert")
            role = st.selectbox("Role", ["user", "assistant"])
        
        with col2:
            avatar = st.text_input("Avatar Emoji", placeholder="e.g., 🤖")
            expertise = st.text_input(
                "Areas of Expertise (comma-separated)", 
                placeholder="e.g., Climate Tech, Tokenomics, DAOs"
            )
        
        # Personality configuration
        st.subheader("Personality Configuration")
        personality = st.text_area(
            "Personality Definition",
            value=render_agent_template(),
            height=400
        )
        
        # Document upload section
        st.subheader("Knowledge Base (Optional)")
        uploaded_files = st.file_uploader(
            "Upload PDF or TXT files for agent's knowledge base",
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            help="These documents will be processed and used to enhance the agent's knowledge."
        )
        
        # Submit button
        submitted = st.form_submit_button("Create Agent")
        
        if submitted and name and personality:
            with st.spinner("Creating agent..."):
                # Process expertise into list
                expertise_list = [x.strip() for x in expertise.split(',')] if expertise else []
                
                new_agent = {
                    "name": name,
                    "role": role,
                    "avatar": avatar if avatar else "🤖",
                    "expertise": expertise_list,
                    "personality": personality,
                    "documents": uploaded_files if uploaded_files else []
                }
                
                # Add agent and process documents
                agent_id = storage.add_agent(new_agent)
                
                if uploaded_files:
                    success, message = handle_document_upload(agent_id, uploaded_files)
                    if success:
                        st.success(f"✨ Agent {name} created successfully with documents processed!")
                    else:
                        st.warning(f"Agent created but there were issues with documents: {message}")
                else:
                    st.success(f"✨ Agent {name} created successfully!")
                
                st.rerun()
    
    # List and manage existing agents
    st.header("Existing Agents")
    agents = storage.get_all_agents()
    
    if not agents:
        st.info("No agents created yet. Use the form above to create your first agent!")
        return
    
    for agent in agents:
        with st.expander(f"{agent.get('avatar', '🤖')} {agent['name']}"):
            # Display current knowledge base status
            display_knowledge_base_status(agent)
            
            with st.form(f"edit_agent_{agent['id']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    updated_name = st.text_input(
                        "Name", 
                        value=agent['name'], 
                        key=f"name_{agent['id']}"
                    )
                    updated_role = st.selectbox(
                        "Role", 
                        ["user", "assistant"],
                        index=0 if agent['role'] == "user" else 1,
                        key=f"role_{agent['id']}"
                    )
                
                with col2:
                    updated_avatar = st.text_input(
                        "Avatar", 
                        value=agent.get('avatar', '🤖'),
                        key=f"avatar_{agent['id']}"
                    )
                    updated_expertise = st.text_input(
                        "Areas of Expertise (comma-separated)",
                        value=', '.join(agent.get('expertise', [])),
                        key=f"expertise_{agent['id']}"
                    )
                
                updated_personality = st.text_area(
                    "Personality",
                    value=agent['personality'],
                    height=300,
                    key=f"personality_{agent['id']}"
                )
                
                # Additional document upload for existing agent
                new_documents = st.file_uploader(
                    "Add More Documents to Knowledge Base",
                    type=['pdf', 'txt'],
                    accept_multiple_files=True,
                    key=f"docs_{agent['id']}"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    update_button = st.form_submit_button("Update Agent")
                with col2:
                    delete_button = st.form_submit_button(
                        "Delete Agent", 
                        type="secondary",
                        use_container_width=True
                    )
                
                if update_button:
                    # Update agent configuration
                    updated_agent = {
                        "name": updated_name,
                        "role": updated_role,
                        "avatar": updated_avatar,
                        "expertise": [x.strip() for x in updated_expertise.split(',')],
                        "personality": updated_personality,
                        "has_knowledge_base": agent.get('has_knowledge_base', False),
                        "document_count": agent.get('document_count', 0)
                    }
                    
                    storage.update_agent(agent['id'], updated_agent)
                    
                    # Process any new documents
                    if new_documents:
                        success, message = handle_document_upload(agent['id'], new_documents)
                        if success:
                            st.success("✅ Agent updated and new documents processed successfully!")
                        else:
                            st.warning(f"Agent updated but there were issues with documents: {message}")
                    else:
                        st.success("✅ Agent updated successfully!")
                    
                    st.rerun()
                
                if delete_button:
                    if storage.delete_agent(agent['id']):
                        st.success("🗑️ Agent deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete agent. Please try again.")

if __name__ == "__main__":
    agent_management_page()