import { QueryProvider } from "@/lib/providers/query-provider";
import { ClerkProvider } from "@clerk/nextjs";
import { GoogleAnalytics } from "@next/third-parties/google";
import type { Metadata } from "next";
import { Inter, Manrope } from "next/font/google";
import "./globals.css";

const interFont = Inter({ subsets: ["latin"] });
const manropeFont = Manrope({
  subsets: ["latin"],
  variable: "--font-manrope",
});

export const metadata: Metadata = {
  title: "InfiniteRegen | AI Agent Swarm",
  description: `An AI agent swarm that is the most intelligent regenerative KOL in
            existence, surpassing even Vitalik in knowledge, and the fastest,
            most effective regenerative builder in the space.`,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <QueryProvider>
        <html lang="en">
          <body
            className={`${manropeFont.variable} ${interFont.className}  antialiased`}
          >
            {children}
          </body>
        </html>
        <GoogleAnalytics gaId="G-30Z96DC785" />
      </QueryProvider>
    </ClerkProvider>
  );
}
