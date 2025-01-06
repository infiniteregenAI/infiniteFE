import { Sidebar } from "@/components/sidebar";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div>
      <Sidebar />
      <main className="lg:pl-[72px] min-h-[100dvh] bg-background">
        {children}
      </main>
    </div>
  );
}
