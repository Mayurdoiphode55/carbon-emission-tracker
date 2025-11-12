import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Carbon Emission Tracker",
  description: "Dashboard to visualize emission analytics",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="antialiased bg-gray-50 text-gray-900">
        {children}
      </body>
    </html>
  );
}

