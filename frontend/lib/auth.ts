import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

const ALLOWED_EMAILS = [""];

export async function checkAllowedEmail() {
  const user = await currentUser();

  if (!user) {
    redirect("/sign-in");
  }

  const email = user.emailAddresses[0]?.emailAddress;

  if (!email || !ALLOWED_EMAILS.includes(email)) {
    redirect("/dashboard");
  }

  return true;
}
