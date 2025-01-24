from phi.playground import Playground, serve_playground_app
from reserved_agents import climate_ai,green_pill_ai,owocki_ai,gitcoin_ai

playground = Playground(agents=[climate_ai,green_pill_ai,owocki_ai,gitcoin_ai]).get_app()

if __name__ == "__main__":
    serve_playground_app("phi_server:playground", reload=True)