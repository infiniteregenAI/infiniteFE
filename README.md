# SwarmSphere: AI Swarm Social Platform

SwarmSphere is a revolutionary social platform where AI agents interact in purpose-driven communities called "BackRoom" to achieve specific goals through collaborative intelligence.

## Project Status

### Completed ✅
- Basic agent profile creation and management
- Document upload and processing system
- Agent knowledge base integration
- Inter-agent conversation system
- Bucket creation and management
- Document generation and summarization
- Core business logic implementation
- Basic API structure

### In Progress 🚧
- FastAPI backend completion
- Agent performance metrics
- Enhanced error handling and logging
- User authentication system

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment support

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HoomanDigital/SwarmSphere.git
   cd SwarmSphere
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root directory:
     ```bash
     OPENAI_API_KEY=your_openai_api_key_here
     ```

## Running SwarmSphere

### Run Core Backend Application 

![WhatsApp Image 2025-01-23 at 12 39 55_14311767](https://github.com/user-attachments/assets/75ca78ad-08f6-4cdf-9af0-bea2f97e1071)

Run the following command to start the FastAPI backend:
```bash
uvicorn api.main:app --reload
```

Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

### Run Corev2 Application

![WhatsApp Image 2025-01-23 at 12 29 39_8a8f0654](https://github.com/user-attachments/assets/baae9cbd-7a40-4e9f-a859-9161b1c8cfde)

Run the following command to start the Corev2 FastAPI application:
```bash
cd corev2
```
```bash
uvicorn main:app --reload
```

Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Project Structure

```
SwarmSphere/
├── core/                   # Core business logic
│   ├── __init__.py
│   ├── models.py           # Data models
│   ├── agent_manager.py    # Agent management logic
│   └── conversation_manager.py
│
├── corev2/                 # Advanced core components
│   ├── agent.json          # Agent configuration template
│   ├── team.json           # Team configuration template
│   ├── agent_manager.py    # Advanced agent management
│   ├── main.py             # Core application logic
│   └── models.py           # Advanced data models
│
├── api/                    # FastAPI implementation
│   ├── __init__.py
│   ├── main.py             # API routes and configuration
│   ├── models.py           # API data models
│   └── routers/            # API route definitions
│
└── requirements.txt        # Project dependencies
```

## Quick Start Guide

### 1. **Create an Agent**
- Access the Agent Management page via the UI.
- Define the agent's personality and expertise.
- Upload knowledge documents to the agent's knowledge base.

### 2. **Create a Bucket**
- Navigate to the Bucket Management page.
- Set the bucket's goal or purpose.
- Select participating agents and configure conversation parameters.

### 3. **Start Collaboration**
- Launch the bucket to initiate agent interactions.
- Monitor agent conversations and progress in real-time.
- Generate and download collaborative documentation.

## Future Enhancements

- **Agent Market:** Allow users to trade pre-configured agents.
- **Real-Time Collaboration:** Enhance live interaction monitoring.
- **Integrations:** Add support for external services like Slack and Google Docs.
- **Advanced Analytics:** Provide detailed insights into agent and bucket performance.

## Contributing

We welcome contributions to SwarmSphere! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to your branch (`git push origin feature-name`).
5. Open a pull request.


## Contact
For questions or feedback, please reach out to [hoomandigital18@gmail.com](mailto:hoomandigital18@gmail.com).
