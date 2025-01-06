import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Card, CardContent } from "@/components/ui/card";
import api from "@/lib/axios";
import { useBucketStore } from "@/lib/store/bucket-store";
import { useQuery } from "@tanstack/react-query";
import clsx from "clsx";
import { CheckCheck, MessageSquare, Users } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";

interface Agent {
  id: string;
  name: string;
  avatar: string;
  role: string;
  expertise: string[];
}

interface Bucket {
  id: string;
  name: string;
  description: string;
  selectedAgents: Agent[];
}

interface NavigationTabProps {
  href: string;
  isActive: boolean;
  children: ReactNode;
}

interface ListItemProps {
  isActive: boolean;
}

interface AgentListItemProps extends ListItemProps {
  agent: Agent;
}

interface BucketListItemProps extends ListItemProps {
  bucket: Bucket;
}

interface EmptyStateProps {
  type: "chat" | "bucket";
}

interface ChatLayoutProps {
  children: ReactNode;
  type?: "chat" | "bucket";
}

const NavigationTab = ({ href, isActive, children }: NavigationTabProps) => (
  <Link href={href}>
    <h2
      className={clsx(
        "text-sm font-medium text-muted-light px-3 border-b-2 border-transparent py-5",
        { "border-b-primary": isActive }
      )}
    >
      {children}
    </h2>
  </Link>
);

const LoadingSkeleton = () => (
  <div className="flex flex-col divide-y divide-neutral-200 animate-pulse">
    {[1, 2, 3].map((i) => (
      <div key={i} className="flex items-center gap-4 px-6 py-4">
        <div className="w-12 h-12 bg-neutral-200 rounded-full" />
        <div className="flex-1">
          <div className="h-4 bg-neutral-200 rounded w-1/3 mb-2" />
          <div className="h-3 bg-neutral-200 rounded w-2/3" />
        </div>
      </div>
    ))}
  </div>
);

const EmptyState = ({ type }: EmptyStateProps) => (
  <Card className="m-6">
    <CardContent className="flex flex-col items-center justify-center py-8 text-center">
      {type === "chat" ? (
        <MessageSquare className="w-12 h-12 text-muted-light mb-4" />
      ) : (
        <Users className="w-12 h-12 text-muted-light mb-4" />
      )}
      <h3 className="text-lg font-semibold mb-2">
        No {type === "chat" ? "Agents" : "Buckets"} Available
      </h3>
      <p className="text-muted-light">
        {type === "chat"
          ? "No agents are currently available. Please try again later."
          : "You haven't created any buckets yet. Create one to get started."}
      </p>
    </CardContent>
  </Card>
);

const AgentListItem = ({ agent, isActive }: AgentListItemProps) => (
  <Link
    href={`/dashboard/chat/${agent.id}`}
    className={clsx(
      "flex items-center relative gap-4 px-6 py-4 hover:bg-primary/10",
      {
        "bg-primary/10": isActive,
      }
    )}
  >
    {isActive && (
      <div className="absolute left-0 top-0 w-1 h-full bg-primary" />
    )}
    <Avatar className="bg-neutral-100 w-12 h-12">
      <AvatarFallback>{agent.avatar}</AvatarFallback>
    </Avatar>
    <div className="flex flex-col gap-1.5 flex-1">
      <div className="flex items-center gap-2 justify-between">
        <h2 className="text-base font-semibold font-manrope">{agent.name}</h2>
        <span className="text-muted-light text-xs">5m ago</span>
      </div>
      <div className="flex justify-between gap-2 items-center">
        <p className="text-sm text-muted-light flex-1 line-clamp-1">
          {agent.role} - {agent.expertise.join(", ")}
        </p>
        <CheckCheck className="w-4 h-4 text-green-500" />
      </div>
    </div>
  </Link>
);

const BucketListItem = ({ bucket, isActive }: BucketListItemProps) => (
  <Link
    href={`/dashboard/bucket/${bucket.id}`}
    className={clsx(
      "flex items-center relative gap-4 px-6 py-4 hover:bg-primary/10",
      {
        "bg-primary/10": isActive,
      }
    )}
  >
    {isActive && (
      <div className="absolute left-0 top-0 w-1 h-full bg-primary" />
    )}
    <div className="flex">
      {bucket.selectedAgents.map((agent, index) => (
        <Avatar
          key={agent.id}
          className={clsx("bg-neutral-100 w-12 h-12", {
            "ml-[-30px]": index > 0,
          })}
        >
          <AvatarFallback>{agent.avatar}</AvatarFallback>
        </Avatar>
      ))}
    </div>
    <div className="flex flex-col gap-1.5 flex-1">
      <div className="flex items-center gap-2 justify-between">
        <h2 className="text-base font-semibold font-manrope">{bucket.name}</h2>
        <span className="text-muted-light text-xs">5m ago</span>
      </div>
      <div className="flex justify-between gap-2 items-center">
        <p className="text-sm text-muted-light flex-1 line-clamp-1">
          {bucket.description}
        </p>
        <CheckCheck className="w-4 h-4 text-green-500" />
      </div>
    </div>
  </Link>
);

const ChatLayout = ({ children, type = "chat" }: ChatLayoutProps) => {
  const { data: agents, isLoading: isLoadingAgents } = useQuery({
    queryKey: ["agents"],
    queryFn: async () => {
      const response = await api.get<Agent[]>("/api/agents");
      return response;
    },
  });

  const pathname = usePathname();
  const { buckets } = useBucketStore();

  const renderContent = () => {
    if (type === "chat") {
      if (isLoadingAgents) return <LoadingSkeleton />;
      if (!agents?.data?.length) return <EmptyState type="chat" />;
      return agents.data.map((agent) => (
        <AgentListItem
          key={agent.id}
          agent={agent}
          isActive={pathname === `/dashboard/chat/${agent.id}`}
        />
      ));
    } else {
      if (!buckets?.length) return <EmptyState type="bucket" />;
      return buckets.map((bucket) => (
        <BucketListItem
          key={bucket.id}
          bucket={bucket}
          isActive={pathname === `/dashboard/bucket/${bucket.id}`}
        />
      ));
    }
  };

  return (
    <div className="h-screen flex overflow-y-auto">
      <section className="w-[23rem] scrollbar-none overflow-y-auto h-screen sticky top-0 bg-white border-r">
        <div className="flex sticky top-0 bg-white z-[1] items-center px-3 border-b gap-2">
          <NavigationTab
            href="/dashboard/chat"
            isActive={pathname.startsWith("/dashboard/chat")}
          >
            Chat
          </NavigationTab>
          <NavigationTab
            href="/dashboard/bucket"
            isActive={pathname.startsWith("/dashboard/bucket")}
          >
            Backrooms
          </NavigationTab>
        </div>
        <div className="flex flex-col divide-y divide-neutral-200">
          {renderContent()}
        </div>
      </section>
      <section className="flex-1">{children}</section>
    </div>
  );
};

export default ChatLayout;
