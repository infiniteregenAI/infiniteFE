"use client";
import ChatLayout from "@/components/chat/ChatLayout";

const page = () => {
  return (
    <ChatLayout type="bucket">
      <div className="h-screen flex-1">
        <div className="flex flex-col gap-2 items-center justify-center h-full">
          <h1 className="text-sm font-medium  text-muted-light font-manrope">
            No Chat selected
          </h1>
        </div>
      </div>
    </ChatLayout>
  );
};

export default page;
