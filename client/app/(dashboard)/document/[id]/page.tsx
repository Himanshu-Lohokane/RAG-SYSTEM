"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { Textarea } from "@/components/ui/textarea";
import { 
  Download, 
  Share2, 
  Edit, 
  Trash2, 
  FileText, 
  User, 
  Calendar, 
  FolderOpen,
  Tag,
  Shield,
  Clock,
  MessageSquare,
  Star,
  Eye
} from "lucide-react";

const DocumentViewerPage = () => {
  const params = useParams();
  const id = params.id as string;
  const [comments, setComments] = useState([
    {
      id: 1,
      author: "John Doe",
      date: "2024-06-15 10:30",
      text: "This document has been reviewed and approved for compliance.",
      type: "approval"
    },
    {
      id: 2,
      author: "Sarah Smith",
      date: "2024-06-14 15:45",
      text: "Please review section 3.2 for accuracy before final approval.",
      type: "review"
    }
  ]);

  // Mock document data
  const document = {
    id: id || "1",
    title: "Safety Compliance Report Q2 2024",
    type: "PDF",
    department: "Safety & Compliance",
    uploadedBy: "John Doe",
    uploadDate: "2024-06-15",
    modifiedDate: "2024-06-16",
    size: "2.4 MB",
    tags: ["safety", "compliance", "quarterly"],
    status: "approved",
    compliance: true,
    description: "Comprehensive safety compliance report covering Q2 2024 operations, including incident analysis, safety metrics, and regulatory compliance status.",
    version: "1.2",
    classification: "Internal",
    retentionPeriod: "7 years",
    nextReview: "2024-12-15"
  };

  const extractedEntities = [
    { type: "Person", value: "John Doe", confidence: 0.95 },
    { type: "Organization", value: "KMRL", confidence: 0.98 },
    { type: "Date", value: "Q2 2024", confidence: 0.92 },
    { type: "Location", value: "Kochi", confidence: 0.88 },
    { type: "Document Type", value: "Safety Report", confidence: 0.96 }
  ];

  const addComment = (text: string) => {
    const newComment = {
      id: comments.length + 1,
      author: "Current User",
      date: new Date().toLocaleString(),
      text,
      type: "comment"
    };
    setComments([...comments, newComment]);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <FileText className="h-6 w-6 text-primary" />
            <h1 className="text-2xl font-bold text-foreground">{document.title}</h1>
          </div>
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <span className="flex items-center gap-1">
              <FolderOpen className="h-4 w-4" />
              {document.department}
            </span>
            <span className="flex items-center gap-1">
              <User className="h-4 w-4" />
              {document.uploadedBy}
            </span>
            <span className="flex items-center gap-1">
              <Calendar className="h-4 w-4" />
              {document.uploadDate}
            </span>
            <Badge variant={document.status === "approved" ? "default" : "secondary"}>
              {document.status}
            </Badge>
            {document.compliance && (
              <Badge variant="outline" className="text-success border-success">
                <Shield className="h-3 w-3 mr-1" />
                Compliant
              </Badge>
            )}
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Star className="h-4 w-4 mr-2" />
            Favorite
          </Button>
          <Button variant="outline">
            <Share2 className="h-4 w-4 mr-2" />
            Share
          </Button>
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Download
          </Button>
          <Button variant="outline">
            <Edit className="h-4 w-4 mr-2" />
            Edit
          </Button>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Document Viewer */}
          <Card>
            <CardHeader>
              <CardTitle>Document Preview</CardTitle>
              <CardDescription>
                {document.type} • {document.size} • Version {document.version}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="border-2 border-dashed border-border rounded-lg p-12 text-center bg-muted/20">
                <FileText className="h-16 w-16 mx-auto mb-4 text-muted-foreground" />
                <h3 className="text-lg font-semibold mb-2">Document Preview</h3>
                <p className="text-muted-foreground mb-4">
                  Document viewer would be embedded here
                </p>
                <div className="flex gap-2 justify-center">
                  <Button>
                    <Eye className="h-4 w-4 mr-2" />
                    Open in New Tab
                  </Button>
                  <Button variant="outline">
                    <Download className="h-4 w-4 mr-2" />
                    Download Original
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Tabs */}
          <Tabs defaultValue="details" className="space-y-4">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="details">Details</TabsTrigger>
              <TabsTrigger value="ai-insights">AI Insights</TabsTrigger>
              <TabsTrigger value="history">History</TabsTrigger>
              <TabsTrigger value="compliance">Compliance</TabsTrigger>
            </TabsList>

            <TabsContent value="details">
              <Card>
                <CardHeader>
                  <CardTitle>Document Details</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <Label className="text-sm font-medium text-muted-foreground">Classification</Label>
                      <p className="text-sm">{document.classification}</p>
                    </div>
                    <div>
                      <Label className="text-sm font-medium text-muted-foreground">Retention Period</Label>
                      <p className="text-sm">{document.retentionPeriod}</p>
                    </div>
                    <div>
                      <Label className="text-sm font-medium text-muted-foreground">Next Review</Label>
                      <p className="text-sm">{document.nextReview}</p>
                    </div>
                    <div>
                      <Label className="text-sm font-medium text-muted-foreground">Last Modified</Label>
                      <p className="text-sm">{document.modifiedDate}</p>
                    </div>
                  </div>
                  <Separator />
                  <div>
                    <Label className="text-sm font-medium text-muted-foreground">Description</Label>
                    <p className="text-sm mt-1">{document.description}</p>
                  </div>
                  <Separator />
                  <div>
                    <Label className="text-sm font-medium text-muted-foreground">Tags</Label>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {document.tags.map((tag) => (
                        <Badge key={tag} variant="secondary">
                          <Tag className="h-3 w-3 mr-1" />
                          {tag}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="ai-insights">
              <Card>
                <CardHeader>
                  <CardTitle>AI-Extracted Insights</CardTitle>
                  <CardDescription>Key entities and information extracted from the document</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-3">
                    {extractedEntities.map((entity, index) => (
                      <div key={index} className="flex items-center justify-between p-3 rounded-lg border">
                        <div>
                          <p className="font-medium">{entity.value}</p>
                          <p className="text-sm text-muted-foreground">{entity.type}</p>
                        </div>
                        <Badge variant="outline">
                          {Math.round(entity.confidence * 100)}% confidence
                        </Badge>
                      </div>
                    ))}
                  </div>
                  <Separator />
                  <div>
                    <h4 className="font-medium mb-2">Summary</h4>
                    <p className="text-sm text-muted-foreground">
                      This document appears to be a quarterly safety compliance report for Q2 2024, 
                      containing safety metrics, incident analysis, and regulatory compliance information 
                      for KMRL operations in Kochi.
                    </p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="history">
              <Card>
                <CardHeader>
                  <CardTitle>Version History</CardTitle>
                  <CardDescription>Track all changes and versions of this document</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      { version: "1.2", date: "2024-06-16", author: "John Doe", changes: "Updated compliance section" },
                      { version: "1.1", date: "2024-06-15", author: "Sarah Smith", changes: "Added Q2 metrics" },
                      { version: "1.0", date: "2024-06-14", author: "John Doe", changes: "Initial version" }
                    ].map((version) => (
                      <div key={version.version} className="flex items-center justify-between p-3 rounded-lg border">
                        <div>
                          <div className="flex items-center gap-2">
                            <Badge variant="outline">v{version.version}</Badge>
                            <span className="font-medium">{version.changes}</span>
                          </div>
                          <p className="text-sm text-muted-foreground mt-1">
                            {version.author} • {version.date}
                          </p>
                        </div>
                        <div className="flex gap-2">
                          <Button variant="ghost" size="sm">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <Download className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="compliance">
              <Card>
                <CardHeader>
                  <CardTitle>Compliance Information</CardTitle>
                  <CardDescription>Regulatory compliance status and requirements</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="p-4 rounded-lg border border-success bg-success/10">
                      <div className="flex items-center gap-2 mb-2">
                        <Shield className="h-5 w-5 text-success" />
                        <span className="font-medium">Compliance Status</span>
                      </div>
                      <p className="text-sm text-muted-foreground">Fully Compliant</p>
                    </div>
                    <div className="p-4 rounded-lg border">
                      <div className="flex items-center gap-2 mb-2">
                        <Clock className="h-5 w-5 text-primary" />
                        <span className="font-medium">Next Review</span>
                      </div>
                      <p className="text-sm text-muted-foreground">{document.nextReview}</p>
                    </div>
                  </div>
                  <Separator />
                  <div>
                    <h4 className="font-medium mb-3">Regulatory Requirements</h4>
                    <div className="space-y-2">
                      {[
                        "Metro Railway Safety Standards - Met",
                        "Environmental Compliance - Met",
                        "Data Protection Requirements - Met",
                        "Financial Reporting Standards - Met"
                      ].map((requirement, index) => (
                        <div key={index} className="flex items-center gap-2">
                          <Shield className="h-4 w-4 text-success" />
                          <span className="text-sm">{requirement}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Comments */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MessageSquare className="h-5 w-5" />
                Comments
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                {comments.map((comment) => (
                  <div key={comment.id} className="p-3 rounded-lg border">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium">{comment.author}</span>
                      <span className="text-xs text-muted-foreground">{comment.date}</span>
                    </div>
                    <p className="text-sm">{comment.text}</p>
                  </div>
                ))}
              </div>
              <div className="space-y-2">
                <Textarea placeholder="Add a comment..." />
                <Button size="sm" className="w-full">
                  Add Comment
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Related Documents */}
          <Card>
            <CardHeader>
              <CardTitle>Related Documents</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {[
                "Safety Protocol Guidelines",
                "Q1 2024 Safety Report", 
                "Safety Guidelines v2.1",
                "Incident Report Template"
              ].map((title, index) => (
                <div key={index} className="p-2 rounded border text-sm hover:bg-muted cursor-pointer">
                  <FileText className="h-3 w-3 inline mr-2" />
                  {title}
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

function Label({ className, children, ...props }: React.LabelHTMLAttributes<HTMLLabelElement>) {
  return (
    <label className={`text-sm font-medium ${className || ""}`} {...props}>
      {children}
    </label>
  );
}

export default DocumentViewerPage;
