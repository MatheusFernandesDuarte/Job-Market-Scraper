// app/layout.tsx

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../styles/globals.css";

import { LanguageProvider } from "@/context/LanguageContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Job Market Scraper",
  description: "Encontre vagas internacionais com base no seu perfil",
  icons: {
    icon: "/app_icon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-br">
      <body className={inter.className}>
        <LanguageProvider>
          {children}
        </LanguageProvider>
      </body>
    </html>
  );
}
