"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calendar } from "@/components/ui/calendar";
import { 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  Shield, 
  FileText, 
  Calendar as CalendarIcon,
  TrendingUp,
  TrendingDown,
  Filter,
  Download
} from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from "recharts";

const ComplianceDashboardPage = () => {
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date());

  const complianceMetrics = [
    {
      title: "Overall Compliance",
      value: "94.2%",
      change: "+2.1%",
      trend: "up",
      icon: Shield,
      color: "text-green-600"
    },
    {
      title: "Documents Reviewed",
      value: "847",
      change: "+12%",
      trend: "up", 
      icon: FileText,
      color: "text-blue-600"
    },
    {
      title: "Pending Reviews",
      value: "23",
      change: "-5%",
      trend: "down",
      icon: Clock,
      color: "text-yellow-600"
    },
    {
      title: "Critical Issues",
      value: "3",
      change: "-2",
      trend: "down",
      icon: AlertTriangle,
      color: "text-red-600"
    }
  ];

  const complianceData = [
    { month: "Jan", compliant: 89, nonCompliant: 11 },
    { month: "Feb", compliant: 92, nonCompliant: 8 },
    { month: "Mar", compliant: 88, nonCompliant: 12 },
    { month: "Apr", compliant: 94, nonCompliant: 6 },
    { month: "May", compliant: 91, nonCompliant: 9 },
    { month: "Jun", compliant: 94, nonCompliant: 6 }
  ];

  const departmentCompliance = [
    { department: "Operations", compliance: 96, total: 156 },
    { department: "Finance", compliance: 94, total: 89 },
    { department: "HR", compliance: 92, total: 67 },
    { department: "Engineering", compliance: 89, total: 134 },
    { department: "Safety", compliance: 98, total: 78 }
  ];

  const riskDistribution = [
    { name: "Low Risk", value: 65, color: "#22c55e" },
    { name: "Medium Risk", value: 28, color: "#f59e0b" },
    { name: "High Risk", value: 7, color: "#ef4444" }
  ];

  const recentAlerts = [
    {
      id: 1,
      type: "critical",
      message: "Safety compliance document overdue",
      department: "Operations",
      timestamp: "2 hours ago",
      action: "Review Required"
    },
    {
      id: 2,
      type: "warning",
      message: "Financial report pending approval",
      department: "Finance",
      timestamp: "4 hours ago",
      action: "Pending"
    },
    {
      id: 3,
      type: "info",
      message: "New compliance standard published",
      department: "All",
      timestamp: "1 day ago",
      action: "Update Required"
    }
  ];

  const getAlertColor = (type: string) => {
    switch (type) {
      case "critical": return "text-red-600";
      case "warning": return "text-yellow-600";
      case "info": return "text-blue-600";
      default: return "text-gray-600";
    }
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case "critical": return AlertTriangle;
      case "warning": return Clock;
      case "info": return CheckCircle;
      default: return AlertTriangle;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Compliance Dashboard</h1>
          <p className="text-muted-foreground">Monitor regulatory compliance and risk management</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Filter className="h-4 w-4 mr-2" />
            Filter
          </Button>
          <Button>
            <Download className="h-4 w-4 mr-2" />
            Export Report
          </Button>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {complianceMetrics.map((metric) => {
          const Icon = metric.icon;
          const TrendIcon = metric.trend === "up" ? TrendingUp : TrendingDown;
          return (
            <Card key={metric.title}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{metric.title}</CardTitle>
                <Icon className={`h-4 w-4 ${metric.color}`} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metric.value}</div>
                <p className={`text-xs flex items-center gap-1 ${
                  metric.trend === "up" ? "text-green-600" : "text-red-600"
                }`}>
                  <TrendIcon className="h-3 w-3" />
                  {metric.change} from last month
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Compliance Trends */}
          <Card>
            <CardHeader>
              <CardTitle>Compliance Trends</CardTitle>
              <CardDescription>Monthly compliance performance overview</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={complianceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Line 
                    type="monotone" 
                    dataKey="compliant" 
                    stroke="hsl(var(--primary))" 
                    strokeWidth={2}
                    name="Compliant %"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Department Performance */}
          <Card>
            <CardHeader>
              <CardTitle>Department Compliance</CardTitle>
              <CardDescription>Compliance rates by department</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {departmentCompliance.map((dept) => (
                  <div key={dept.department} className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium">{dept.department}</span>
                      <span className="text-sm text-muted-foreground">
                        {dept.compliance}% ({dept.total} documents)
                      </span>
                    </div>
                    <Progress value={dept.compliance} className="h-2" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Recent Alerts */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Alerts</CardTitle>
              <CardDescription>Latest compliance notifications and warnings</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentAlerts.map((alert) => {
                  const AlertIcon = getAlertIcon(alert.type);
                  return (
                    <div key={alert.id} className="flex items-start gap-3 p-4 rounded-lg border">
                      <AlertIcon className={`h-5 w-5 mt-0.5 ${getAlertColor(alert.type)}`} />
                      <div className="flex-1">
                        <p className="font-medium">{alert.message}</p>
                        <div className="flex items-center justify-between mt-2">
                          <p className="text-xs text-muted-foreground">{alert.timestamp}</p>
                          <Badge variant="outline">{alert.action}</Badge>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Calendar */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Compliance Calendar</CardTitle>
            </CardHeader>
            <CardContent>
              <Calendar
                mode="single"
                selected={selectedDate}
                onSelect={setSelectedDate}
                className="rounded-md border-0"
              />
            </CardContent>
          </Card>

          {/* Risk Distribution */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Risk Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={riskDistribution}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={60}
                    label={({ name, value }) => `${name}: ${value}%`}
                  >
                    {riskDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full justify-start">
                <FileText className="h-4 w-4 mr-2" />
                Generate Report
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Shield className="h-4 w-4 mr-2" />
                Review Policies
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <CalendarIcon className="h-4 w-4 mr-2" />
                Schedule Audit
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <AlertTriangle className="h-4 w-4 mr-2" />
                View Violations
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ComplianceDashboardPage;
