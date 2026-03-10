import type { Metadata } from "next";
import { Inter } from "next/font/google";
// IMPORT CRUCIAL : C'est ce qui charge Tailwind !
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "TechWatch AI",
  description: "Tableau de bord de veille technologique avec IA",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}