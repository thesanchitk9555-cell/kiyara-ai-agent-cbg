import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Kiyara AI - Autonomous Agent',
  description: 'AI Voice Agent for Chandra Bhanu Gupt Agriculture College',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased bg-black min-h-screen">
        {children}
      </body>
    </html>
  );
}
