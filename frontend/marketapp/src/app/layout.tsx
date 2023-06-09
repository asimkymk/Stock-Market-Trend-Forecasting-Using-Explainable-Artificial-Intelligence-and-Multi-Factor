import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Stock Market Trend Forecasting Using Explainable Artificial Intelligence and Multi-Factor',
  description: 'Generated by Asım Kaymak and Mustafa Emre Taşkın',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
