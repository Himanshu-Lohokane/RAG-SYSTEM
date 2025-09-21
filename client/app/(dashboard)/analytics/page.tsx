"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { 
  BarChart, 
  Bar, 
  LineChart, 
  Line, 
  PieChart, 
  Pie, 
  Cell, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from "recharts";
import { 
  Download, 
  Clock, 
  Target, 
  TrendingUp, 
  Users, 
  Calendar,
  AlertTriangle,
  CheckCircle,
  Activity
} from "lucide-react";
import { useState } from "react";

const kpiData = [
  {
    title: "Avg Processing Time",
    value: "38s",
    change: "-12%",
    icon: Clock,
    trend: "down"
  },
  {
    title: "Accuracy Rate",
    value: "96.5%",
    change: "+2.1%",
    icon: Target,
    trend: "up"
  },
  {
    title: "Cost Savings",
    value: "₹4.2L",
    change: "+18%",
    icon: TrendingUp,
    trend: "up"
  },
  {
    title: "Documents/Hour",
    value: "847",
    change: "+5.3%",
    icon: Activity,
    trend: "up"
  }
];

const documentData = [
  { month: "Jan", processed: 12400, accuracy: 94.2 },
  { month: "Feb", processed: 13890, accuracy: 95.1 },
  { month: "Mar", processed: 15200, accuracy: 96.8 },
  { month: "Apr", processed: 14100, accuracy: 95.9 },
  { month: "May", processed: 16800, accuracy: 96.5 },
  { month: "Jun", processed: 18200, accuracy: 97.2 }
];

const departmentData = [
  { name: "Operations", documents: 4500, accuracy: 97.2, efficiency: 89 },
  { name: "Finance", documents: 3200, accuracy: 96.8, efficiency: 92 },
  { name: "HR", documents: 2100, accuracy: 95.4, efficiency: 87 },
  { name: "Legal", documents: 1800, accuracy: 98.1, efficiency: 94 },
  { name: "Technical", documents: 2900, accuracy: 96.3, efficiency: 91 }
];

const categoryData = [
  { name: "Contracts", value: 35, color: "hsl(var(--primary))" },
  { name: "Invoices", value: 28, color: "hsl(var(--chart-2))" },
  { name: "Reports", value: 22, color: "hsl(var(--chart-3))" },
  { name: "Legal", value: 15, color: "hsl(var(--chart-4))" }
];

const heatmapData = [
  { hour: "00", Mon: 12, Tue: 8, Wed: 15, Thu: 10, Fri: 20, Sat: 5, Sun: 3 },
  { hour: "04", Mon: 5, Tue: 3, Wed: 8, Thu: 6, Fri: 12, Sat: 2, Sun: 1 },
  { hour: "08", Mon: 89, Tue: 92, Wed: 88, Thu: 94, Fri: 87, Sat: 15, Sun: 8 },
  { hour: "12", Mon: 156, Tue: 142, Wed: 159, Thu: 148, Fri: 145, Sat: 32, Sun: 18 },
  { hour: "16", Mon: 134, Tue: 128, Wed: 139, Thu: 131, Fri: 142, Sat: 28, Sun: 22 },
  { hour: "20", Mon: 45, Tue: 38, Wed: 42, Thu: 39, Fri: 48, Sat: 25, Sun: 15 }
];

const predictionData = [
  { month: "Jul", predicted: 19500, maintenance: "Low", confidence: 92 },
  { month: "Aug", predicted: 20800, maintenance: "Medium", confidence: 89 },
  { month: "Sep", predicted: 18900, maintenance: "Low", confidence: 94 },
  { month: "Oct", predicted: 22100, maintenance: "High", confidence: 87 },
  { month: "Nov", predicted: 21500, maintenance: "Medium", confidence: 91 },
  { month: "Dec", predicted: 23200, maintenance: "Low", confidence: 93 }
];

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState("30-days");

  const exportData = (format: string) => {
    // Export functionality would be implemented here
    console.log(`Exporting data in ${format} format`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Analytics Dashboard</h1>
          <p className="text-muted-foreground">Comprehensive insights into document processing performance</p>
        </div>
        <div className="flex gap-2">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7-days">Last 7 days</SelectItem>
              <SelectItem value="30-days">Last 30 days</SelectItem>
              <SelectItem value="3-months">Last 3 months</SelectItem>
              <SelectItem value="1-year">Last 1 year</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" onClick={() => exportData("pdf")}>
            <Download className="h-4 w-4 mr-2" />
            Export PDF
          </Button>
          <Button variant="outline" onClick={() => exportData("excel")}>
            <Download className="h-4 w-4 mr-2" />
            Export Excel
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpiData.map((kpi, index) => (
          <Card key={index} className="relative overflow-hidden">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {kpi.title}
              </CardTitle>
              <kpi.icon className="h-5 w-5 text-primary" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-foreground">{kpi.value}</div>
              <p className={`text-xs flex items-center gap-1 ${
                kpi.trend === "up" ? "text-green-600" : "text-red-600"
              }`}>
                {kpi.change} from last period
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Tabs */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="departments">Departments</TabsTrigger>
          <TabsTrigger value="users">Users</TabsTrigger>
          <TabsTrigger value="predictions">Predictions</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Document Processing Trend */}
            <Card>
              <CardHeader>
                <CardTitle>Document Processing Trend</CardTitle>
                <CardDescription>Monthly document processing volume</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={documentData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Area 
                      type="monotone" 
                      dataKey="processed" 
                      stroke="hsl(var(--primary))" 
                      fill="hsl(var(--primary) / 0.2)" 
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Document Categories */}
            <Card>
              <CardHeader>
                <CardTitle>Document Categories</CardTitle>
                <CardDescription>Distribution by document type</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={categoryData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={120}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {categoryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="performance" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Processing Accuracy Over Time</CardTitle>
              <CardDescription>Monthly accuracy rate trends</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={documentData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis domain={[90, 100]} />
                  <Tooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="accuracy" 
                    stroke="hsl(var(--primary))" 
                    strokeWidth={3}
                    dot={{ fill: "hsl(var(--primary))", strokeWidth: 2, r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="departments" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Department Performance Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Department Performance</CardTitle>
                <CardDescription>Processing volume by department</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={departmentData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="documents" fill="hsl(var(--primary))" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Department Details Table */}
            <Card>
              <CardHeader>
                <CardTitle>Department Details</CardTitle>
                <CardDescription>Detailed performance metrics</CardDescription>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Department</TableHead>
                      <TableHead>Accuracy</TableHead>
                      <TableHead>Efficiency</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {departmentData.map((dept) => (
                      <TableRow key={dept.name}>
                        <TableCell className="font-medium">{dept.name}</TableCell>
                        <TableCell>
                          <Badge variant={dept.accuracy > 96 ? "default" : "secondary"}>
                            {dept.accuracy}%
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Badge variant={dept.efficiency > 90 ? "default" : "secondary"}>
                            {dept.efficiency}%
                          </Badge>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="users" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>User Activity Heatmap</CardTitle>
              <CardDescription>Peak processing hours throughout the week</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {heatmapData.map((row) => (
                  <div key={row.hour} className="flex items-center gap-2">
                    <span className="w-8 text-sm text-muted-foreground">{row.hour}:00</span>
                    <div className="flex gap-1">
                      {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day) => {
                        const value = row[day as keyof typeof row] as number;
                        const intensity = Math.min(value / 100, 1);
                        return (
                          <div
                            key={day}
                            className="w-8 h-6 rounded text-xs flex items-center justify-center text-white"
                            style={{
                              backgroundColor: `hsl(var(--primary) / ${intensity * 0.8 + 0.2})`
                            }}
                            title={`${day}: ${value} documents`}
                          >
                            {value > 50 ? value : ''}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
                <div className="flex items-center gap-2 text-sm text-muted-foreground mt-4">
                  <span>Low</span>
                  <div className="flex gap-1">
                    {[0.2, 0.4, 0.6, 0.8, 1.0].map((opacity) => (
                      <div
                        key={opacity}
                        className="w-4 h-4 rounded"
                        style={{ backgroundColor: `hsl(var(--primary) / ${opacity})` }}
                      />
                    ))}
                  </div>
                  <span>High</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="predictions" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Prediction Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Volume Predictions</CardTitle>
                <CardDescription>Forecasted document processing volume</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={predictionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Area 
                      type="monotone" 
                      dataKey="predicted" 
                      stroke="hsl(var(--chart-2))" 
                      fill="hsl(var(--chart-2) / 0.2)" 
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Maintenance Forecast */}
            <Card>
              <CardHeader>
                <CardTitle>Maintenance Forecast</CardTitle>
                <CardDescription>Predicted system maintenance needs</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {predictionData.map((prediction) => (
                    <div key={prediction.month} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center gap-3">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        <span className="font-medium">{prediction.month}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge 
                          variant={
                            prediction.maintenance === "Low" ? "default" :
                            prediction.maintenance === "Medium" ? "secondary" : "destructive"
                          }
                        >
                          {prediction.maintenance} Risk
                        </Badge>
                        <span className="text-sm text-muted-foreground">
                          {prediction.confidence}% confidence
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
