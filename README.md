# InfiniteFE infrastructure
A monorepo containing the Next.js frontend application with integrated FastAPI backend.

## Repository Structure
```
infiniteFE/
├   # Next.js frontend application with integrated FastAPI backend
    ├── api/     # FastAPI backend logic
        └── core/  # Backend business logic
```

## Prerequisites
- Node.js 18+
- Python 3.10+
- npm or yarn
- Git

## Environment Setup
Create a `.env.local` file in the `frontend` directory:
```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
NEXT_PUBLIC_API_URL=your_api_url
OPENAI_API_KEY=your_openai_api_key
```
> Note: Never commit your `.env.local` file to version control.

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd infiniteFE/frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Run the development server:
```bash
npm run dev
# or
yarn dev
```

The application will be available at [http://localhost:3000](http://localhost:3000)

## Build for Production
```bash
npm run build
npm start
# or
yarn build
yarn start
```


## Tech Stack
- Next.js
- FastAPI (integrated backend)
- React
- TypeScript
- Tailwind CSS
- Clerk Authentication
- React Query
- Zustand
- Radix UI Components
- Axios
- OpenAI SDK

## Development Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License.

## Learn More
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Clerk Documentation](https://clerk.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## Deploy
The application can be deployed on [Vercel](https://vercel.com) or any other platform that supports Next.js applications with Python runtime.
