import { currentUser } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

const ALLOWED_EMAILS = [
  "dddharamveersingh@gmail.com",
  "chaitanyarai899@gmail.com",
  "piyushch377@gmail.com",
  "kevin@gitcoin.co",
  "venkatachaitanya373@gmail.com",
];

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
