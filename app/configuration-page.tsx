import { Metadata } from "next";
=import Configuration from "@/components/ui/configuration-form"; // Adjust the path accordingly to where your Configuration component is located.

export const metadata: Metadata = {
  title: "T2",
  description: "A template for Next.js with Tailwind",
};

export default function Page() {
  return (
    <>
      <main className="flex min-h-screen flex-col items-left justify-between p-20">
      <div className="text-3xl font-bold text-center mt-8 mb-20">
          <h1>Welcome to the Mock Salary Negotiator</h1>
        </div>
        <Configuration />
      </main>
    </>
  );
}