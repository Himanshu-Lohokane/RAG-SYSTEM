"use client";

import { useState } from "react";
import { Camera, User, Shield, Bell, Clock, Edit2, Upload, Download, Trash2, Eye, EyeOff, Key, Smartphone, Globe, Save, X, Check } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Separator } from "@/components/ui/separator";
import { Progress } from "@/components/ui/progress";
import { toast } from "@/hooks/use-toast";

export default function UserProfilePage() {
  const [activeTab, setActiveTab] = useState("personal");
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState(0);
  const [twoFactorEnabled, setTwoFactorEnabled] = useState(false);
  
  // Mock user data
  const [userData, setUserData] = useState({
    name: "Dr. Sarah Johnson",
    title: "Senior Research Manager",
    role: "Manager",
    email: "sarah.johnson@kmrl.gov.in",
    phone: "+91 9876543210",
    bio: "Experienced research manager with over 10 years in marine research and data analysis. Specializes in compliance monitoring and environmental data processing.",
    employeeId: "KMRL-2019-0142",
    department: "Marine Research",
    manager: "Dr. Rajesh Kumar",
    lastLogin: "2024-01-15 09:32 AM",
    status: "Active"
  });

  const [notificationSettings, setNotificationSettings] = useState({
    emailNotifications: true,
    documentProcessing: true,
    complianceDeadlines: true,
    systemAlerts: false,
    weeklyReports: true,
    smsAlerts: false,
    pushNotifications: true,
    notificationFrequency: [60] // minutes
  });

  // Mock data for tables
  const activeSessions = [
    { id: 1, device: "Chrome - Windows", location: "Kochi, Kerala", loginTime: "2024-01-15 09:32 AM", current: true },
    { id: 2, device: "Mobile App - Android", location: "Kochi, Kerala", loginTime: "2024-01-14 06:45 PM", current: false },
    { id: 3, device: "Firefox - Windows", location: "Thiruvananthapuram, Kerala", loginTime: "2024-01-12 02:15 PM", current: false }
  ];

  const activityHistory = [
    { id: 1, action: "Document Upload", details: "Environmental_Report_2024.pdf", timestamp: "2024-01-15 08:30 AM", location: "192.168.1.100" },
    { id: 2, action: "Login", details: "Successful login", timestamp: "2024-01-15 08:15 AM", location: "192.168.1.100" },
    { id: 3, action: "Document Access", details: "Compliance_Checklist.xlsx", timestamp: "2024-01-14 04:22 PM", location: "192.168.1.100" },
    { id: 4, action: "Profile Update", details: "Updated phone number", timestamp: "2024-01-14 02:10 PM", location: "192.168.1.100" },
    { id: 5, action: "Document Download", details: "Research_Data_Q4.csv", timestamp: "2024-01-12 11:45 AM", location: "192.168.1.100" }
  ];

  const getRoleBadgeColor = (role: string) => {
    const colors = {
      Admin: "bg-destructive text-destructive-foreground",
      Manager: "bg-primary text-primary-foreground", 
      Engineer: "bg-warning text-warning-foreground",
      Officer: "bg-info text-info-foreground",
      Clerk: "bg-secondary text-secondary-foreground"
    };
    return colors[role as keyof typeof colors] || "bg-muted text-muted-foreground";
  };

  const handleSaveProfile = () => {
    setIsEditingProfile(false);
    toast({
      title: "Profile updated",
      description: "Your profile has been successfully updated.",
    });
  };

  const handlePasswordUpdate = () => {
    toast({
      title: "Password updated",
      description: "Your password has been successfully changed.",
    });
  };

  const toggleTwoFactor = () => {
    setTwoFactorEnabled(!twoFactorEnabled);
    toast({
      title: twoFactorEnabled ? "2FA disabled" : "2FA enabled",
      description: twoFactorEnabled ? "Two-factor authentication has been disabled." : "Two-factor authentication has been enabled.",
    });
  };

  const handleRevokeSession = (sessionId: number) => {
    toast({
      title: "Session revoked",
      description: "The selected session has been terminated.",
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Profile Settings</h1>
          <p className="text-muted-foreground">Manage your account settings and preferences</p>
        </div>
        <div className="flex gap-2">
          {isEditingProfile ? (
            <>
              <Button variant="outline" onClick={() => setIsEditingProfile(false)}>
                <X className="h-4 w-4 mr-2" />
                Cancel
              </Button>
              <Button onClick={handleSaveProfile}>
                <Save className="h-4 w-4 mr-2" />
                Save Changes
              </Button>
            </>
          ) : (
            <Button onClick={() => setIsEditingProfile(true)}>
              <Edit2 className="h-4 w-4 mr-2" />
              Edit Profile
            </Button>
          )}
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid grid-cols-4 w-full max-w-md">
          <TabsTrigger value="personal">Personal</TabsTrigger>
          <TabsTrigger value="security">Security</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="activity">Activity</TabsTrigger>
        </TabsList>

        <TabsContent value="personal" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Profile Card */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <User className="h-5 w-5" />
                  Personal Information
                </CardTitle>
                <CardDescription>
                  Update your personal details and job information
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Avatar Section */}
                <div className="flex items-center gap-6">
                  <div className="relative">
                    <Avatar className="h-20 w-20">
                      <AvatarImage src="/api/placeholder/80/80" alt={userData.name} />
                      <AvatarFallback className="text-lg">
                        {userData.name.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    {isEditingProfile && (
                      <Button
                        size="sm"
                        variant="outline"
                        className="absolute -bottom-2 -right-2 h-8 w-8 rounded-full p-0"
                      >
                        <Camera className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold">{userData.name}</h3>
                    <p className="text-muted-foreground">{userData.title}</p>
                    <Badge className={getRoleBadgeColor(userData.role)}>
                      {userData.role}
                    </Badge>
                  </div>
                </div>

                <Separator />

                {/* Form Fields */}
                <div className="grid gap-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="name">Full Name</Label>
                      <Input
                        id="name"
                        value={userData.name}
                        disabled={!isEditingProfile}
                        onChange={(e) => setUserData({...userData, name: e.target.value})}
                      />
                    </div>
                    <div>
                      <Label htmlFor="employeeId">Employee ID</Label>
                      <Input
                        id="employeeId"
                        value={userData.employeeId}
                        disabled
                        className="bg-muted"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="email">Email</Label>
                      <Input
                        id="email"
                        type="email"
                        value={userData.email}
                        disabled={!isEditingProfile}
                        onChange={(e) => setUserData({...userData, email: e.target.value})}
                      />
                    </div>
                    <div>
                      <Label htmlFor="phone">Phone</Label>
                      <Input
                        id="phone"
                        value={userData.phone}
                        disabled={!isEditingProfile}
                        onChange={(e) => setUserData({...userData, phone: e.target.value})}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="department">Department</Label>
                      <Input
                        id="department"
                        value={userData.department}
                        disabled
                        className="bg-muted"
                      />
                    </div>
                    <div>
                      <Label htmlFor="manager">Reporting Manager</Label>
                      <Input
                        id="manager"
                        value={userData.manager}
                        disabled
                        className="bg-muted"
                      />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="bio">Bio</Label>
                    <Textarea
                      id="bio"
                      value={userData.bio}
                      disabled={!isEditingProfile}
                      onChange={(e) => setUserData({...userData, bio: e.target.value})}
                      rows={3}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quick Stats */}
            <div className="space-y-6">
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Account Status</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Status</span>
                      <Badge variant="default">{userData.status}</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Last Login</span>
                      <span className="text-sm font-medium">{userData.lastLogin}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Member Since</span>
                      <span className="text-sm font-medium">Jan 2019</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Documents</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Uploaded</span>
                      <span className="font-medium">247</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Processed</span>
                      <span className="font-medium">189</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Shared</span>
                      <span className="font-medium">45</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="security" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Password Settings */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Password & Security
                </CardTitle>
                <CardDescription>
                  Update your password and security settings
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="current-password">Current Password</Label>
                  <div className="relative">
                    <Input
                      id="current-password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Enter current password"
                    />
                    <Button
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3 py-2"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </Button>
                  </div>
                </div>

                <div>
                  <Label htmlFor="new-password">New Password</Label>
                  <Input
                    id="new-password"
                    type="password"
                    placeholder="Enter new password"
                  />
                  <div className="mt-2">
                    <div className="flex justify-between text-sm">
                      <span>Password strength</span>
                      <span>Medium</span>
                    </div>
                    <Progress value={65} className="mt-1" />
                  </div>
                </div>

                <div>
                  <Label htmlFor="confirm-password">Confirm Password</Label>
                  <Input
                    id="confirm-password"
                    type="password"
                    placeholder="Confirm new password"
                  />
                </div>

                <Button onClick={handlePasswordUpdate} className="w-full">
                  <Key className="h-4 w-4 mr-2" />
                  Update Password
                </Button>
              </CardContent>
            </Card>

            {/* Two-Factor Authentication */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Smartphone className="h-5 w-5" />
                  Two-Factor Authentication
                </CardTitle>
                <CardDescription>
                  Add an extra layer of security to your account
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">SMS Authentication</p>
                    <p className="text-sm text-muted-foreground">
                      Receive codes via SMS
                    </p>
                  </div>
                  <Switch
                    checked={twoFactorEnabled}
                    onCheckedChange={toggleTwoFactor}
                  />
                </div>

                {twoFactorEnabled && (
                  <div className="space-y-3 p-4 border rounded-lg bg-muted/50">
                    <p className="text-sm font-medium">Backup Codes</p>
                    <p className="text-sm text-muted-foreground">
                      Generate backup codes in case you lose access to your phone
                    </p>
                    <Button variant="outline" size="sm">
                      <Download className="h-4 w-4 mr-2" />
                      Generate Codes
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Active Sessions */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5" />
                  Active Sessions
                </CardTitle>
                <CardDescription>
                  Manage your active login sessions across devices
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Device</TableHead>
                      <TableHead>Location</TableHead>
                      <TableHead>Login Time</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {activeSessions.map((session) => (
                      <TableRow key={session.id}>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            {session.device}
                            {session.current && (
                              <Badge variant="outline" className="text-xs">
                                Current
                              </Badge>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>{session.location}</TableCell>
                        <TableCell>{session.loginTime}</TableCell>
                        <TableCell className="text-right">
                          {!session.current && (
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleRevokeSession(session.id)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                Notification Preferences
              </CardTitle>
              <CardDescription>
                Choose how you want to be notified about important events
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Email Notifications</p>
                    <p className="text-sm text-muted-foreground">
                      Receive notifications via email
                    </p>
                  </div>
                  <Switch
                    checked={notificationSettings.emailNotifications}
                    onCheckedChange={(checked) =>
                      setNotificationSettings({
                        ...notificationSettings,
                        emailNotifications: checked
                      })
                    }
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Document Processing</p>
                    <p className="text-sm text-muted-foreground">
                      Alerts when documents are processed
                    </p>
                  </div>
                  <Switch
                    checked={notificationSettings.documentProcessing}
                    onCheckedChange={(checked) =>
                      setNotificationSettings({
                        ...notificationSettings,
                        documentProcessing: checked
                      })
                    }
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Compliance Deadlines</p>
                    <p className="text-sm text-muted-foreground">
                      Reminders for upcoming deadlines
                    </p>
                  </div>
                  <Switch
                    checked={notificationSettings.complianceDeadlines}
                    onCheckedChange={(checked) =>
                      setNotificationSettings({
                        ...notificationSettings,
                        complianceDeadlines: checked
                      })
                    }
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">System Alerts</p>
                    <p className="text-sm text-muted-foreground">
                      Critical system notifications
                    </p>
                  </div>
                  <Switch
                    checked={notificationSettings.systemAlerts}
                    onCheckedChange={(checked) =>
                      setNotificationSettings({
                        ...notificationSettings,
                        systemAlerts: checked
                      })
                    }
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Weekly Reports</p>
                    <p className="text-sm text-muted-foreground">
                      Weekly summary reports
                    </p>
                  </div>
                  <Switch
                    checked={notificationSettings.weeklyReports}
                    onCheckedChange={(checked) =>
                      setNotificationSettings({
                        ...notificationSettings,
                        weeklyReports: checked
                      })
                    }
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">SMS Alerts</p>
                    <p className="text-sm text-muted-foreground">
                      Urgent notifications via SMS
                    </p>
                  </div>
                  <Switch
                    checked={notificationSettings.smsAlerts}
                    onCheckedChange={(checked) =>
                      setNotificationSettings({
                        ...notificationSettings,
                        smsAlerts: checked
                      })
                    }
                  />
                </div>
              </div>

              <Separator />

              <div>
                <Label>Notification Frequency</Label>
                <p className="text-sm text-muted-foreground mb-3">
                  How often should we send you notifications? (in minutes)
                </p>
                <Slider
                  value={notificationSettings.notificationFrequency}
                  onValueChange={(value) =>
                    setNotificationSettings({
                      ...notificationSettings,
                      notificationFrequency: value
                    })
                  }
                  max={240}
                  min={15}
                  step={15}
                  className="w-full"
                />
                <div className="flex justify-between text-sm text-muted-foreground mt-2">
                  <span>15 min</span>
                  <span>{notificationSettings.notificationFrequency[0]} minutes</span>
                  <span>4 hours</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="activity" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-3">
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Recent Activity
                </CardTitle>
                <CardDescription>
                  Your recent actions and system events
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Action</TableHead>
                      <TableHead>Details</TableHead>
                      <TableHead>Timestamp</TableHead>
                      <TableHead>IP Address</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {activityHistory.map((activity) => (
                      <TableRow key={activity.id}>
                        <TableCell className="font-medium">{activity.action}</TableCell>
                        <TableCell>{activity.details}</TableCell>
                        <TableCell className="text-sm text-muted-foreground">
                          {activity.timestamp}
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground">
                          {activity.location}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>

            <div className="space-y-6">
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Activity Summary</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Documents Uploaded</span>
                      <span className="font-medium">12</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Logins This Week</span>
                      <span className="font-medium">8</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Downloads</span>
                      <span className="font-medium">24</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base">Security Events</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Password Changes</span>
                      <span className="font-medium">2</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Failed Logins</span>
                      <span className="font-medium">0</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Security Alerts</span>
                      <span className="font-medium">1</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
