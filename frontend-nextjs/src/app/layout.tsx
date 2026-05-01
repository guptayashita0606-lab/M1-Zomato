import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Zomato AI - Restaurant Recommendations",
  description: "AI-powered restaurant recommendation system with culinary joy",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="light">
      <body className="bg-background text-on-background font-body-md min-h-screen flex">
        {children}
      </body>
    </html>
  );
}
