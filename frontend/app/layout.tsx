import type { Metadata } from "next";
import type { ReactNode } from "react";
import Link from "next/link";
import { Inter, Space_Grotesk } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  weight: ["500", "600", "700"],
  variable: "--font-space-grotesk",
});

export const metadata: Metadata = {
  title: "compileit.chat",
  description: "Frågor och svar om Compileit, med källor.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="sv" className={`${inter.variable} ${spaceGrotesk.variable}`}>
      <body className="bg-canvas font-sans text-[15px] leading-[1.55] text-ink">
        <div className="mx-auto flex min-h-dvh w-full max-w-[1280px] flex-col gap-5 p-3 sm:p-5">
          <header className="flex items-center px-2 py-1">
            <Link
              href="/"
              className="font-display text-lg font-bold tracking-[-0.02em]"
            >
              compileit<span className="text-accent">.</span>chat
            </Link>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
