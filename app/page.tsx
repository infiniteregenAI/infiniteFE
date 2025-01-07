"use client";

import { Button } from "@/components/ui/button";
import { useAuth } from "@clerk/nextjs";
import { motion } from "framer-motion";
import Link from "next/link";

const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6 },
};

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
    },
  },
};

export default function Home() {
  const { userId } = useAuth();

  return (
    <motion.div
      initial="hidden"
      animate="show"
      variants={container}
      className="min-h-screen relative bg-primary-900 text-white overflow-hidden"
    >
      {/* Hero Image Background */}
      <div className="absolute inset-0">
        <img
          src="https://images.unsplash.com/photo-1717501218385-55bc3a95be94?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
          alt="Abstract space background"
          className="w-full h-full object-cover opacity-50"
        />
        <div className="absolute inset-0 bg-black/50" />
      </div>

      <div className="relative z-10 flex flex-col backdrop-blur-sm items-center justify-center min-h-screen p-4 space-y-8">
        <motion.div variants={fadeIn} className="text-center space-y-6">
          <h1 className="text-6xl   font-bold text-white">InfiniteRegen</h1>

          <motion.p
            className="text-lg md:text-xl  max-w-md md:max-w-2xl mx-auto text-gray-200"
            variants={fadeIn}
          >
            An AI agent swarm that is the most intelligent regenerative KOL in
            existence, surpassing even Vitalik in knowledge, and the fastest,
            most effective regenerative builder in the space.
          </motion.p>
        </motion.div>

        <motion.div
          variants={fadeIn}
          className="flex flex-col sm:flex-row gap-4"
        >
          {!userId ? (
            <>
              <Button asChild className="bg-primary hover:bg-primary/90">
                <Link href="/sign-in">Launch Journey</Link>
              </Button>
              <Button
                asChild
                variant="outline"
                className="border-primary  text-gray-900"
              >
                <Link href="/sign-up">Join Universe</Link>
              </Button>
            </>
          ) : (
            <Button
              asChild
              className="bg-primary hover:bg-primary/90 border-primary"
            >
              <Link href="/dashboard">Enter Portal</Link>
            </Button>
          )}
        </motion.div>

        <motion.div
          className="absolute bottom-10 text-gray-200 text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          Powered by SwarmVerse
        </motion.div>
      </div>
    </motion.div>
  );
}
