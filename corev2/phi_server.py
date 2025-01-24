import json
from phi.agent import Agent
from phi.playground import Playground, serve_playground_app
from reserved_agents import climate_ai, green_pill_ai, owocki_ai, gitcoin_ai

with open("agents.json", "r") as agent_file:
    agents_data = json.load(agent_file)

with open("teams.json", "r") as teams_file:
    teams_data = json.load(teams_file)

dynamic_agents = []
for agent_data in agents_data:
    dynamic_agent = Agent(
        name=agent_data["name"],
        introduction=f"I am {agent_data['name']}, a {agent_data['role']}.",
        role=agent_data["role"],
        description=agent_data["description"],
        instructions=agent_data["instructions"],
        task=f"Perform the tasks outlined in the instructions for {agent_data['name']}.",
        search_knowledge=True,
        stream=agent_data.get("markdown", False),
    )
    dynamic_agents.append(dynamic_agent)

dynamic_teams = []
for team_data in teams_data:
    team_agents = []
    for agent_data in team_data["agents"]:
        team_agent = Agent(
            name=agent_data["name"],
            introduction=f"I am {agent_data['name']}, a {agent_data['role']}.",
            role=agent_data["role"],
            description=agent_data["description"],
            instructions=agent_data["instructions"],
            task=f"Perform the tasks outlined in the instructions for {agent_data['name']}.",
            search_knowledge=True,
            stream=agent_data.get("markdown", False),
        )
        team_agents.append(team_agent)
    
    team_agent = Agent(
        name=team_data["name"],
        team=team_agents,
        instructions=team_data["instructions"],
        role="Team",
        description=f"The {team_data['name']} consists of multiple agents collaborating to achieve shared goals.",
        task=f"Collaborate as a team to achieve the goals specified for {team_data['name']}.",
        stream=team_data.get("markdown", False),
        show_tool_calls=team_data.get("show_tool_calls", True),
    )
    dynamic_teams.append(team_agent)

all_agents = [climate_ai, green_pill_ai, owocki_ai, gitcoin_ai] + dynamic_agents + dynamic_teams

playground = Playground(agents=all_agents).get_app()

if __name__ == "__main__":
    serve_playground_app("phi_server:playground", reload=True)
