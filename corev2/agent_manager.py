from typing import List, Dict, Any
import json
import os
from phi.agent import Agent
from phi.tools.hackernews import HackerNews
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k
from models import AgentResponse, TeamResponse

class AgentManager:
    """
    Manages the creation, storage, and retrieval of agents and teams.
    
    Attributes:
        storage_path (str): Path to the JSON file storing agent data
        team_storage_path (str): Path to the JSON file storing team data
    """
    
    def __init__(self, storage_path: str = "agents.json", team_storage_path: str = "teams.json"):
        """
        Initialize the AgentManager.
        
        Args:
            storage_path (str): Path for storing agent data
            team_storage_path (str): Path for storing team data
        """
        self.storage_path = storage_path
        self.team_storage_path = team_storage_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Create storage files if they don't exist."""
        for path in [self.storage_path, self.team_storage_path]:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump([], f)

    def _initialize_tool(self, tool_name: str) -> Any:
        """
        Initialize a tool instance based on the tool name.
        
        Args:
            tool_name (str): Name of the tool to initialize
            
        Returns:
            Tool instance or None if tool not found
        """
        tool_map = {
            "HackerNews": HackerNews(),
            "DuckDuckGo": DuckDuckGo(),
            "Newspaper4k": Newspaper4k(),
        }
        return tool_map.get(tool_name)

    def create_agent(self, name: str, role: str, tools: List[str], 
                    description: str, instructions: List[str], 
                    urls: List[str] = None) -> AgentResponse: 
        """
        Create a new agent and save it to storage.
        
        Args:
            name (str): Name of the agent
            role (str): Role of the agent
            tools (List[str]): List of tool names the agent can use
            description (str): Description of the agent
            instructions (List[str]): List of instructions for the agent
            urls (List[str], optional): List of URLs for the agent to use
            
        Returns:
            AgentResponse: Created agent data
        """
        # Get existing agents and generate new ID
        agents = self.get_all_agents()
        agent_id = str(len(agents) + 1)

        # Initialize urls if None
        urls = urls or []

        # Create agent instance with tools
        tool_instances = [self._initialize_tool(tool) for tool in tools]
        agent = Agent(
            name=name,
            role=role,
            tools=tool_instances,
            description=description,
            instructions=instructions,
            markdown=True,
            show_tool_calls=True,
            add_datetime_to_instructions=True,
        )

        # Create response model
        agent_data = AgentResponse(
            id=agent_id,
            name=name,
            role=role,
            tools=tools,
            description=description,
            instructions=instructions,
            urls=urls,  
            markdown=True,
            show_tool_calls=True,
            add_datetime_to_instructions=True,
        )

        # Save to storage
        agents.append(agent_data.dict())
        with open(self.storage_path, 'w') as f:
            json.dump(agents, f, indent=2)

        return agent_data

    def get_all_agents(self) -> List[Dict]:
        """
        Retrieve all agents from storage.
        
        Returns:
            List[Dict]: List of all stored agents
        """
        with open(self.storage_path, 'r') as f:
            return json.load(f)

    def get_agent_by_name(self, agent_name: str) -> Agent:
        """
        Get an agent instance by its name.
        
        Args:
            agent_name (str): Name of the agent to retrieve
            
        Returns:
            Agent: Initialized agent instance
            
        Raises:
            ValueError: If agent not found
        """
        agents = self.get_all_agents()
        agent_data = next((a for a in agents if a['name'] == agent_name), None)
        
        if not agent_data:
            raise ValueError(f"Agent with name '{agent_name}' not found")
        
        # Initialize tools and create agent instance
        tool_instances = [self._initialize_tool(tool) for tool in agent_data['tools']]
        return Agent(
            name=agent_data['name'],
            role=agent_data['role'],
            tools=tool_instances,
            description=agent_data['description'],
            instructions=agent_data['instructions'],
            markdown=agent_data['markdown'],
            show_tool_calls=agent_data['show_tool_calls'],
            add_datetime_to_instructions=agent_data['add_datetime_to_instructions']
        )

    def create_team(self, name: str, agent_names: List[str], 
                instructions: List[str]) -> TeamResponse:
        """
        Create a new team from existing agents.
        
        Args:
            name (str): Name of the team
            agent_names (List[str]): List of agent names to include in the team
            instructions (List[str]): List of instructions for the team
            
        Returns:
            TeamResponse: Created team data
            
        Raises:
            ValueError: If any agent is not found or if less than two agents are provided
        """
        # Validate that at least two agents are provided
        if len(agent_names) < 2:
            raise ValueError("At least two agents are required to create a team.")
        
        teams = self.get_all_teams()
        team_id = str(len(teams) + 1)

        # Initialize all agents for the team
        agent_instances = []
        agent_responses = []
        
        for agent_name in agent_names:
            # Find agent data
            agent_data = next(
                (a for a in self.get_all_agents() if a['name'] == agent_name), 
                None
            )
            if not agent_data:
                raise ValueError(f"Agent with name '{agent_name}' not found")
            
            # Create agent instance and response
            agent_instances.append(self.get_agent_by_name(agent_name))
            agent_responses.append(AgentResponse(**agent_data))

        # Create team instance
        team = Agent(
            name=name,
            team=agent_instances,
            instructions=instructions,
            show_tool_calls=True,
            markdown=True
        )

        # Create team response
        team_data = TeamResponse(
            id=team_id,
            name=name,
            agents=agent_responses,
            instructions=instructions,
            markdown=True,
            show_tool_calls=True
        )

        # Save to storage
        teams.append(team_data.dict())
        with open(self.team_storage_path, 'w') as f:
            json.dump(teams, f, indent=2)

        return team_data

    def get_all_teams(self) -> List[Dict]:
        """
        Retrieve all teams from storage.
        
        Returns:
            List[Dict]: List of all stored teams
        """
        with open(self.team_storage_path, 'r') as f:
            return json.load(f)

    def get_team_by_name(self, team_name: str) -> TeamResponse:
        """
        Get a team by its name.
        
        Args:
            team_name (str): Name of the team to retrieve
            
        Returns:
            TeamResponse: Team data
            
        Raises:
            ValueError: If team not found
        """
        teams = self.get_all_teams()
        team_data = next((t for t in teams if t['name'] == team_name), None)
        
        if not team_data:
            raise ValueError(f"Team with name '{team_name}' not found")
            
        return TeamResponse(**team_data)
    
    def update_agent(self, name: str, role: str, tools: List[str], 
                    description: str, instructions: List[str],
                    urls: List[str] = None) -> AgentResponse:
        """
        Update an existing agent's details.
        
        Args:
            name (str): Name of the agent to update
            role (str): New role of the agent
            tools (List[str]): Updated list of tool names the agent can use
            description (str): Updated description of the agent
            instructions (List[str]): Updated list of instructions for the agent
            urls (List[str], optional): Updated list of URLs for the agent to use
            
        Returns:
            AgentResponse: Updated agent data
        """
        agents = self.get_all_agents()
        agent_data = next((a for a in agents if a['name'] == name), None)
        
        if not agent_data:
            raise ValueError(f"Agent with name '{name}' not found")
        
        # Update agent details
        agent_data['role'] = role
        agent_data['tools'] = tools
        agent_data['description'] = description
        agent_data['instructions'] = instructions
        agent_data['urls'] = urls or []

        # Save updated agents list to storage
        with open(self.storage_path, 'w') as f:
            json.dump(agents, f, indent=2)

        return AgentResponse(**agent_data)