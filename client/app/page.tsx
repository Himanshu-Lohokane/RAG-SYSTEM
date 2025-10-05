import Link from 'next/link'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Upload, Search, FileText, Languages, Zap, Shield } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="px-6 py-4 border-b bg-white/80 backdrop-blur-sm">
        <div className="flex items-center justify-between max-w-6xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center">
              <span className="text-white font-bold text-lg">DM</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">DocuMind AI</h1>
              <p className="text-sm text-gray-600">Intelligent Document Processing</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Link href="/upload">
              <Button variant="outline">Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-6xl mx-auto px-6 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Your Personal
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600"> AI Document</span>
            <br />Processing Assistant
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Upload, process, and chat with your documents using advanced AI. Extract text, translate languages, 
            and get intelligent insights from any document format.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/upload">
              <Button size="lg" className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                <Upload className="h-5 w-5 mr-2" />
                Start Processing
              </Button>
            </Link>
            <Link href="/search">
              <Button size="lg" variant="outline">
                <Search className="h-5 w-5 mr-2" />
                AI Assistant
              </Button>
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <FileText className="h-6 w-6 text-blue-600" />
              </div>
              <CardTitle>Multi-Format Support</CardTitle>
              <CardDescription>
                Process images (JPG, PNG), PDFs, and Word documents with intelligent OCR technology
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <Languages className="h-6 w-6 text-purple-600" />
              </div>
              <CardTitle>Multi-Language AI</CardTitle>
              <CardDescription>
                Detect languages automatically and translate content with advanced language processing
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <Search className="h-6 w-6 text-green-600" />
              </div>
              <CardTitle>Intelligent Chat</CardTitle>
              <CardDescription>
                Ask questions about your documents and get AI-powered answers with source references
              </CardDescription>
            </CardHeader>
          </Card>
        </div>

        {/* Key Features */}
        <div className="bg-white rounded-2xl p-8 shadow-lg">
          <h2 className="text-3xl font-bold text-center mb-12">Powerful AI Capabilities</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Zap className="h-4 w-4 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold mb-2">Lightning Fast Processing</h3>
                <p className="text-gray-600">Advanced OCR and AI processing for quick document analysis and text extraction</p>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Shield className="h-4 w-4 text-purple-600" />
              </div>
              <div>
                <h3 className="font-semibold mb-2">Secure & Private</h3>
                <p className="text-gray-600">Your documents are processed securely with industry-standard encryption</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
