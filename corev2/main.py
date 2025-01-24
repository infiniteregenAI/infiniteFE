import traceback
from fastapi import FastAPI, HTTPException
from agent_manager import AgentManager
from models import (
    CreateAgentRequest, 
    CreateAgentResponse, 
    CreateTeamRequest, 
    CreateTeamResponse, 
    AgentResponse
)
from phi.agent import Agent

app = FastAPI()
agent_manager = AgentManager()

AVAILABLE_TOOLS = ["HackerNews", "DuckDuckGo", "Newspaper4k"]

@app.get("/available-tools/")
async def get_available_tools():
    """
    Endpoint to retrieve all available tools.
    
    Returns a list of available tools in the format:
    {
      "available_tools": ["HackerNews", "DuckDuckGo", "Newspaper4k"]
    }
    """
    return {"available_tools": AVAILABLE_TOOLS}

@app.post("/create-agent/", response_model=CreateAgentResponse)
async def create_agent(request: CreateAgentRequest):
    """
    Endpoint to create a new agent.
    Accepts request in the format:
    {
      "name": "Agent1",
      "role": "Data Retriever",
      "tools": ["HackerNews", "DuckDuckGo"],
      "description": "You are a senior NYT researcher writing an article on a topic.",
      "instructions": [
        "For a given topic, search for the top 5 links.",
        "Then read each URL and extract the article text, if a URL isn't available, ignore it.",
        "Analyse and prepare an NYT worthy article based on the information."
      ],
      "urls": ["https://example.com", "https://example.org"]  # Optional field
    }
    """
    # Validate tools
    invalid_tools = [tool for tool in request.tools if tool not in AVAILABLE_TOOLS]
    if invalid_tools:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid tools selected: {', '.join(invalid_tools)}. Available tools are: {', '.join(AVAILABLE_TOOLS)}."
        )
    
    try:
        # Create agent using AgentManager
        agent = agent_manager.create_agent(
            name=request.name,
            role=request.role,
            tools=request.tools,
            description=request.description,
            instructions=request.instructions,
            urls=request.urls,  
        )
        
        # Return response using the Pydantic models
        return CreateAgentResponse(
            message="Agent created successfully",
            agent=AgentResponse(
                id=agent.id,
                name=agent.name,
                role=agent.role,
                tools=request.tools,
                description=request.description,
                instructions=request.instructions,
                urls=request.urls,  
                markdown=True,
                show_tool_calls=True,
                add_datetime_to_instructions=True
            )
        )
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))
      
@app.post("/create-team/", response_model=CreateTeamResponse)
async def create_team(request: CreateTeamRequest):
    """
    Endpoint to create a new team of agents using agent names.
    Accepts request in the format:
    {
        "name": "Research Team",
        "agent_names": ["HN Researcher", "Web Searcher", "Article Reader"],
        "instructions": [
            "First, search hackernews for what the user is asking about.",
            "Then, ask the article reader to read the links for the stories.",
            "Finally, provide a summary."
        ]
    }
    """
    try:
        team = agent_manager.create_team(
            name=request.name,
            agent_names=request.agent_names,
            instructions=request.instructions,
        )
        
        return CreateTeamResponse(
            message="Team created successfully",
            team=team
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/update-agent/{agent_name}", response_model=CreateAgentResponse)
async def update_agent(agent_name: str, request: CreateAgentRequest):
    """
    Endpoint to update an existing agent.
    Accepts request in the format:
    {
      "name": "Agent1",
      "role": "Data Retriever",
      "tools": ["HackerNews", "DuckDuckGo"],
      "description": "You are a senior NYT researcher writing an article on a topic.",
      "instructions": [
        "For a given topic, search for the top 5 links.",
        "Then read each URL and extract the article text, if a URL isn't available, ignore it.",
        "Analyse and prepare an NYT worthy article based on the information."
      ],
      "urls": ["https://example.com", "https://example.org"]  # Optional field
    }
    """
    # Validate tools
    invalid_tools = [tool for tool in request.tools if tool not in AVAILABLE_TOOLS]
    if invalid_tools:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid tools selected: {', '.join(invalid_tools)}. Available tools are: {', '.join(AVAILABLE_TOOLS)}."
        )
    
    try:
        # Update agent using AgentManager
        agent = agent_manager.update_agent(
            name=agent_name,
            role=request.role,
            tools=request.tools,
            description=request.description,
            instructions=request.instructions,
            urls=request.urls,  
        )
        
        return CreateAgentResponse(
            message="Agent updated successfully",
            agent=AgentResponse(
                id=agent.id,
                name=agent.name,
                role=agent.role,
                tools=request.tools,
                description=request.description,
                instructions=request.instructions,
                urls=request.urls,  
                markdown=True,
                show_tool_calls=True,
                add_datetime_to_instructions=True
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 