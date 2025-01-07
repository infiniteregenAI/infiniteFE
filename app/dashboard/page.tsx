"use client";

import { Card } from "@/components/ui/card";
import { UserButton, useUser } from "@clerk/nextjs";
import { motion } from "framer-motion";
import { Boxes, Plus } from "lucide-react";
import Link from "next/link";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

export default function Home() {
  const { user } = useUser();

  return (
    <motion.div
      initial="hidden"
      animate="show"
      variants={container}
      className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800"
    >
      <div className="max-w-6xl mx-auto p-6">
        {/* Header with User Info */}
        <motion.div
          variants={item}
          className="flex justify-between items-center mb-8"
        >
          <h1 className="text-3xl font-bold ">Dashboard</h1>
          <UserButton />
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
          {/* Profile Section */}
          <motion.div variants={item} className="md:col-span-4">
            <Card className="p-6 backdrop-blur-sm bg-white/80 dark:bg-gray-800/80 ">
              <div className="flex items-center gap-4">
                <img
                  src={user?.imageUrl}
                  alt="Profile"
                  className="w-16 h-16 rounded-full ring-2 ring-primary p-1"
                />
                <div>
                  <h2 className="text-lg font-bold">{user?.fullName}</h2>
                  <p className="text-gray-600 dark:text-gray-300 text-sm">
                    {user?.primaryEmailAddress?.emailAddress}
                  </p>
                </div>
              </div>
            </Card>
          </motion.div>

          {/* Actions Grid */}
          <motion.div variants={item} className="md:col-span-8">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 ">
              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full  "
              >
                <Link href="/dashboard/create-profile">
                  <Card className="p-6 hover:shadow-lg border transition-all duration-300 backdrop-blur-sm bg-white/80 dark:bg-gray-800/80  hover:border-primary">
                    <Plus className="w-8 h-8 mb-3 text-primary" />
                    <h3 className="font-semibold">Create Agent</h3>
                  </Card>
                </Link>
              </motion.div>

              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Link href="/dashboard/chat">
                  <Card className="p-6 border bg-white  hover:border-green-500">
                    <svg
                      width="32"
                      height="32"
                      className="mb-3 text-green-500"
                      viewBox="0 0 24 24"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M20 2H4C2.9 2 2.01 2.9 2.01 4L2 22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM6 9H18V11H6V9ZM14 14H6V12H14V14ZM18 8H6V6H18V8Z"
                        fill="currentColor"
                      />
                    </svg>
                    <h3 className="font-semibold">Chat</h3>
                  </Card>
                </Link>
              </motion.div>
              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Link href="/dashboard/create-bucket">
                  <Card className="p-6 border  bg-white hover:border-green-500">
                    <Boxes className="w-8 h-8 mb-3 text-green-500" />
                    <h3 className="font-semibold">Launch Backroom</h3>
                  </Card>
                </Link>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}
