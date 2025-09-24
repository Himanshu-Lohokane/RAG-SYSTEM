"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { 
  Search, 
  Filter, 
  Download, 
  Eye, 
  FileText, 
  Calendar,
  User,
  FolderOpen,
  Star,
  Share2
} from "lucide-react";
import { useRouter } from "next/navigation";
import RagChat from "./RagChat";

interface Document {
  id: string;
  title: string;
  type: string;
  department: string;
  uploadedBy: string;
  uploadDate: string;
  size: string;
  tags: string[];
  status: "draft" | "approved" | "archived";
  compliance: boolean;
}

const DocumentSearchPage = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedFilters, setSelectedFilters] = useState<string[]>([]);
  const router = useRouter();

  const mockDocuments: Document[] = [
    {
      id: "1",
      title: "Safety Compliance Report Q2 2024",
      type: "PDF",
      department: "Safety & Compliance",
      uploadedBy: "John Doe",
      uploadDate: "2024-06-15",
      size: "2.4 MB",
      tags: ["safety", "compliance", "quarterly"],
      status: "approved",
      compliance: true,
    },
    {
      id: "2",
      title: "Metro Line Extension Proposal",
      type: "DOCX",
      department: "Engineering",
      uploadedBy: "Sarah Smith",
      uploadDate: "2024-06-10",
      size: "5.1 MB",
      tags: ["engineering", "proposal", "expansion"],
      status: "draft",
      compliance: false,
    },
    {
      id: "3",
      title: "Financial Statement Q1 2024",
      type: "XLSX",
      department: "Finance",
      uploadedBy: "Mike Johnson",
      uploadDate: "2024-04-30",
      size: "1.8 MB",
      tags: ["finance", "quarterly", "statement"],
      status: "approved",
      compliance: true,
    },
    {
      id: "4",
      title: "Employee Handbook 2024",
      type: "PDF",
      department: "HR",
      uploadedBy: "Lisa Wong",
      uploadDate: "2024-01-15",
      size: "3.2 MB",
      tags: ["hr", "handbook", "policies"],
      status: "approved",
      compliance: true,
    },
    {
      id: "5",
      title: "Maintenance Schedule June",
      type: "PDF",
      department: "Operations",
      uploadedBy: "David Chen",
      uploadDate: "2024-05-28",
      size: "890 KB",
      tags: ["maintenance", "schedule", "operations"],
      status: "draft",
      compliance: false,
    },
  ];

  const filteredDocuments = mockDocuments.filter(doc => 
    doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.department.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "approved":
        return <Badge className="bg-green-100 text-green-800">Approved</Badge>;
      case "draft":
        return <Badge variant="secondary">Draft</Badge>;
      case "archived":
        return <Badge variant="outline">Archived</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Document Search & Browse</h1>
          <p className="text-muted-foreground">Find and manage your documents efficiently</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export Results
          </Button>
          <Button>
            <Filter className="h-4 w-4 mr-2" />
            Advanced Filter
          </Button>
        </div>
      </div>
      
      {/* RAG Chat Component */}
      <RagChat />

      <div className="grid gap-6 lg:grid-cols-4">
        {/* Filters Sidebar */}
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Filters</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Department Filter */}
              <div className="space-y-2">
                <Label className="text-sm font-medium">Department</Label>
                <div className="space-y-2">
                  {["Operations", "Finance", "HR", "Engineering", "Safety & Compliance"].map((dept) => (
                    <div key={dept} className="flex items-center space-x-2">
                      <Checkbox id={dept} />
                      <Label htmlFor={dept} className="text-sm">{dept}</Label>
                    </div>
                  ))}
                </div>
              </div>

              <Separator />

              {/* File Type Filter */}
              <div className="space-y-2">
                <Label className="text-sm font-medium">File Type</Label>
                <div className="space-y-2">
                  {["PDF", "DOCX", "XLSX", "PPTX", "TXT"].map((type) => (
                    <div key={type} className="flex items-center space-x-2">
                      <Checkbox id={type} />
                      <Label htmlFor={type} className="text-sm">{type}</Label>
                    </div>
                  ))}
                </div>
              </div>

              <Separator />

              {/* Status Filter */}
              <div className="space-y-2">
                <Label className="text-sm font-medium">Status</Label>
                <div className="space-y-2">
                  {["Approved", "Draft", "Archived"].map((status) => (
                    <div key={status} className="flex items-center space-x-2">
                      <Checkbox id={status} />
                      <Label htmlFor={status} className="text-sm">{status}</Label>
                    </div>
                  ))}
                </div>
              </div>

              <Separator />

              {/* Date Range */}
              <div className="space-y-2">
                <Label className="text-sm font-medium">Upload Date</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select range" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="today">Today</SelectItem>
                    <SelectItem value="week">This Week</SelectItem>
                    <SelectItem value="month">This Month</SelectItem>
                    <SelectItem value="quarter">This Quarter</SelectItem>
                    <SelectItem value="year">This Year</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Quick Stats</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Total Documents</span>
                <span className="text-sm font-medium">{mockDocuments.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Filtered Results</span>
                <span className="text-sm font-medium">{filteredDocuments.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Compliance Rate</span>
                <span className="text-sm font-medium">
                  {Math.round((mockDocuments.filter(d => d.compliance).length / mockDocuments.length) * 100)}%
                </span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3 space-y-4">
          {/* Search Bar */}
          <Card>
            <CardContent className="p-4">
              <div className="flex gap-2">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    placeholder="Search documents by title, department, or tags..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <Select>
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="Sort by" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="date">Date</SelectItem>
                    <SelectItem value="name">Name</SelectItem>
                    <SelectItem value="size">Size</SelectItem>
                    <SelectItem value="department">Department</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Search Results */}
          <Tabs defaultValue="grid" className="space-y-4">
            <div className="flex justify-between items-center">
              <TabsList>
                <TabsTrigger value="grid">Grid View</TabsTrigger>
                <TabsTrigger value="list">List View</TabsTrigger>
              </TabsList>
              <p className="text-sm text-muted-foreground">
                Showing {filteredDocuments.length} of {mockDocuments.length} documents
              </p>
            </div>

            <TabsContent value="grid">
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 items-start">
                {filteredDocuments.map((document) => (
                  <Card key={document.id} className="cursor-pointer hover:shadow-md transition-shadow min-h-[280px] flex flex-col">
                    <div className="relative p-4 pb-2">
                      {/* Status Badge - Fixed Position */}
                      <div className="absolute top-2 right-2">
                        {getStatusBadge(document.status)}
                      </div>
                      
                      {/* File Icon and Type */}
                      <div className="flex items-center gap-3 mb-3">
                        <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                          <FileText className="h-5 w-5 text-primary" />
                        </div>
                        <Badge variant="outline" className="text-xs">
                          {document.type}
                        </Badge>
                      </div>
                      
                      {/* Document Title */}
                      <CardTitle className="text-sm font-medium line-clamp-2 min-h-[2.5rem] mb-2 pr-16">
                        {document.title}
                      </CardTitle>
                    </div>

                    <CardContent className="flex-1 flex flex-col space-y-3 p-4 pt-0">
                      {/* Department and Uploader */}
                      <div className="space-y-2 text-xs text-muted-foreground">
                        <div className="flex items-center gap-2">
                          <FolderOpen className="h-3 w-3 flex-shrink-0" />
                          <span className="truncate">{document.department}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <User className="h-3 w-3 flex-shrink-0" />
                          <span className="truncate">{document.uploadedBy}</span>
                        </div>
                      </div>

                      {/* Date and Size */}
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          <span>{document.uploadDate}</span>
                        </div>
                        <span>{document.size}</span>
                      </div>

                      {/* Tags */}
                      <div className="flex flex-wrap gap-1 min-h-[1.5rem]">
                        {document.tags.slice(0, 3).map((tag) => (
                          <Badge key={tag} variant="secondary" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                        {document.tags.length > 3 && (
                          <Badge variant="secondary" className="text-xs">
                            +{document.tags.length - 3}
                          </Badge>
                        )}
                      </div>

                      {/* Action Buttons - Always at bottom */}
                      <div className="flex gap-1 mt-auto pt-2">
                        <Button 
                          variant="ghost" 
                          size="sm"
                          className="flex-1 text-xs"
                          onClick={() => router.push(`/document/${document.id}`)}
                        >
                          <Eye className="h-3 w-3 mr-1" />
                          View
                        </Button>
                        <Button variant="ghost" size="sm" className="flex-1 text-xs">
                          <Download className="h-3 w-3 mr-1" />
                          Download
                        </Button>
                        <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                          <Share2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="list">
              <Card>
                <div className="space-y-0">
                  {filteredDocuments.map((document, index) => (
                    <div key={document.id}>
                      <div className="flex items-center justify-between p-4 hover:bg-muted/50">
                        <div className="flex items-center gap-4 flex-1">
                          <FileText className="h-5 w-5 text-primary" />
                          <div className="flex-1 min-w-0">
                            <h3 className="font-medium truncate">{document.title}</h3>
                            <div className="flex items-center gap-4 text-sm text-muted-foreground mt-1">
                              <span>{document.department}</span>
                              <span>•</span>
                              <span>{document.uploadedBy}</span>
                              <span>•</span>
                              <span>{document.uploadDate}</span>
                              <span>•</span>
                              <span>{document.size}</span>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Badge variant="outline" className="text-xs">
                              {document.type}
                            </Badge>
                            {getStatusBadge(document.status)}
                          </div>
                          <div className="flex gap-1">
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => router.push(`/document/${document.id}`)}
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Download className="h-4 w-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Share2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      </div>
                      {index < filteredDocuments.length - 1 && <Separator />}
                    </div>
                  ))}
                </div>
              </Card>
            </TabsContent>
          </Tabs>

          {/* Pagination */}
          <div className="flex items-center justify-between">
            <p className="text-sm text-muted-foreground">
              Page 1 of 1
            </p>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" disabled>Previous</Button>
              <Button variant="outline" size="sm" disabled>Next</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentSearchPage;
