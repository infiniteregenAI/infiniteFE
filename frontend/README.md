# InfiniteFE

A repository containing all the infrastructure and code for the user interface.

## Prerequisites

- Node.js 18+
- npm or yarn
- Git

## Environment Setup

Create a `.env.local` file in the root directory with the following variables:

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
NEXT_PUBLIC_API_URL=your_api_url
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

## Key Features

- 🔐 Authentication with Clerk
- 🎨 Modern UI with Tailwind CSS
- 🚀 Server-side rendering with Next.js
- 📱 Responsive design
- ⚡ Real-time features
- 🔄 State management with Zustand
- 📝 Form handling with React Hook Form
- ✨ Beautiful animations with Framer Motion

## Tech Stack

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Clerk Authentication
- React Query
- Zustand
- Radix UI Components
- Axios
- And more!

## Development

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

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
