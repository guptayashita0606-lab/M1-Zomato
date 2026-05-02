import type { Metadata } from "next";
import "./globals.css";
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
      <body className="bg-[#fcf9f8] text-[#1b1c1c] min-h-screen flex" style={{ fontFamily: 'Plus Jakarta Sans, sans-serif' }}>
        {children}
      </body>
    </html>
  );
}
