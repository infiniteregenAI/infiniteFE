"use client";

import { cn } from "@/lib/utils";
import { Menu, Plus } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const routes = [
  {
    label: "Home",
    icon: (
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM9 17H7V10H9V17ZM13 17H11V7H13V17ZM17 17H15V13H17V17Z"
          fill="currentColor"
        />
      </svg>
    ),
    href: "/dashboard",
  },
  {
    label: "Add",
    icon: <Plus className="size-5" />,
    href: "/dashboard/create-profile",
  },
  {
    label: "Chat",
    icon: (
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M20 2H4C2.9 2 2.01 2.9 2.01 4L2 22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM6 9H18V11H6V9ZM14 14H6V12H14V14ZM18 8H6V6H18V8Z"
          fill="currentColor"
        />
      </svg>
    ),
    href: "/dashboard/chat",
  },
  // {
  //   label: "Settings",
  //   icon: (
  //     <svg
  //       width="24"
  //       height="24"
  //       viewBox="0 0 24 24"
  //       fill="none"
  //       xmlns="http://www.w3.org/2000/svg"
  //     >
  //       <path
  //         d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM11 19.93C7.05 19.44 4 16.08 4 12C4 11.38 4.08 10.79 4.21 10.21L9 15V16C9 17.1 9.9 18 11 18V19.93ZM17.9 17.39C17.64 16.58 16.9 16 16 16H15V13C15 12.45 14.55 12 14 12H8V10H10C10.55 10 11 9.55 11 9V7H13C14.1 7 15 6.1 15 5V4.59C17.93 5.78 20 8.65 20 12C20 14.08 19.2 15.97 17.9 17.39Z"
  //         fill="currentColor"
  //       />
  //     </svg>
  //   ),
  //   href: "/dashboard/settings",
  // },
  // {
  //   label: "Help",
  //   icon: (
  //     <svg
  //       width="24"
  //       height="24"
  //       viewBox="0 0 24 24"
  //       fill="none"
  //       xmlns="http://www.w3.org/2000/svg"
  //     >
  //       <path
  //         d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM12.01 18C11.31 18 10.75 17.44 10.75 16.74C10.75 16.03 11.31 15.49 12.01 15.49C12.72 15.49 13.26 16.03 13.26 16.74C13.25 17.43 12.72 18 12.01 18ZM15.02 10.6C14.26 11.71 13.54 12.06 13.15 12.77C12.99 13.06 12.93 13.25 12.93 14.18H11.11C11.11 13.69 11.03 12.89 11.42 12.2C11.91 11.33 12.84 10.81 13.38 10.04C13.95 9.23 13.63 7.71 12.01 7.71C10.95 7.71 10.43 8.51 10.21 9.19L8.56 8.49C9.01 7.15 10.22 6 11.99 6C13.47 6 14.48 6.67 15 7.52C15.44 8.24 15.7 9.59 15.02 10.6Z"
  //         fill="currentColor"
  //       />
  //     </svg>
  //   ),
  //   href: "/dashboard/help",
  // },
];

export function Sidebar() {
  const pathname = usePathname();
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  return (
    <div className="relative">
      <button
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-gray-200 rounded-md" // Changed to light mode background
        onClick={() => setIsMobileOpen(!isMobileOpen)}
      >
        <Menu className="h-6 w-6 text-gray-800" />
      </button>

      <div
        className={cn(
          "fixed left-0 top-0 h-full bg-white py-8 text-gray-800 px-3 py-4 flex flex-col gap-12 border-r transition-all duration-300", // Changed text color for light mode
          isMobileOpen
            ? "w-64 translate-x-0"
            : "w-64 -translate-x-full lg:translate-x-0 lg:w-[72px] "
        )}
      >
        <Image
          src="/logo.svg"
          alt="Logo"
          width={40}
          height={24}
          className="mx-auto"
        />
        <div className="flex-1  flex flex-col gap-0.5">
          {routes.map((route) => (
            <Link
              key={route.href}
              href={route.href}
              className={cn(
                "text-sm group flex aspect-square hover:bg-primary/10 hover:text-primary transition-all duration-300 rounded items-center  w-full justify-center font-medium cursor-pointer ",
                pathname.split("/")[2] === route.href.split("/")[2]
                  ? "text-primary bg-primary/10"
                  : "text-gray-400"
              )}
            >
              {route.icon}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
