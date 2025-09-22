"use client";

import { useState, useCallback } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { 
  Upload, 
  FileText, 
  Image, 
  File, 
  CheckCircle, 
  Clock, 
  AlertCircle,
  X,
  Plus,
  Eye,
  Download,
  Languages
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface OCRResult {
  text: string;
  confidence: number;
  method: string;
  processing_time_seconds: number;
  character_count: number;
  word_count: number;
}

interface LanguageDetection {
  language_code: string;
  language_name: string;
  confidence: number;
  is_kmrl_primary: boolean;
}

interface ProcessingResult {
  ocr: OCRResult;
  language_detection: LanguageDetection;
  metadata: {
    filename: string;
    file_size: number;
    processed_at: string;
  };
}

interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: string;
  status: "uploading" | "processing" | "completed" | "error";
  progress: number;
  error?: string;
  result?: ProcessingResult;
  file?: File; // Store original file for processing
}

const DocumentUploadPage = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [dragActive, setDragActive] = useState(false);
  const [selectedFileResult, setSelectedFileResult] = useState<UploadedFile | null>(null);
  const { toast } = useToast();

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    processFiles(droppedFiles);
  }, []);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      processFiles(selectedFiles);
    }
  };

  const processFiles = (fileList: File[]) => {
    // Filter for image files only (for OCR processing)
    const imageFiles = fileList.filter(file => file.type.startsWith('image/'));
    const nonImageFiles = fileList.filter(file => !file.type.startsWith('image/'));

    if (nonImageFiles.length > 0) {
      toast({
        title: "File type notice",
        description: `${nonImageFiles.length} non-image file(s) skipped. OCR processing only supports images.`,
        variant: "destructive"
      });
    }

    if (imageFiles.length === 0) {
      toast({
        title: "No valid files",
        description: "Please upload image files (PNG, JPG, JPEG) for OCR processing.",
        variant: "destructive"
      });
      return;
    }

    const newFiles: UploadedFile[] = imageFiles.map(file => ({
      id: Math.random().toString(36).substring(7),
      name: file.name,
      size: file.size,
      type: file.type,
      status: "uploading",
      progress: 0,
      file: file
    }));

    setFiles(prev => [...prev, ...newFiles]);

    // Start OCR processing for each file
    newFiles.forEach(file => {
      processOCR(file.id);
    });

    toast({
      title: "Files added for OCR processing",
      description: `${imageFiles.length} image file(s) added to processing queue.`,
    });
  };

  const processOCR = async (fileId: string) => {
    console.log(`[UPLOAD] Starting OCR processing for file ID: ${fileId}`);
    
    try {
      // Find the file
      const fileData = files.find(f => f.id === fileId) || 
                      [...files].find(f => f.id === fileId);
      
      if (!fileData || !fileData.file) {
        throw new Error("File not found for processing");
      }

      // Update status to processing
      setFiles(prev => prev.map(file => 
        file.id === fileId 
          ? { ...file, status: "processing", progress: 10 }
          : file
      ));

      console.log(`[UPLOAD] Sending OCR request for: ${fileData.name}`);

      // Create FormData for API request
      const formData = new FormData();
      formData.append('file', fileData.file);
      formData.append('ocr_method', 'document'); // Use document method for KMRL docs

      // Update progress
      setFiles(prev => prev.map(file => 
        file.id === fileId 
          ? { ...file, progress: 30 }
          : file
      ));

      // Call DataTrack KMRL OCR API
      const response = await fetch('http://localhost:8001/api/ocr/extract-text', {
        method: 'POST',
        body: formData,
      });

      setFiles(prev => prev.map(file => 
        file.id === fileId 
          ? { ...file, progress: 60 }
          : file
      ));

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `API Error: ${response.status}`);
      }

      const apiResult = await response.json();
      console.log(`[UPLOAD] OCR API Response:`, apiResult);

      // Update progress
      setFiles(prev => prev.map(file => 
        file.id === fileId 
          ? { ...file, progress: 80 }
          : file
      ));

      // Get language detection
      let languageResult = null;
      if (apiResult.data.text) {
        try {
          const langResponse = await fetch('http://localhost:8001/api/language/detect', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: apiResult.data.text }),
          });

          if (langResponse.ok) {
            const langData = await langResponse.json();
            languageResult = langData.data;
            console.log(`[UPLOAD] Language detected:`, languageResult);
          }
        } catch (error) {
          console.warn(`[UPLOAD] Language detection failed:`, error);
        }
      }

      // Complete processing
      setFiles(prev => prev.map(file => 
        file.id === fileId 
          ? { 
              ...file, 
              status: "completed", 
              progress: 100,
              result: {
                ocr: apiResult.data,
                language_detection: languageResult,
                metadata: apiResult.metadata
              }
            }
          : file
      ));

      console.log(`[UPLOAD] ✅ OCR processing completed for: ${fileData.name}`);
      
      toast({
        title: "OCR Processing Complete",
        description: `Successfully processed ${fileData.name}. ${apiResult.data.character_count} characters extracted.`,
      });

    } catch (error) {
      console.error(`[UPLOAD] ❌ OCR processing failed for file ${fileId}:`, error);
      
      setFiles(prev => prev.map(file => 
        file.id === fileId 
          ? { 
              ...file, 
              status: "error", 
              progress: 100,
              error: error instanceof Error ? error.message : "Processing failed"
            }
          : file
      ));

      toast({
        title: "OCR Processing Failed",
        description: `Failed to process file: ${error instanceof Error ? error.message : "Unknown error"}`,
        variant: "destructive"
      });
    }
  };

  const removeFile = (fileId: string) => {
    setFiles(prev => prev.filter(file => file.id !== fileId));
    if (selectedFileResult?.id === fileId) {
      setSelectedFileResult(null);
    }
  };

  const viewResult = (file: UploadedFile) => {
    setSelectedFileResult(file);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const getFileIcon = (type: string) => {
    if (type.startsWith("image/")) return Image;
    if (type.includes("pdf") || type.includes("document")) return FileText;
    return File;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed": return CheckCircle;
      case "processing": return Clock;
      case "error": return AlertCircle;
      default: return Clock;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">DataTrack OCR Document Upload</h1>
        <p className="text-muted-foreground">Upload images for AI-powered OCR processing with English/Malayalam support</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Left side - Upload and File List */}
        <div className="lg:col-span-2 space-y-6">
          <Tabs defaultValue="upload" className="space-y-4">
            <TabsList>
              <TabsTrigger value="upload">
                <Upload className="h-4 w-4 mr-2" />
                Upload Images
              </TabsTrigger>
            </TabsList>

            <TabsContent value="upload" className="space-y-4">
              {/* Upload Area */}
              <Card>
                <CardContent className="p-6">
                  <div
                    className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                      dragActive 
                        ? "border-primary bg-primary/5" 
                        : "border-border hover:border-primary/50"
                    }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                  >
                    <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                    <h3 className="text-lg font-semibold mb-2">Drag and drop images here</h3>
                    <p className="text-muted-foreground mb-4">
                      Upload images for OCR text extraction
                    </p>
                    <input
                      type="file"
                      multiple
                      onChange={handleFileInput}
                      className="hidden"
                      id="file-upload"
                      accept="image/*"
                    />
                    <Button 
                      className="bg-gradient-primary"
                      onClick={() => document.getElementById('file-upload')?.click()}
                    >
                      <Plus className="h-4 w-4 mr-2" />
                      Select Images
                    </Button>
                    <p className="text-xs text-muted-foreground mt-2">
                      Supported formats: JPG, PNG, JPEG • Max 50MB per file
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* KMRL OCR Info */}
              <Alert>
                <Languages className="h-4 w-4" />
                <AlertDescription>
                  <strong>KMRL OCR Processing:</strong> Supports English and Malayalam text extraction with high accuracy. 
                  Optimized for documents, forms, and technical drawings.
                </AlertDescription>
              </Alert>

              {/* File List */}
              {files.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Processing Queue</CardTitle>
                    <CardDescription>
                      {files.length} file(s) • {files.filter(f => f.status === 'completed').length} completed
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {files.map((file) => {
                      const FileIcon = getFileIcon(file.type);
                      const StatusIcon = getStatusIcon(file.status);
                      return (
                        <Card key={file.id} className="cursor-pointer hover:shadow-md transition-shadow">
                          <div className="relative p-4">
                            {/* Status Badge */}
                            <div className="absolute top-2 right-2 flex gap-2">
                              {file.result?.language_detection && (
                                <Badge variant="outline" className="text-xs">
                                  <Languages className="h-3 w-3 mr-1" />
                                  {file.result.language_detection.language_name}
                                </Badge>
                              )}
                              <Badge 
                                variant={file.status === "completed" ? "default" : file.status === "error" ? "destructive" : "secondary"}
                                className="text-xs"
                              >
                                <StatusIcon className="h-3 w-3 mr-1" />
                                {file.status}
                              </Badge>
                            </div>

                            <div className="flex items-center gap-4 pr-32">
                              {/* File Icon */}
                              <div className="w-10 h-10 bg-muted rounded-lg flex items-center justify-center flex-shrink-0">
                                <FileIcon className="h-5 w-5 text-muted-foreground" />
                              </div>
                              
                              <div className="flex-1 min-w-0 space-y-3">
                                {/* File Info */}
                                <div className="space-y-1">
                                  <p className="text-sm font-medium truncate">{file.name}</p>
                                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                                    <span>{formatFileSize(file.size)}</span>
                                    {file.result?.ocr && (
                                      <>
                                        <span>•</span>
                                        <span>{file.result.ocr.character_count} chars</span>
                                        <span>•</span>
                                        <span>{(file.result.ocr.confidence * 100).toFixed(1)}% confidence</span>
                                      </>
                                    )}
                                  </div>
                                </div>
                                
                                {/* Progress Bar */}
                                <div className="space-y-1">
                                  <div className="flex items-center justify-between text-xs">
                                    <span className="text-muted-foreground">
                                      {file.status === "uploading" ? "Uploading..." : 
                                       file.status === "processing" ? "Processing OCR..." :
                                       file.status === "completed" ? "OCR Completed" : 
                                       file.error || "Error"}
                                    </span>
                                    <span className="font-medium">{file.progress}%</span>
                                  </div>
                                  <Progress value={file.progress} className="h-2" />
                                </div>
                              </div>
                            </div>

                            {/* Action Buttons */}
                            <div className="absolute top-2 right-20 flex gap-1">
                              {file.status === "completed" && file.result && (
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={() => viewResult(file)}
                                  className="h-6 w-6 p-0"
                                >
                                  <Eye className="h-3 w-3" />
                                </Button>
                              )}
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => removeFile(file.id)}
                                className="h-6 w-6 p-0 opacity-60 hover:opacity-100"
                              >
                                <X className="h-3 w-3" />
                              </Button>
                            </div>
                          </div>
                        </Card>
                      );
                    })}
                  </CardContent>
                </Card>
              )}
            </TabsContent>
          </Tabs>
        </div>

        {/* Right side - OCR Results */}
        <div className="space-y-6">
          {selectedFileResult ? (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  OCR Results
                </CardTitle>
                <CardDescription>{selectedFileResult.name}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {selectedFileResult.result && (
                  <>
                    {/* OCR Stats */}
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="font-medium">Confidence</p>
                        <p className="text-muted-foreground">
                          {(selectedFileResult.result.ocr.confidence * 100).toFixed(1)}%
                        </p>
                      </div>
                      <div>
                        <p className="font-medium">Processing Time</p>
                        <p className="text-muted-foreground">
                          {selectedFileResult.result.ocr.processing_time_seconds.toFixed(2)}s
                        </p>
                      </div>
                      <div>
                        <p className="font-medium">Characters</p>
                        <p className="text-muted-foreground">
                          {selectedFileResult.result.ocr.character_count}
                        </p>
                      </div>
                      <div>
                        <p className="font-medium">Words</p>
                        <p className="text-muted-foreground">
                          {selectedFileResult.result.ocr.word_count}
                        </p>
                      </div>
                    </div>

                    {/* Language Detection */}
                    {selectedFileResult.result.language_detection && (
                      <div className="space-y-2">
                        <h4 className="font-medium flex items-center gap-2">
                          <Languages className="h-4 w-4" />
                          Detected Language
                        </h4>
                        <Badge 
                          variant={selectedFileResult.result.language_detection.is_kmrl_primary ? "default" : "secondary"}
                          className="text-xs"
                        >
                          {selectedFileResult.result.language_detection.language_name}
                          {selectedFileResult.result.language_detection.is_kmrl_primary && " (KMRL Primary)"}
                        </Badge>
                      </div>
                    )}

                    {/* Extracted Text */}
                    <div className="space-y-2">
                      <h4 className="font-medium">Extracted Text</h4>
                      <Textarea 
                        value={selectedFileResult.result.ocr.text}
                        readOnly
                        rows={8}
                        className="resize-none text-sm"
                      />
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline">
                        <Download className="h-4 w-4 mr-2" />
                        Export Text
                      </Button>
                      <Button size="sm" variant="outline">
                        <Languages className="h-4 w-4 mr-2" />
                        Translate
                      </Button>
                    </div>
                  </>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="p-6 text-center">
                <FileText className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <h3 className="font-medium mb-2">No file selected</h3>
                <p className="text-sm text-muted-foreground">
                  Upload and process an image to view OCR results here.
                </p>
              </CardContent>
            </Card>
          )}

          {/* Processing Stats */}
          {files.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Processing Stats</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Total Files</span>
                  <span className="font-medium">{files.length}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Completed</span>
                  <span className="font-medium text-green-600">
                    {files.filter(f => f.status === 'completed').length}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Processing</span>
                  <span className="font-medium text-blue-600">
                    {files.filter(f => f.status === 'processing').length}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Failed</span>
                  <span className="font-medium text-red-600">
                    {files.filter(f => f.status === 'error').length}
                  </span>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentUploadPage;
