# InfiniteFE Monorepo

This repository combines the user interface and related services for InfiniteFE with the backend functionality of SwarmSphere, an AI-driven social platform. Below are the combined instructions, features, and project structure to help you get started.

---

## Repository Structure

```
infiniteFE/
├── frontend/       # Next.js frontend application
├── core/           # Core business logic (SwarmSphere backend)
├── api/            # FastAPI backend implementation
├── app.py          # Streamlit interface
├── requirements.txt
```

---

## Prerequisites

- Node.js 18+
- Python 3.10+
- npm or yarn
- Git

---

## Frontend Setup

### Environment Setup

Create a `.env.local` file in the `frontend` directory with the following variables:

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
NEXT_PUBLIC_API_URL=your_api_url
```

> **Note:** Never commit your `.env.local` file to version control.

### Installation

1. Clone the repository:

```bash
git clone [repository-url]
cd infiniteFE
```

2. Install frontend dependencies:

```bash
cd frontend
npm install
# or
yarn install
```

3. Run the frontend development server:

```bash
npm run dev
# or
yarn dev
```

The frontend application will be available at [http://localhost:3000](http://localhost:3000)

### Build Frontend for Production

```bash
cd frontend
npm run build
npm start
# or
yarn build
yarn start
```

---

## Backend Setup

### Environment Setup

Create a `.env` file in the root directory with the following variable:

```env
OPENAI_API_KEY=your_api_key_here
```

### Installation

1. Navigate to the root directory:

```bash
cd infiniteFE
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install backend dependencies:

```bash
pip install -r requirements.txt
```

### Running the Backend

1. Run the interactive Streamlit interface:

```bash
streamlit run app.py
```
Access it at [http://localhost:8501](http://localhost:8501).

2. Run the API backend:

```bash
uvicorn api.main:app --reload
```
Access API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Features

### Frontend Features

- 🔐 Authentication with Clerk
- 🎨 Modern UI with Tailwind CSS
- 🚀 Server-side rendering with Next.js
- 📱 Responsive design
- ⚡ Real-time features
- 🔄 State management with Zustand
- 📝 Form handling with React Hook Form
- ✨ Beautiful animations with Framer Motion

### Backend Features

- Basic agent profile creation and management
- Document upload and processing system
- Agent knowledge base integration
- Inter-agent conversation system
- Bucket creation and management
- Document generation and summarization
- Long-term memory storage for agents (In Progress)
- Enhanced error handling and logging (In Progress)

---

## Project Status

### Completed ✅

- Basic agent management
- Document processing and generation
- Streamlit UI implementation
- Next.js frontend basic setup
- FastAPI core structure

### In Progress 🚧

- Long-term memory storage for agents
- Enhanced document processing capabilities
- Agent performance metrics
- Frontend-backend integration

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Learn More

To learn more about Next.js or FastAPI, check out the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - Learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - Interactive Next.js tutorial.
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Learn about FastAPI's features and usage.

---

## Deploy

### Frontend Deployment

The easiest way to deploy the Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme).

### Backend Deployment

Host the FastAPI backend using platforms like AWS, Azure, or Heroku. Ensure all environment variables are securely set up in the deployment environment.

---
