from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from fastapi import BackgroundTasks
import traceback
from ..models import ConversationInput, GenerateDocumentInput
from ..core.agent_manager import AgentManager
from ..core.conversation_manager import ConversationManager
from ..core.document_generator import DocumentGenerator
import traceback
import json
import os
import aiofiles
import asyncio

router = APIRouter()
agent_manager = AgentManager()

@router.post("/conversation/{agent_id}/chat")
async def chat(agent_id: str, conversation: ConversationInput):
    """
        This api endpoint is used to chat with an agent.
        
        Args :
            agent_id (str) : The id of the agent.
            conversation (ConversationInput) : The conversation details.
            
        Returns :
            List[Message] : The conversation messages.
    """
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    messages = []
    for message in conversation.messages:
        if message.agent_id != agent_id:
            messages.append({
                "role": "user",
                "content": message.content
            })
        else:
            messages.append({
                "role": "assistant",
                "content": message.content
            })
    
    conv_manager = ConversationManager(agent)
    return StreamingResponse(
        conv_manager.get_response(messages),
        media_type="text/plain"
    )


@router.get("/conversation")
async def chat():
    """
        This api endpoint is used to chat with an agent.
        
        Args :
            agent_id (str) : The id of the agent.
            conversation (ConversationInput) : The conversation details.
            
        Returns :
            List[Message] : The conversation messages.
    """
    agent_id = "1"
    
    messages = [
        {
            "role": "user",
            "content": "Generate a 1000 words essay on green plants."
        }
    ]
    
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    messages = []
    for message in messages:
        if message.agent_id != agent_id:
            messages.append({
                "role": "user",
                "content": message.content
            })
        else:
            messages.append({
                "role": "assistant",
                "content": message.content
            })
    
    conv_manager = ConversationManager(agent)
    return StreamingResponse(
        conv_manager.get_response(messages),
        media_type="text/plain"
    )

@router.post("/conversation/generate-document")
async def generate_document(conversation: GenerateDocumentInput):
    """
    This API endpoint generates a Word document from the conversation.
    
    Args:
        conversation (GenerateDocumentInput): The conversation details.
        
    Returns:
        StreamingResponse: The generated document as a downloadable Word file.
    """
    try:
        # Prepare messages and goal
        messages = [
            {"role": message.role, "content": message.content}
            for message in conversation.messages
        ]
        goal = conversation.goal

        # Generate summary and document
        summary = DocumentGenerator.generate_summary(messages)
        doc_io = DocumentGenerator.create_document(summary, goal, messages)

        # Return the document as a downloadable file
        return StreamingResponse(
            doc_io,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename=conversation_summary.docx"}
        )
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/conversation/{conversation_id}/chat-between-n-agents")
async def chat_between_n_agents(conversation_id: str, agent_ids: list[str], number_of_exchanges: int, goal: str, background_tasks: BackgroundTasks):
    if len(agent_ids) < 2:
        raise HTTPException(status_code=400, detail="At least two agents are required for the conversation")

    agents = []
    try:
        with open("agents.json", "r") as f:
            agents_data = json.load(f)
            for agent_id in agent_ids:
                agent = next((agent for agent in agents_data if agent["id"] == agent_id), None)
                if not agent:
                    raise HTTPException(status_code=404, detail=f"Agent with id {agent_id} not found in agents.json")
                agents.append(agent)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="agents.json not found")

    conversation_managers = []
    for agent in agents:
        agent_instance = agent_manager.get_agent(agent["id"])
        if not agent_instance:
            raise HTTPException(status_code=404, detail=f"Agent with id {agent['id']} not found")
        conversation_managers.append((agent["name"], ConversationManager(agent_instance)))

    file_path = f"conversations_JSON/{conversation_id}.json"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    conversation = {
        "conversation_id": conversation_id,
        "goal": goal,
        "messages": []
    }
    with open(file_path, "w") as f:
        json.dump(conversation, f, indent=4)

    concise_prompt = f"""Respond thoughtfully and analytically to the previous message, either expanding upon or questioning its points. Use specific examples, avoid repetition, and ensure your response reflects your unique personality and perspective. Stay concise (2-3 sentences)."""
    temp_messages = [
        {"role": "system", "content": f"Let's delve into this topic: {goal}. Respond in a manner that aligns with your personality while following this approach: {concise_prompt}"}
    ]

    async def write_to_file(message):
        try:
            async with aiofiles.open(file_path, "r+") as file:
                data = await file.read()
                data_json = json.loads(data)
                data_json["messages"].append(message)
                await file.seek(0)
                await file.truncate()
                await file.write(json.dumps(data_json, indent=4))
        except Exception as e:
            print(f"Error writing to file: {str(e)}")

    async def event_generator():
        try:
            for exchange in range(number_of_exchanges):
                for agent_idx, (agent_name, conv_manager) in enumerate(conversation_managers):
                    current_message = {"role": agent_name, "content": ""}
                    
                    yield f"\nAgent {agent_name} (Exchange {exchange + 1}):\n"
                    
                    async for chunk in conv_manager.get_response(temp_messages):
                        if isinstance(chunk, str) and chunk.strip():
                            yield chunk
                            current_message["content"] += chunk
                            await asyncio.sleep(0)  
                    
                    temp_messages.append({
                        "role": "assistant" if temp_messages[-1]["role"] == "user" else "user",
                        "content": current_message["content"]
                    })
                    
                    background_tasks.add_task(write_to_file, current_message)
                    
                    yield "\n---\n"

        except Exception as e:
            print(f"Error in event_generator: {traceback.format_exc()}")
            yield f"Error: {str(e)}\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no"  
        }
    )

@router.get("/conversation/{conversation_id}/multi-agent-chat")
async def get_multi_agent_chat(conversation_id: str):
    file_path = f"conversations_JSON/{conversation_id}.json"
    try:
        with open(file_path, "r") as file:
            conversation = json.load(file)
        return conversation
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Conversation not found")

@router.post("/conversation/{conversation_id}/generate-document-with-multi-agent-chat")
async def generate_document_with_multi_agent_chat(conversation_id: str):
    """
    This API endpoint generates a Word document from a multi-agent chat conversation.
    
    Args:
        conversation_id (str): The ID of the conversation file.
        
    Returns:
        StreamingResponse: The generated document as a downloadable Word file.
    """
    file_path = f"conversations_JSON/{conversation_id}.json"
    try:
        # Read the conversation JSON file
        with open(file_path, "r") as file:
            conversation = json.load(file)

        # Generate the summary
        try:
            summary = DocumentGenerator.generate_summary(conversation["messages"])
        except Exception as e:
            print(f"Error in generate_summary: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail="Error generating document summary")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Conversation not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON structure: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    # Create the Word document
    doc_io = DocumentGenerator.create_document(
        summary,
        conversation["goal"],
        conversation["messages"]
    )

    # Return the document as a downloadable file
    return StreamingResponse(
        doc_io,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename={conversation_id}_summary.docx"
        }
    )
