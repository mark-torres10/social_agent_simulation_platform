import React from 'react'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Prophecy - AI-Powered Business Simulation Platform',
  description: 'Transform million-dollar guesswork into data-driven certainty with 1M+ AI agent simulations. Predict product launches, prevent crises, and maximize profits.',
  keywords: ['AI simulation', 'business intelligence', 'predictive analytics', 'crisis prevention', 'product launch', 'market research'],
  authors: [{ name: 'Prophecy Team' }],
  creator: 'Prophecy',
  publisher: 'Prophecy',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://prophecy.ai'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'Prophecy - AI-Powered Business Simulation Platform',
    description: 'Transform million-dollar guesswork into data-driven certainty with 1M+ AI agent simulations.',
    url: 'https://prophecy.ai',
    siteName: 'Prophecy',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Prophecy - AI Business Simulation Platform',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Prophecy - AI-Powered Business Simulation Platform',
    description: 'Transform million-dollar guesswork into data-driven certainty with 1M+ AI agent simulations.',
    images: ['/og-image.jpg'],
    creator: '@prophecyai',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
    yandex: 'your-yandex-verification-code',
    yahoo: 'your-yahoo-verification-code',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} antialiased`}>
        {children}
      </body>
    </html>
  )
}