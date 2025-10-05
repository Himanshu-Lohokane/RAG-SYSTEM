import { redirect } from 'next/navigation'

export default function UsersPage() {
  redirect('/upload')
}
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Switch } from "@/components/ui/switch";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Search, 
  Plus, 
  Edit, 
  Trash2, 
  Download, 
  Mail, 
  Filter,
  MoreHorizontal,
  Shield,
  Users,
  UserCheck,
  UserX,
  Key,
  History
} from "lucide-react";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";

// Mock data
const departments = ["Operations", "Finance", "HR", "Legal", "Technical", "Admin"];
const roles = ["Admin", "Manager", "User", "Viewer"];

const mockUsers = [
  {
    id: 1,
    name: "Rajesh Kumar",
    email: "rajesh.kumar@kmrl.org",
    role: "Admin",
    department: "Operations",
    status: "Active",
    lastLogin: "2024-01-20 14:30",
    avatar: "/api/placeholder/32/32",
    permissions: ["read", "write", "delete", "admin"]
  },
  {
    id: 2,
    name: "Priya Nair",
    email: "priya.nair@kmrl.org",
    role: "Manager",
    department: "Finance",
    status: "Active",
    lastLogin: "2024-01-20 11:15",
    avatar: "/api/placeholder/32/32",
    permissions: ["read", "write"]
  },
  {
    id: 3,
    name: "Arun Menon",
    email: "arun.menon@kmrl.org",
    role: "User",
    department: "Technical",
    status: "Inactive",
    lastLogin: "2024-01-18 16:45",
    avatar: "/api/placeholder/32/32",
    permissions: ["read"]
  },
  {
    id: 4,
    name: "Deepika Sharma",
    email: "deepika.sharma@kmrl.org",
    role: "Manager",
    department: "HR",
    status: "Active",
    lastLogin: "2024-01-20 09:20",
    avatar: "/api/placeholder/32/32",
    permissions: ["read", "write"]
  },
  {
    id: 5,
    name: "Vikram Singh",
    email: "vikram.singh@kmrl.org",
    role: "User",
    department: "Legal",
    status: "Active",
    lastLogin: "2024-01-19 13:10",
    avatar: "/api/placeholder/32/32",
    permissions: ["read"]
  }
];

const auditLogs = [
  { id: 1, user: "Rajesh Kumar", action: "Created user account", target: "Deepika Sharma", timestamp: "2024-01-20 14:30" },
  { id: 2, user: "Priya Nair", action: "Updated role permissions", target: "Finance Team", timestamp: "2024-01-20 11:15" },
  { id: 3, user: "Arun Menon", action: "Reset password", target: "Self", timestamp: "2024-01-18 16:45" },
  { id: 4, user: "Rajesh Kumar", action: "Deactivated user", target: "John Doe", timestamp: "2024-01-18 10:30" }
];

const permissionMatrix = [
  { category: "Contracts", admin: true, manager: true, user: false, viewer: false },
  { category: "Invoices", admin: true, manager: true, user: true, viewer: true },
  { category: "Reports", admin: true, manager: true, user: true, viewer: false },
  { category: "Legal Documents", admin: true, manager: false, user: false, viewer: false },
  { category: "HR Records", admin: true, manager: true, user: false, viewer: false }
];

const departmentStats = [
  { name: "Operations", count: 12, active: 10 },
  { name: "Finance", count: 8, active: 7 },
  { name: "Technical", count: 15, active: 14 },
  { name: "HR", count: 6, active: 6 },
  { name: "Legal", count: 4, active: 3 },
  { name: "Admin", count: 3, active: 3 }
];

export default function UserManagementPage() {
  const [users, setUsers] = useState(mockUsers);
  const [selectedUsers, setSelectedUsers] = useState<number[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [roleFilter, setRoleFilter] = useState("all");
  const [departmentFilter, setDepartmentFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const [isAddUserOpen, setIsAddUserOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<any>(null);
  const { toast } = useToast();

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = roleFilter === "all" || user.role === roleFilter;
    const matchesDepartment = departmentFilter === "all" || user.department === departmentFilter;
    const matchesStatus = statusFilter === "all" || user.status === statusFilter;
    
    return matchesSearch && matchesRole && matchesDepartment && matchesStatus;
  });

  const toggleUserStatus = (userId: number) => {
    setUsers(users.map(user => 
      user.id === userId 
        ? { ...user, status: user.status === "Active" ? "Inactive" : "Active" }
        : user
    ));
    toast({
      title: "User status updated",
      description: "User status has been successfully changed."
    });
  };

  const handleSelectUser = (userId: number) => {
    setSelectedUsers(prev => 
      prev.includes(userId) 
        ? prev.filter(id => id !== userId)
        : [...prev, userId]
    );
  };

  const handleSelectAll = () => {
    if (selectedUsers.length === filteredUsers.length) {
      setSelectedUsers([]);
    } else {
      setSelectedUsers(filteredUsers.map(user => user.id));
    }
  };

  const handleBulkExport = () => {
    toast({
      title: "Export started",
      description: `Exporting ${selectedUsers.length} user records.`
    });
  };

  const handleSendInvitations = () => {
    toast({
      title: "Invitations sent",
      description: `Sent invitations to ${selectedUsers.length} users.`
    });
  };

  const UserDialog = ({ user, isOpen, onClose }: { user?: any, isOpen: boolean, onClose: () => void }) => {
    const [formData, setFormData] = useState({
      name: user?.name || "",
      email: user?.email || "",
      role: user?.role || "User",
      department: user?.department || "",
      permissions: user?.permissions || []
    });

    const handleSave = () => {
      if (user) {
        // Edit existing user
        setUsers(users.map(u => u.id === user.id ? { ...u, ...formData } : u));
        toast({ title: "User updated", description: "User information has been updated successfully." });
      } else {
        // Add new user
        const newUser = {
          id: users.length + 1,
          ...formData,
          status: "Active",
          lastLogin: "Never",
          avatar: "/api/placeholder/32/32"
        };
        setUsers([...users, newUser]);
        toast({ title: "User created", description: "New user has been created successfully." });
      }
      onClose();
    };

    return (
      <Dialog open={isOpen} onOpenChange={onClose}>
        <DialogContent className="sm:max-w-[600px]">
          <DialogHeader>
            <DialogTitle>{user ? "Edit User" : "Add New User"}</DialogTitle>
            <DialogDescription>
              {user ? "Update user information and permissions" : "Create a new user account"}
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="name">Full Name</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                />
              </div>
              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="role">Role</Label>
                <Select value={formData.role} onValueChange={(value) => setFormData({ ...formData, role: value })}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {roles.map(role => (
                      <SelectItem key={role} value={role}>{role}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="department">Department</Label>
                <Select value={formData.department} onValueChange={(value) => setFormData({ ...formData, department: value })}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {departments.map(dept => (
                      <SelectItem key={dept} value={dept}>{dept}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div>
              <Label>Permissions</Label>
              <div className="grid grid-cols-2 gap-2 mt-2">
                {["read", "write", "delete", "admin"].map(permission => (
                  <div key={permission} className="flex items-center space-x-2">
                    <Checkbox
                      id={permission}
                      checked={formData.permissions.includes(permission)}
                      onCheckedChange={(checked) => {
                        if (checked) {
                          setFormData({ ...formData, permissions: [...formData.permissions, permission] });
                        } else {
                          setFormData({ ...formData, permissions: formData.permissions.filter((p: string) => p !== permission) });
                        }
                      }}
                    />
                    <Label htmlFor={permission} className="capitalize">{permission}</Label>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={onClose}>Cancel</Button>
            <Button onClick={handleSave}>{user ? "Update" : "Create"} User</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">User Management</h1>
          <p className="text-muted-foreground">Manage user accounts, roles, and permissions</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleBulkExport} disabled={selectedUsers.length === 0}>
            <Download className="h-4 w-4 mr-2" />
            Export ({selectedUsers.length})
          </Button>
          <Button onClick={() => setIsAddUserOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Add User
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {departmentStats.map((dept) => (
          <Card key={dept.name}>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {dept.name}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dept.active}</div>
              <p className="text-xs text-muted-foreground">
                of {dept.count} total
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Tabs defaultValue="users" className="space-y-6">
        <TabsList>
          <TabsTrigger value="users">Users</TabsTrigger>
          <TabsTrigger value="roles">Roles & Permissions</TabsTrigger>
          <TabsTrigger value="audit">Audit Log</TabsTrigger>
        </TabsList>

        <TabsContent value="users" className="space-y-6">
          {/* Filters */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Filters</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <Label htmlFor="search">Search</Label>
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="search"
                      placeholder="Search users..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="role-filter">Role</Label>
                  <Select value={roleFilter} onValueChange={setRoleFilter}>
                    <SelectTrigger id="role-filter">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Roles</SelectItem>
                      {roles.map(role => (
                        <SelectItem key={role} value={role}>{role}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="dept-filter">Department</Label>
                  <Select value={departmentFilter} onValueChange={setDepartmentFilter}>
                    <SelectTrigger id="dept-filter">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Departments</SelectItem>
                      {departments.map(dept => (
                        <SelectItem key={dept} value={dept}>{dept}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="status-filter">Status</Label>
                  <Select value={statusFilter} onValueChange={setStatusFilter}>
                    <SelectTrigger id="status-filter">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Status</SelectItem>
                      <SelectItem value="Active">Active</SelectItem>
                      <SelectItem value="Inactive">Inactive</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Users Table */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Users ({filteredUsers.length})
                </CardTitle>
                <div className="flex gap-2">
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={handleSendInvitations}
                    disabled={selectedUsers.length === 0}
                  >
                    <Mail className="h-4 w-4 mr-2" />
                    Send Invites ({selectedUsers.length})
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-12">
                      <Checkbox
                        checked={selectedUsers.length === filteredUsers.length && filteredUsers.length > 0}
                        onCheckedChange={handleSelectAll}
                      />
                    </TableHead>
                    <TableHead>User</TableHead>
                    <TableHead>Role</TableHead>
                    <TableHead>Department</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Last Login</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredUsers.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell>
                        <Checkbox
                          checked={selectedUsers.includes(user.id)}
                          onCheckedChange={() => handleSelectUser(user.id)}
                        />
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <Avatar className="h-8 w-8">
                            <AvatarImage src={user.avatar} alt={user.name} />
                            <AvatarFallback>{user.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                          </Avatar>
                          <div>
                            <div className="font-medium">{user.name}</div>
                            <div className="text-sm text-muted-foreground">{user.email}</div>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={user.role === 'Admin' ? 'default' : 'secondary'}>
                          {user.role}
                        </Badge>
                      </TableCell>
                      <TableCell>{user.department}</TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Switch
                            checked={user.status === "Active"}
                            onCheckedChange={() => toggleUserStatus(user.id)}
                          />
                          <Badge variant={user.status === 'Active' ? 'default' : 'secondary'}>
                            {user.status}
                          </Badge>
                        </div>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {user.lastLogin}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex items-center gap-2 justify-end">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setEditingUser(user)}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                          <AlertDialog>
                            <AlertDialogTrigger asChild>
                              <Button variant="outline" size="sm">
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </AlertDialogTrigger>
                            <AlertDialogContent>
                              <AlertDialogHeader>
                                <AlertDialogTitle>Delete User</AlertDialogTitle>
                                <AlertDialogDescription>
                                  Are you sure you want to delete {user.name}? This action cannot be undone.
                                </AlertDialogDescription>
                              </AlertDialogHeader>
                              <AlertDialogFooter>
                                <AlertDialogCancel>Cancel</AlertDialogCancel>
                                <AlertDialogAction>Delete</AlertDialogAction>
                              </AlertDialogFooter>
                            </AlertDialogContent>
                          </AlertDialog>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="roles" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                Permission Matrix
              </CardTitle>
              <CardDescription>
                Document access permissions by role
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Document Type</TableHead>
                    <TableHead>Admin</TableHead>
                    <TableHead>Manager</TableHead>
                    <TableHead>User</TableHead>
                    <TableHead>Viewer</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {permissionMatrix.map((permission) => (
                    <TableRow key={permission.category}>
                      <TableCell className="font-medium">{permission.category}</TableCell>
                      <TableCell>
                        {permission.admin ? (
                          <UserCheck className="h-4 w-4 text-green-600" />
                        ) : (
                          <UserX className="h-4 w-4 text-red-600" />
                        )}
                      </TableCell>
                      <TableCell>
                        {permission.manager ? (
                          <UserCheck className="h-4 w-4 text-green-600" />
                        ) : (
                          <UserX className="h-4 w-4 text-red-600" />
                        )}
                      </TableCell>
                      <TableCell>
                        {permission.user ? (
                          <UserCheck className="h-4 w-4 text-green-600" />
                        ) : (
                          <UserX className="h-4 w-4 text-red-600" />
                        )}
                      </TableCell>
                      <TableCell>
                        {permission.viewer ? (
                          <UserCheck className="h-4 w-4 text-green-600" />
                        ) : (
                          <UserX className="h-4 w-4 text-red-600" />
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="audit" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <History className="h-5 w-5" />
                Audit Log
              </CardTitle>
              <CardDescription>
                User actions and system changes
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>User</TableHead>
                    <TableHead>Action</TableHead>
                    <TableHead>Target</TableHead>
                    <TableHead>Timestamp</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {auditLogs.map((log) => (
                    <TableRow key={log.id}>
                      <TableCell className="font-medium">{log.user}</TableCell>
                      <TableCell>{log.action}</TableCell>
                      <TableCell>{log.target}</TableCell>
                      <TableCell className="text-sm text-muted-foreground">{log.timestamp}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* User Dialog */}
      <UserDialog
        user={editingUser}
        isOpen={!!editingUser || isAddUserOpen}
        onClose={() => {
          setEditingUser(null);
          setIsAddUserOpen(false);
        }}
      />
    </div>
  );
}
