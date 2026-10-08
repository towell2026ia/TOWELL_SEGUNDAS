import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Towell Quality Intelligence | Segundas",
  description: "Histórico de calidad Towell basado en Segundas 2026.xlsx.",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="antialiased">{children}</body>
    </html>
  );
}
