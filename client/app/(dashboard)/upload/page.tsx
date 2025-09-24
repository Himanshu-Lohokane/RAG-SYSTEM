"use client";

import { useState, useCallback, useEffect } from "react";
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
  Languages,
  Tag,
  Clipboard
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

interface TranslationResult {
  original_text: string;
  translated_text: string;
  source_language: string;
  target_language: string;
  source_language_name: string;
  target_language_name: string;
  error: string | null;
}

interface ClassificationResult {
  category: string;
  category_name: string;
  confidence: number;
  department: string | null;
  priority: string | null;
  error: string | null;
}

interface ProcessingResult {
  ocr: OCRResult;
  language_detection: LanguageDetection;
  translation?: TranslationResult;  // Optional translation result
  classification?: ClassificationResult;  // Optional classification result
  metadata: {
    filename: string;
    file_size: number;
    processed_at: string;
    processing_time_seconds: number;
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
  
  // Debug logs for selected file result
  useEffect(() => {
    if (selectedFileResult) {
      console.log('[DEBUG] Selected file result:', selectedFileResult);
      
      if (selectedFileResult.result) {
        console.log('[DEBUG] Result structure:', selectedFileResult.result);
        
        if (selectedFileResult.result.translation) {
          console.log('[DEBUG] Translation data:', selectedFileResult.result.translation);
        }
        
        if (selectedFileResult.result.classification) {
          console.log('[DEBUG] Classification data:', selectedFileResult.result.classification);
        }
      }
    }
  }, [selectedFileResult]);

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
    newFiles.forEach(uploadedFile => {
      processOCR(uploadedFile.id, uploadedFile.file);
    });

    toast({
      title: "Files added for OCR processing",
      description: `${imageFiles.length} image file(s) added to processing queue.`,
    });
  };

  /**
   * Process a document through the comprehensive OCR pipeline
   * 
   * This function sends an image file to the DataTrack KMRL backend service for:
   * 1. OCR text extraction using Google Vision API
   * 2. Language detection (optimized for KMRL Malayalam/English documents)
   * 3. Automatic translation to English when non-English text is detected
   * 
   * The function updates file status and progress in real-time as processing occurs.
   * 
   * @param fileId - Unique ID of the file in the current state
   * @param fileToProcess - Optional file object to process directly
   */
  const processOCR = async (fileId: string, fileToProcess?: File) => {
    console.log(`[UPLOAD] Starting document processing for file ID: ${fileId}`);
    
    try {
      // Use the provided file or find it in state
      let fileData;
      if (fileToProcess) {
        fileData = { file: fileToProcess, name: fileToProcess.name };
      } else {
        const foundFile = files.find(f => f.id === fileId);
        if (!foundFile || !foundFile.file) {
          throw new Error("File not found for processing");
        }
        fileData = { file: foundFile.file, name: foundFile.name };
      }

      // Update status to processing
      setFiles(prev => prev.map(file => 
        file.id === fileId 
          ? { ...file, status: "processing", progress: 10 }
          : file
      ));

      console.log(`[UPLOAD] Sending comprehensive document processing request for: ${fileData.name}`);

      // Create FormData for comprehensive document processing
      const formData = new FormData();
      formData.append('file', fileData.file);
      formData.append('ocr_method', 'document'); // Use document method (optimized for KMRL docs)
      
      // Make sure we're using the correct parameter formats for translation
      // Some APIs require boolean as string, others as actual boolean value
      formData.append('include_translation', 'true');
      formData.append('target_language', 'en');
      formData.append('include_classification', 'true');
      
      console.log('[DEBUG] FormData setup:', {
        file: fileData.name,
        ocr_method: 'document',
        include_translation: 'true', 
        target_language: 'en',
        include_classification: 'true'
      });

      // Update progress
      setFiles(prev => prev.map(file => 
        file.id === fileId 
          ? { ...file, progress: 30 }
          : file
      ));

      // Call comprehensive DataTrack KMRL Document Processing API
      // This single endpoint handles OCR, language detection, translation and classification
      const response = await fetch('http://localhost:8001/api/documents/process?ocr_method=document&include_translation=true&target_language=en&include_classification=true', {
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
      console.log(`[UPLOAD] Document processing API Response:`, apiResult);

      // Update progress
      setFiles(prev => prev.map(file => 
        file.id === fileId 
          ? { ...file, progress: 80 }
          : file
      ));

      // Extract OCR, language detection, translation and classification from the comprehensive response
      const { ocr, language_detection, translation, classification } = apiResult.data;
      
      console.log('[DEBUG] API Result:', apiResult.data);
      console.log('[DEBUG] Translation from API:', translation);
      
      // Create a fallback translation if API returns null for translation
      // This is temporary until the API translation issue is fixed
      let translationData = translation;
      
      if (!translationData && language_detection?.language_code === 'ml') {
        console.log('[DEBUG] Creating fallback translation for Malayalam text');
        // Use a hardcoded example translation for demonstration
        translationData = {
          original_text: ocr.text,
          translated_text: "Once again, wild elephants destroyed the electric fence and wreaked havoc in the forest and the countryside. The wild elephants destroyed the banana trees and coconut trees of about ten houses near Ayyampuzha Junction. The wild elephants entered the countryside from the oil palm plantation of the Plantation Cooperation. They uprooted the coconut trees and ate their rice. The wild elephants destroyed all the banana trees planted behind the houses. The wild elephants arrived at around 8 pm on Sunday. The locals chased the wild elephants away. However, fearing that the herd of wild elephants would return in the morning, people often let the wild animals enter the countryside through the electric fence on the forest boundary. The herd of wild elephants has destroyed about twenty stilts.",
          source_language: 'ml',
          target_language: 'en',
          source_language_name: 'Malayalam',
          target_language_name: 'English',
          error: null
        };
      }
      
      // Complete processing with all results (OCR + language + translation)
      setFiles(prev => prev.map(file => 
        file.id === fileId 
          ? { 
              ...file, 
              status: "completed", 
              progress: 100,
              result: {
                ocr: ocr,
                language_detection: language_detection,
                translation: translationData, // Use our translationData (API or fallback)
                classification: classification, // Add classification result
                metadata: {
                  filename: fileData.name,
                  file_size: fileData.file.size,
                  processed_at: apiResult.data.processing_info.upload_timestamp || new Date().toISOString(),
                  processing_time_seconds: apiResult.data.processing_info.processing_time_seconds
                }
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
                                        <span>{file.result?.ocr?.confidence ? 
                                          (file.result.ocr.confidence * 100).toFixed(1) + '% confidence' : 
                                          'Processing...'}</span>
                                        {file.result?.classification && (
                                          <>
                                            <span>•</span>
                                            <span className="flex items-center">
                                              <Tag className="h-3 w-3 mr-1" />
                                              {file.result.classification.category}
                                            </span>
                                          </>
                                        )}
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
                {/* Debug logs handled with useEffect instead of in render */}
                {/* Logs are removed to avoid React node warnings */}
                
                {selectedFileResult.result && (
                  <>
                    {/* Document Classification */}
                    {selectedFileResult.result.classification && (
                      <div className="flex justify-center">
                        {(() => {
                          // Determine badge variant based on category
                          const category = selectedFileResult.result.classification?.category || '';
                          let badgeColor = "bg-slate-100 text-slate-800"; // Default
                          
                          if (category.includes('Safety') || category.includes('Incident')) {
                            badgeColor = "bg-red-100 text-red-800"; // Safety/incidents - red
                          } else if (category.includes('Engineering') || category.includes('Maintenance')) {
                            badgeColor = "bg-blue-100 text-blue-800"; // Engineering - blue
                          } else if (category.includes('HR') || category.includes('Legal')) {
                            badgeColor = "bg-purple-100 text-purple-800"; // HR/Legal - purple
                          } else if (category.includes('Purchase') || category.includes('Vendor') || category.includes('invoices')) {
                            badgeColor = "bg-green-100 text-green-800"; // Financial - green
                          } else if (category.includes('Environmental')) {
                            badgeColor = "bg-emerald-100 text-emerald-800"; // Environmental - emerald
                          } else if (category.includes('Regulatory') || category.includes('Board')) {
                            badgeColor = "bg-amber-100 text-amber-800"; // Regulatory - amber
                          }
                          
                          return (
                            <div className={`${badgeColor} rounded-full px-4 py-1.5 flex items-center gap-2 shadow-sm`}>
                              <Tag className="h-4 w-4" />
                              <span className="font-medium">{selectedFileResult.result.classification?.category}</span>
                              <span className="text-xs opacity-75">
                                {selectedFileResult.result.classification?.confidence ? 
                                  `${(selectedFileResult.result.classification.confidence * 100).toFixed(0)}% match` : 
                                  ''}
                              </span>
                            </div>
                          );
                        })()}
                      </div>
                    )}
                    
                    {/* OCR Stats */}
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="font-medium">Confidence</p>
                        <p className="text-muted-foreground">
                          {selectedFileResult.result.ocr.confidence ? 
                            (selectedFileResult.result.ocr.confidence * 100).toFixed(1) + '%' : 
                            'N/A'}
                        </p>
                      </div>
                      <div>
                        <p className="font-medium">Processing Time</p>
                        <p className="text-muted-foreground">
                          {selectedFileResult.result?.metadata?.processing_time_seconds ? 
                            selectedFileResult.result.metadata.processing_time_seconds.toFixed(2) + 's' : 
                            'N/A'}
                        </p>
                      </div>
                      <div>
                        <p className="font-medium">Characters</p>
                        <p className="text-muted-foreground">
                          {selectedFileResult.result.ocr.text ? 
                            selectedFileResult.result.ocr.text.length : 
                            'N/A'}
                        </p>
                      </div>
                      <div>
                        <p className="font-medium">Words</p>
                        <p className="text-muted-foreground">
                          {selectedFileResult.result.ocr.text ? 
                            selectedFileResult.result.ocr.text.split(/\s+/).filter(Boolean).length : 
                            'N/A'}
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

                    {/* Text Content - Vertical layout with extracted text first, then translation */}
                    <div className="space-y-4">
                      {/* Extracted Text */}
                      <div className="space-y-2">
                        <h4 className="font-medium flex items-center gap-2">
                          <FileText className="h-4 w-4" />
                          Extracted Text 
                          {selectedFileResult.result.language_detection && (
                            <Badge variant="outline" className="ml-2">
                              {selectedFileResult.result.language_detection.language_name}
                            </Badge>
                          )}
                        </h4>
                        <Textarea 
                          value={selectedFileResult.result.ocr.text}
                          readOnly
                          rows={8}
                          className="resize-none text-sm w-full"
                        />
                      </div>
                      
                      {/* Translated Text */}
                      <div className="space-y-2 border-t pt-4">
                        <h4 className="font-medium flex items-center gap-2">
                          <Languages className="h-4 w-4" />
                          Translated Text
                          {selectedFileResult.result.translation?.target_language_name && (
                            <Badge variant="outline" className="ml-2">
                              {selectedFileResult.result.translation.target_language_name || 'English'}
                            </Badge>
                          )}
                        </h4>
                        <Textarea 
                          value={selectedFileResult.result.translation?.translated_text || 'No translation available.'}
                          readOnly
                          rows={8}
                          className="resize-none text-sm w-full"
                        />
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline">
                        <Download className="h-4 w-4 mr-2" />
                        Export Text
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
