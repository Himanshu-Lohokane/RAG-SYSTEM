import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground">Configure your DocuMind AI preferences</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Personal Settings</CardTitle>
          <CardDescription>
            Basic configuration for your DocuMind AI experience
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Settings panel coming soon. For now, enjoy using DocuMind AI for document processing!
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Slider } from "@/components/ui/slider";
import { Textarea } from "@/components/ui/textarea";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";
import { 
  Settings as SettingsIcon,
  Bell,
  Shield,
  Zap,
  Brain,
  HardDrive,
  Globe,
  Clock,
  Key,
  Mail,
  MessageSquare,
  Database,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Copy,
  RefreshCw,
  Eye,
  EyeOff,
  GripVertical,
  Download,
  Save
} from "lucide-react";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";

export default function SettingsPage() {
  const { toast } = useToast();
  
  // General Settings State
  const [generalSettings, setGeneralSettings] = useState({
    organizationName: "Kochi Metro Rail Limited",
    timezone: "Asia/Kolkata",
    language: "English",
    dateFormat: "DD/MM/YYYY",
    autoSave: true,
    debugMode: false
  });

  // File Processing Settings
  const [fileSettings, setFileSettings] = useState({
    maxFileSize: [50], // MB
    supportedFormats: {
      pdf: true,
      docx: true,
      xlsx: true,
      pptx: true,
      txt: true,
      csv: true,
      jpg: false,
      png: false
    },
    ocrEnabled: true,
    autoClassification: true
  });

  // Notification Settings
  const [notificationSettings, setNotificationSettings] = useState({
    emailNotifications: true,
    smsNotifications: false,
    documentProcessed: { email: true, sms: false, frequency: "immediate" },
    systemAlerts: { email: true, sms: true, frequency: "immediate" },
    weeklyReports: { email: true, sms: false, frequency: "weekly" },
    maintenanceAlerts: { email: true, sms: false, frequency: "immediate" }
  });

  // Security Settings
  const [securitySettings, setSecuritySettings] = useState({
    passwordMinLength: [8],
    requireTwoFactor: false,
    sessionTimeout: [60], // minutes
    maxLoginAttempts: [3],
    enableIPWhitelist: false,
    ipWhitelist: "",
    dataEncryption: true,
    auditLogging: true
  });

  // AI & ML Settings
  const [aiSettings, setAiSettings] = useState({
    aiProcessingEnabled: true,
    confidenceThreshold: [0.85],
    autoApprovalThreshold: [0.95],
    modelVersion: "v2.1.0",
    enablePreview: false
  });

  // System Performance Settings
  const [performanceSettings, setPerformanceSettings] = useState({
    maxConcurrentProcessing: [5],
    batchSize: [10],
    cacheEnabled: true,
    compressionEnabled: true,
    cdnEnabled: true
  });

  // Backup & Recovery Settings
  const [backupSettings, setBackupSettings] = useState({
    autoBackupEnabled: true,
    backupFrequency: "daily",
    retentionPeriod: [30], // days
    cloudBackupEnabled: false,
    encryptBackups: true
  });

  const handleSaveSettings = (settingType: string) => {
    toast({
      title: "Settings saved",
      description: `${settingType} settings have been successfully updated.`,
    });
  };

  const handleResetSettings = () => {
    toast({
      title: "Settings reset",
      description: "All settings have been reset to default values.",
    });
  };

  const handleExportConfig = () => {
    toast({
      title: "Configuration exported",
      description: "Settings have been exported to a configuration file.",
    });
  };

  const handleTestConnection = () => {
    toast({
      title: "Connection test",
      description: "Testing system connections...",
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">System Settings</h1>
          <p className="text-muted-foreground">Configure system preferences and operational parameters</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleExportConfig}>
            <Copy className="h-4 w-4 mr-2" />
            Export Config
          </Button>
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button variant="outline">
                <RefreshCw className="h-4 w-4 mr-2" />
                Reset All
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Reset All Settings</AlertDialogTitle>
                <AlertDialogDescription>
                  This will reset all settings to their default values. This action cannot be undone.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction onClick={handleResetSettings}>Reset</AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </div>

      <Tabs defaultValue="general" className="space-y-6">
        <TabsList className="grid grid-cols-3 lg:grid-cols-6 w-full">
          <TabsTrigger value="general">General</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="security">Security</TabsTrigger>
          <TabsTrigger value="processing">Processing</TabsTrigger>
          <TabsTrigger value="ai">AI & ML</TabsTrigger>
          <TabsTrigger value="backup">Backup</TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Organization Settings */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <SettingsIcon className="h-5 w-5" />
                  Organization Settings
                </CardTitle>
                <CardDescription>
                  Configure basic organization information
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="orgName">Organization Name</Label>
                  <Input
                    id="orgName"
                    value={generalSettings.organizationName}
                    onChange={(e) => setGeneralSettings({
                      ...generalSettings,
                      organizationName: e.target.value
                    })}
                  />
                </div>
                <div>
                  <Label htmlFor="timezone">Timezone</Label>
                  <Select 
                    value={generalSettings.timezone}
                    onValueChange={(value) => setGeneralSettings({
                      ...generalSettings,
                      timezone: value
                    })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Asia/Kolkata">Asia/Kolkata (IST)</SelectItem>
                      <SelectItem value="UTC">UTC</SelectItem>
                      <SelectItem value="US/Eastern">US/Eastern</SelectItem>
                      <SelectItem value="Europe/London">Europe/London</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="language">Language</Label>
                  <Select 
                    value={generalSettings.language}
                    onValueChange={(value) => setGeneralSettings({
                      ...generalSettings,
                      language: value
                    })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="English">English</SelectItem>
                      <SelectItem value="Hindi">Hindi</SelectItem>
                      <SelectItem value="Malayalam">Malayalam</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="dateFormat">Date Format</Label>
                  <Select 
                    value={generalSettings.dateFormat}
                    onValueChange={(value) => setGeneralSettings({
                      ...generalSettings,
                      dateFormat: value
                    })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="DD/MM/YYYY">DD/MM/YYYY</SelectItem>
                      <SelectItem value="MM/DD/YYYY">MM/DD/YYYY</SelectItem>
                      <SelectItem value="YYYY-MM-DD">YYYY-MM-DD</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <Button onClick={() => handleSaveSettings("General")} className="w-full">
                  <Save className="h-4 w-4 mr-2" />
                  Save General Settings
                </Button>
              </CardContent>
            </Card>

            {/* System Preferences */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5" />
                  System Preferences
                </CardTitle>
                <CardDescription>
                  Configure system behavior and features
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Auto Save</p>
                    <p className="text-sm text-muted-foreground">
                      Automatically save changes
                    </p>
                  </div>
                  <Switch
                    checked={generalSettings.autoSave}
                    onCheckedChange={(checked) => setGeneralSettings({
                      ...generalSettings,
                      autoSave: checked
                    })}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Debug Mode</p>
                    <p className="text-sm text-muted-foreground">
                      Enable detailed logging
                    </p>
                  </div>
                  <Switch
                    checked={generalSettings.debugMode}
                    onCheckedChange={(checked) => setGeneralSettings({
                      ...generalSettings,
                      debugMode: checked
                    })}
                  />
                </div>
                <div className="pt-4">
                  <Button variant="outline" onClick={handleTestConnection} className="w-full">
                    <CheckCircle className="h-4 w-4 mr-2" />
                    Test System Connection
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                Notification Settings
              </CardTitle>
              <CardDescription>
                Configure how the system sends notifications
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Global Settings */}
              <div className="space-y-4">
                <h4 className="font-medium">Global Notification Settings</h4>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Email Notifications</p>
                    <p className="text-sm text-muted-foreground">Enable email notifications</p>
                  </div>
                  <Switch
                    checked={notificationSettings.emailNotifications}
                    onCheckedChange={(checked) => setNotificationSettings({
                      ...notificationSettings,
                      emailNotifications: checked
                    })}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">SMS Notifications</p>
                    <p className="text-sm text-muted-foreground">Enable SMS notifications</p>
                  </div>
                  <Switch
                    checked={notificationSettings.smsNotifications}
                    onCheckedChange={(checked) => setNotificationSettings({
                      ...notificationSettings,
                      smsNotifications: checked
                    })}
                  />
                </div>
              </div>

              {/* Specific Notification Types */}
              <div className="space-y-4">
                <h4 className="font-medium">Notification Types</h4>
                <div className="grid gap-4">
                  {Object.entries(notificationSettings).filter(([key]) => 
                    typeof notificationSettings[key as keyof typeof notificationSettings] === 'object' &&
                    notificationSettings[key as keyof typeof notificationSettings] !== null
                  ).map(([key, setting]) => (
                    <div key={key} className="p-4 border rounded-lg">
                      <h5 className="font-medium capitalize mb-3">
                        {key.replace(/([A-Z])/g, ' $1').trim()}
                      </h5>
                      <div className="grid grid-cols-3 gap-4">
                        <div className="flex items-center space-x-2">
                          <Checkbox
                            id={`${key}-email`}
                            checked={(setting as any).email}
                            onCheckedChange={(checked) => {
                              setNotificationSettings({
                                ...notificationSettings,
                                [key]: { ...(setting as any), email: checked }
                              });
                            }}
                          />
                          <Label htmlFor={`${key}-email`} className="text-sm">Email</Label>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Checkbox
                            id={`${key}-sms`}
                            checked={(setting as any).sms}
                            onCheckedChange={(checked) => {
                              setNotificationSettings({
                                ...notificationSettings,
                                [key]: { ...(setting as any), sms: checked }
                              });
                            }}
                          />
                          <Label htmlFor={`${key}-sms`} className="text-sm">SMS</Label>
                        </div>
                        <Select 
                          value={(setting as any).frequency}
                          onValueChange={(value) => {
                            setNotificationSettings({
                              ...notificationSettings,
                              [key]: { ...(setting as any), frequency: value }
                            });
                          }}
                        >
                          <SelectTrigger className="h-8">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="immediate">Immediate</SelectItem>
                            <SelectItem value="hourly">Hourly</SelectItem>
                            <SelectItem value="daily">Daily</SelectItem>
                            <SelectItem value="weekly">Weekly</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <Button onClick={() => handleSaveSettings("Notification")} className="w-full">
                <Save className="h-4 w-4 mr-2" />
                Save Notification Settings
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Authentication */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Authentication & Access
                </CardTitle>
                <CardDescription>
                  Configure security and access controls
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Minimum Password Length</Label>
                  <div className="mt-2">
                    <Slider
                      value={securitySettings.passwordMinLength}
                      onValueChange={(value) => setSecuritySettings({
                        ...securitySettings,
                        passwordMinLength: value
                      })}
                      max={20}
                      min={6}
                      step={1}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-muted-foreground mt-1">
                      <span>6 chars</span>
                      <span>{securitySettings.passwordMinLength[0]} characters</span>
                      <span>20 chars</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Two-Factor Authentication</p>
                    <p className="text-sm text-muted-foreground">Require 2FA for all users</p>
                  </div>
                  <Switch
                    checked={securitySettings.requireTwoFactor}
                    onCheckedChange={(checked) => setSecuritySettings({
                      ...securitySettings,
                      requireTwoFactor: checked
                    })}
                  />
                </div>
                <div>
                  <Label>Session Timeout (minutes)</Label>
                  <div className="mt-2">
                    <Slider
                      value={securitySettings.sessionTimeout}
                      onValueChange={(value) => setSecuritySettings({
                        ...securitySettings,
                        sessionTimeout: value
                      })}
                      max={480}
                      min={15}
                      step={15}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-muted-foreground mt-1">
                      <span>15 min</span>
                      <span>{securitySettings.sessionTimeout[0]} minutes</span>
                      <span>8 hours</span>
                    </div>
                  </div>
                </div>
                <div>
                  <Label>Max Login Attempts</Label>
                  <div className="mt-2">
                    <Slider
                      value={securitySettings.maxLoginAttempts}
                      onValueChange={(value) => setSecuritySettings({
                        ...securitySettings,
                        maxLoginAttempts: value
                      })}
                      max={10}
                      min={2}
                      step={1}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-muted-foreground mt-1">
                      <span>2 attempts</span>
                      <span>{securitySettings.maxLoginAttempts[0]} attempts</span>
                      <span>10 attempts</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Data Security */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Key className="h-5 w-5" />
                  Data Security
                </CardTitle>
                <CardDescription>
                  Configure data protection and monitoring
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">IP Whitelist</p>
                    <p className="text-sm text-muted-foreground">Restrict access by IP address</p>
                  </div>
                  <Switch
                    checked={securitySettings.enableIPWhitelist}
                    onCheckedChange={(checked) => setSecuritySettings({
                      ...securitySettings,
                      enableIPWhitelist: checked
                    })}
                  />
                </div>
                {securitySettings.enableIPWhitelist && (
                  <div>
                    <Label htmlFor="ipWhitelist">Allowed IP Addresses</Label>
                    <Textarea
                      id="ipWhitelist"
                      placeholder="Enter IP addresses, one per line"
                      value={securitySettings.ipWhitelist}
                      onChange={(e) => setSecuritySettings({
                        ...securitySettings,
                        ipWhitelist: e.target.value
                      })}
                    />
                  </div>
                )}
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Data Encryption</p>
                    <p className="text-sm text-muted-foreground">Encrypt data at rest</p>
                  </div>
                  <Switch
                    checked={securitySettings.dataEncryption}
                    onCheckedChange={(checked) => setSecuritySettings({
                      ...securitySettings,
                      dataEncryption: checked
                    })}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Audit Logging</p>
                    <p className="text-sm text-muted-foreground">Log all user actions</p>
                  </div>
                  <Switch
                    checked={securitySettings.auditLogging}
                    onCheckedChange={(checked) => setSecuritySettings({
                      ...securitySettings,
                      auditLogging: checked
                    })}
                  />
                </div>
              </CardContent>
            </Card>
          </div>
          <Button onClick={() => handleSaveSettings("Security")} className="w-full">
            <Save className="h-4 w-4 mr-2" />
            Save Security Settings
          </Button>
        </TabsContent>

        <TabsContent value="processing" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            {/* File Processing */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <HardDrive className="h-5 w-5" />
                  File Processing
                </CardTitle>
                <CardDescription>
                  Configure file upload and processing settings
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Maximum File Size (MB)</Label>
                  <div className="mt-2">
                    <Slider
                      value={fileSettings.maxFileSize}
                      onValueChange={(value) => setFileSettings({
                        ...fileSettings,
                        maxFileSize: value
                      })}
                      max={500}
                      min={1}
                      step={1}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-muted-foreground mt-1">
                      <span>1 MB</span>
                      <span>{fileSettings.maxFileSize[0]} MB</span>
                      <span>500 MB</span>
                    </div>
                  </div>
                </div>
                <div>
                  <Label>Supported File Formats</Label>
                  <div className="grid grid-cols-2 gap-2 mt-2">
                    {Object.entries(fileSettings.supportedFormats).map(([format, enabled]) => (
                      <div key={format} className="flex items-center space-x-2">
                        <Checkbox
                          id={format}
                          checked={enabled}
                          onCheckedChange={(checked) => setFileSettings({
                            ...fileSettings,
                            supportedFormats: {
                              ...fileSettings.supportedFormats,
                              [format]: checked
                            }
                          })}
                        />
                        <Label htmlFor={format} className="uppercase">{format}</Label>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">OCR Processing</p>
                    <p className="text-sm text-muted-foreground">Extract text from images</p>
                  </div>
                  <Switch
                    checked={fileSettings.ocrEnabled}
                    onCheckedChange={(checked) => setFileSettings({
                      ...fileSettings,
                      ocrEnabled: checked
                    })}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Auto Classification</p>
                    <p className="text-sm text-muted-foreground">Automatically classify documents</p>
                  </div>
                  <Switch
                    checked={fileSettings.autoClassification}
                    onCheckedChange={(checked) => setFileSettings({
                      ...fileSettings,
                      autoClassification: checked
                    })}
                  />
                </div>
              </CardContent>
            </Card>

            {/* Performance Settings */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5" />
                  Performance Settings
                </CardTitle>
                <CardDescription>
                  Configure system performance parameters
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label>Concurrent Processing Limit</Label>
                  <div className="mt-2">
                    <Slider
                      value={performanceSettings.maxConcurrentProcessing}
                      onValueChange={(value) => setPerformanceSettings({
                        ...performanceSettings,
                        maxConcurrentProcessing: value
                      })}
                      max={20}
                      min={1}
                      step={1}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-muted-foreground mt-1">
                      <span>1 file</span>
                      <span>{performanceSettings.maxConcurrentProcessing[0]} files</span>
                      <span>20 files</span>
                    </div>
                  </div>
                </div>
                <div>
                  <Label>Batch Processing Size</Label>
                  <div className="mt-2">
                    <Slider
                      value={performanceSettings.batchSize}
                      onValueChange={(value) => setPerformanceSettings({
                        ...performanceSettings,
                        batchSize: value
                      })}
                      max={50}
                      min={1}
                      step={1}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-muted-foreground mt-1">
                      <span>1 file</span>
                      <span>{performanceSettings.batchSize[0]} files</span>
                      <span>50 files</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Enable Caching</p>
                    <p className="text-sm text-muted-foreground">Cache processed results</p>
                  </div>
                  <Switch
                    checked={performanceSettings.cacheEnabled}
                    onCheckedChange={(checked) => setPerformanceSettings({
                      ...performanceSettings,
                      cacheEnabled: checked
                    })}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Data Compression</p>
                    <p className="text-sm text-muted-foreground">Compress stored data</p>
                  </div>
                  <Switch
                    checked={performanceSettings.compressionEnabled}
                    onCheckedChange={(checked) => setPerformanceSettings({
                      ...performanceSettings,
                      compressionEnabled: checked
                    })}
                  />
                </div>
              </CardContent>
            </Card>
          </div>
          <Button onClick={() => handleSaveSettings("Processing")} className="w-full">
            <Save className="h-4 w-4 mr-2" />
            Save Processing Settings
          </Button>
        </TabsContent>

        <TabsContent value="ai" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5" />
                AI & Machine Learning
              </CardTitle>
              <CardDescription>
                Configure AI processing and model settings
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">AI Processing</p>
                  <p className="text-sm text-muted-foreground">Enable AI-powered document analysis</p>
                </div>
                <Switch
                  checked={aiSettings.aiProcessingEnabled}
                  onCheckedChange={(checked) => setAiSettings({
                    ...aiSettings,
                    aiProcessingEnabled: checked
                  })}
                />
              </div>

              {aiSettings.aiProcessingEnabled && (
                <div className="space-y-4">
                  <div>
                    <Label>Confidence Threshold</Label>
                    <p className="text-sm text-muted-foreground mb-2">
                      Minimum confidence level for AI predictions
                    </p>
                    <Slider
                      value={aiSettings.confidenceThreshold}
                      onValueChange={(value) => setAiSettings({
                        ...aiSettings,
                        confidenceThreshold: value
                      })}
                      max={1}
                      min={0.5}
                      step={0.05}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-muted-foreground mt-1">
                      <span>50%</span>
                      <span>{Math.round(aiSettings.confidenceThreshold[0] * 100)}%</span>
                      <span>100%</span>
                    </div>
                  </div>

                  <div>
                    <Label>Auto-Approval Threshold</Label>
                    <p className="text-sm text-muted-foreground mb-2">
                      Confidence level for automatic approval
                    </p>
                    <Slider
                      value={aiSettings.autoApprovalThreshold}
                      onValueChange={(value) => setAiSettings({
                        ...aiSettings,
                        autoApprovalThreshold: value
                      })}
                      max={1}
                      min={0.8}
                      step={0.05}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-muted-foreground mt-1">
                      <span>80%</span>
                      <span>{Math.round(aiSettings.autoApprovalThreshold[0] * 100)}%</span>
                      <span>100%</span>
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="modelVersion">Model Version</Label>
                    <Select 
                      value={aiSettings.modelVersion}
                      onValueChange={(value) => setAiSettings({
                        ...aiSettings,
                        modelVersion: value
                      })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="v2.1.0">v2.1.0 (Current)</SelectItem>
                        <SelectItem value="v2.0.5">v2.0.5 (Stable)</SelectItem>
                        <SelectItem value="v2.2.0-beta">v2.2.0-beta (Preview)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">Enable Preview Features</p>
                      <p className="text-sm text-muted-foreground">Test experimental AI features</p>
                    </div>
                    <Switch
                      checked={aiSettings.enablePreview}
                      onCheckedChange={(checked) => setAiSettings({
                        ...aiSettings,
                        enablePreview: checked
                      })}
                    />
                  </div>
                </div>
              )}
              <Button onClick={() => handleSaveSettings("AI")} className="w-full">
                <Save className="h-4 w-4 mr-2" />
                Save AI Settings
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="backup" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5" />
                Backup & Recovery
              </CardTitle>
              <CardDescription>
                Configure backup schedules and data retention policies
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Auto Backup</p>
                  <p className="text-sm text-muted-foreground">Automatically backup system data</p>
                </div>
                <Switch
                  checked={backupSettings.autoBackupEnabled}
                  onCheckedChange={(checked) => setBackupSettings({
                    ...backupSettings,
                    autoBackupEnabled: checked
                  })}
                />
              </div>

              {backupSettings.autoBackupEnabled && (
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="backupFreq">Backup Frequency</Label>
                    <Select 
                      value={backupSettings.backupFrequency}
                      onValueChange={(value) => setBackupSettings({
                        ...backupSettings,
                        backupFrequency: value
                      })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="hourly">Hourly</SelectItem>
                        <SelectItem value="daily">Daily</SelectItem>
                        <SelectItem value="weekly">Weekly</SelectItem>
                        <SelectItem value="monthly">Monthly</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label>Retention Period (days)</Label>
                    <div className="mt-2">
                      <Slider
                        value={backupSettings.retentionPeriod}
                        onValueChange={(value) => setBackupSettings({
                          ...backupSettings,
                          retentionPeriod: value
                        })}
                        max={365}
                        min={7}
                        step={1}
                        className="w-full"
                      />
                      <div className="flex justify-between text-sm text-muted-foreground mt-1">
                        <span>7 days</span>
                        <span>{backupSettings.retentionPeriod[0]} days</span>
                        <span>365 days</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">Cloud Backup</p>
                      <p className="text-sm text-muted-foreground">Store backups in cloud storage</p>
                    </div>
                    <Switch
                      checked={backupSettings.cloudBackupEnabled}
                      onCheckedChange={(checked) => setBackupSettings({
                        ...backupSettings,
                        cloudBackupEnabled: checked
                      })}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">Encrypt Backups</p>
                      <p className="text-sm text-muted-foreground">Encrypt backup files</p>
                    </div>
                    <Switch
                      checked={backupSettings.encryptBackups}
                      onCheckedChange={(checked) => setBackupSettings({
                        ...backupSettings,
                        encryptBackups: checked
                      })}
                    />
                  </div>
                </div>
              )}

              <div className="flex gap-2 pt-4">
                <Button variant="outline" className="flex-1">
                  <Download className="h-4 w-4 mr-2" />
                  Manual Backup
                </Button>
                <Button variant="outline" className="flex-1">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Test Restore
                </Button>
              </div>

              <Button onClick={() => handleSaveSettings("Backup")} className="w-full">
                <Save className="h-4 w-4 mr-2" />
                Save Backup Settings
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
