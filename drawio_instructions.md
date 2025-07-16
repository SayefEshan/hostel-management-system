# Draw.io Visual Diagram Creation Guide
## Hostel Management System UML Diagrams

### 🚀 Getting Started with Draw.io

1. **Go to**: https://app.diagrams.net/
2. **Choose**: "Create New Diagram"
3. **Select**: "Blank Diagram" or choose a UML template
4. **Name your file**: e.g., "HMS-Use-Case-Diagram"

---

## 📋 Diagram 1: Use Case Diagram

### **Step 1: Set up the Canvas**
- **File → New → Blank Diagram**
- **Name**: "HMS-Use-Case-Diagram"
- **Set page size**: A4 Landscape

### **Step 2: Add Actor Shapes**
**Left Sidebar → Search "UML" → UML Shapes**

**Actors to Create (Left side of canvas):**
1. **Student** 
   - Drag "Actor" shape
   - Double-click to rename: "Student"
   - Position: Top-left

2. **Hostel Staff**
   - Drag another "Actor" shape
   - Rename: "Hostel Staff"
   - Position: Below Student

3. **Provost**
   - Actor shape
   - Rename: "Provost"
   - Position: Below Staff

4. **System Admin**
   - Actor shape
   - Rename: "System Admin"
   - Position: Below Provost

5. **Security Personnel**
   - Actor shape
   - Rename: "Security Personnel"
   - Position: Bottom-left

### **Step 3: Create System Boundary**
1. **Drag a Rectangle** from Basic Shapes
2. **Make it large** to contain all use cases
3. **Right-click → Format**
4. **Set**: 
   - Fill: Light blue (#E3F2FD)
   - Border: Solid, dark blue
   - Add label: "Hostel Management System"

### **Step 4: Add Use Cases (Inside the Rectangle)**

**Search "UML" → Use Case shapes (oval)**

**Authentication Use Cases:**
- Login to System
- Logout from System
- Change Password

**Student Management:**
- View Student Profile
- Update Contact Info
- Register New Student
- Manage Student Records

**Room Management:**
- View Room Status
- Apply for Room
- Allocate Room
- Approve Room Application
- View Room Allocation

**Complaint Management:**
- Submit Complaint
- View Complaint Status
- Handle Complaint
- Update Complaint Status

**Notice Board:**
- View Notices
- Post Notice
- Manage Notices

**Additional Features:**
- View Stipend History
- Process Stipend
- Report Lost Item
- Search Lost Items
- Register Visitor
- View Visitor Log
- Check-in Visitor
- Generate Reports
- View Dashboard

### **Step 5: Add Connections**
**Use "Connector" tool from toolbar**

**Student Connections:**
- Student → Login to System
- Student → View Student Profile
- Student → Apply for Room
- Student → Submit Complaint
- Student → View Notices
- Student → View Stipend History
- Student → Report Lost Item
- Student → Register Visitor

**Staff Connections:**
- Hostel Staff → Login to System
- Hostel Staff → Register New Student
- Hostel Staff → Manage Student Records
- Hostel Staff → Allocate Room
- Hostel Staff → Handle Complaint
- Hostel Staff → Post Notice
- Hostel Staff → Process Stipend

**And so on for other actors...**

### **Step 6: Add Relationship Types**
**For extends/includes relationships:**
1. **Use dashed arrows**
2. **Add labels**: "<<extends>>" or "<<includes>>"
3. **Example**: Allocate Room --extends--> Approve Application

---

## 🔄 Diagram 2: Activity Diagram - Room Application Process

### **Step 1: Setup**
- **New Diagram**: "Room-Application-Activity"
- **Choose**: UML Activity template or blank

### **Step 2: Add Activity Elements**

**From UML Shapes:**

**Start/End Nodes:**
1. **Initial Node** (solid black circle)
   - Label: "Start"

2. **Final Node** (circle with solid center)
   - Label: "End"

**Activity Boxes:**
3. **Activity rectangles** with rounded corners:
   - "Student Login"
   - "View Available Rooms"
   - "Select Room"
   - "Fill Application Form"
   - "Submit Application"
   - "Staff Reviews Application"
   - "Forward to Provost"
   - "Provost Reviews"
   - "Room Allocated"
   - "Update Room Status"
   - "Notify Student"

**Decision Nodes:**
4. **Diamond shapes** for decisions:
   - "Room Available?"
   - "Staff Decision"
   - "Provost Decision"

### **Step 3: Arrange Flow**
**Top to Bottom Layout:**
1. **Start** at top
2. **Sequential activities** flowing down
3. **Decision diamonds** with Yes/No branches
4. **Parallel paths** for different outcomes
5. **End** at bottom

### **Step 4: Add Flow Arrows**
1. **Use arrows** to connect elements
2. **Label decision paths**: "Yes", "No", "Approve", "Reject"
3. **Add swimlanes** if needed (Student, Staff, Provost columns)

### **Step 5: Color Coding**
- **Start/End**: Green
- **Activities**: Light blue
- **Decisions**: Orange
- **Notifications**: Pink

---

## 🏗️ Diagram 3: Class Diagram - User Management

### **Step 1: Setup**
- **New Diagram**: "User-Management-Classes"
- **Template**: UML Class Diagram

### **Step 2: Create Class Boxes**

**From UML Shapes → Class:**

**User Class:**
1. **Drag Class shape**
2. **Three sections**:
   - **Top**: Class name "User"
   - **Middle**: Attributes
   - **Bottom**: Methods

**Format the User Class:**
```
User
─────────────────
+id: int
+username: string
+email: string
+password: string
+first_name: string
+last_name: string
+is_active: boolean
+date_joined: datetime
─────────────────
+login(): void
+logout(): void
+change_password(): void
+update_profile(): void
```

**CustomUser Class:**
```
CustomUser
─────────────────
+user_type: string
+phone: string
+emergency_contact: string
+profile_picture: string
─────────────────
+get_user_type(): string
+is_student(): boolean
+is_staff(): boolean
```

**StudentProfile Class:**
```
StudentProfile
─────────────────
+student_id: string
+department: string
+academic_year: int
+semester: int
+faculty: string
+enrollment_date: datetime
─────────────────
+get_academic_info(): dict
+get_room_status(): dict
```

**StaffProfile Class:**
```
StaffProfile
─────────────────
+employee_id: string
+designation: string
+department: string
+joining_date: datetime
─────────────────
+get_assigned_complaints(): list
+get_managed_rooms(): list
```

### **Step 3: Add Relationships**

**Inheritance (User → CustomUser):**
1. **Use inheritance arrow** (hollow triangle)
2. **Connect**: User to CustomUser

**One-to-One (CustomUser → StudentProfile):**
1. **Use association line**
2. **Add multiplicity**: "1" on both ends
3. **Add role labels** if needed

**One-to-One (CustomUser → StaffProfile):**
- Same as above

### **Step 4: Position Classes**
- **User**: Top center
- **CustomUser**: Below User
- **StudentProfile**: Bottom left
- **StaffProfile**: Bottom right

---

## 🏠 Diagram 4: Class Diagram - Room Management

### **Classes to Create:**

**Room Class:**
```
Room
─────────────────
+room_number: string
+capacity: int
+current_occupancy: int
+room_type: string
+facilities: json
+block: string
+floor: int
+is_available: boolean
─────────────────
+get_available_beds(): int
+get_occupants(): list
+allocate_bed(): void
+deallocate_bed(): void
```

**RoomApplication Class:**
```
RoomApplication
─────────────────
+application_id: int
+application_date: datetime
+status: string
+priority_score: int
+preferences: string
+justification: string
─────────────────
+submit_application(): void
+approve_application(): void
+reject_application(): void
```

**RoomAllocation Class:**
```
RoomAllocation
─────────────────
+allocation_date: datetime
+move_in_date: datetime
+move_out_date: datetime
+is_current: boolean
+bed_number: string
─────────────────
+allocate_room(): void
+deallocate_room(): void
+transfer_room(): void
```

### **Relationships:**
- **StudentProfile** (1) → (many) **RoomApplication**
- **Room** (1) → (many) **RoomApplication**
- **StudentProfile** (1) → (many) **RoomAllocation**
- **Room** (1) → (many) **RoomAllocation**
- **RoomApplication** (1) → (1) **RoomAllocation**

---

## 🎨 Formatting Tips for Professional Look

### **Color Scheme:**
- **Actors**: Light green (#C8E6C9)
- **Use Cases**: Light blue (#E3F2FD)
- **Classes**: Light yellow (#FFF9C4)
- **Activities**: Light purple (#F3E5F5)
- **Decisions**: Light orange (#FFE0B2)

### **Font Settings:**
- **Class names**: Bold, 12pt
- **Attributes/Methods**: Regular, 10pt
- **Labels**: Regular, 9pt

### **Layout Tips:**
1. **Align elements** using Draw.io's alignment tools
2. **Use consistent spacing** between elements
3. **Group related elements** together
4. **Use layers** for complex diagrams
5. **Add background colors** to group related sections

### **Professional Touches:**
1. **Add title** at top of each diagram
2. **Include legend** for symbols and colors
3. **Add creation date** and version number
4. **Use consistent naming conventions**
5. **Export as high-quality PNG** (300 DPI)

---

## 📤 Export and Usage

### **Export Options:**
1. **File → Export as → PNG**
   - **Resolution**: 300 DPI for printing
   - **Transparent background**: For presentations

2. **File → Export as → PDF**
   - **Best for**: Documentation
   - **Vector format**: Scalable

3. **File → Export as → SVG**
   - **Best for**: Web documentation
   - **Smallest file size**

### **Integration with Documentation:**
1. **Save images** in `docs/images/` folder
2. **Reference in SRS**: `![Use Case Diagram](images/use-case-diagram.png)`
3. **Include in presentations**
4. **Print for physical submission**

---

## 🎯 Quick Start Checklist

For your sister's project, create these diagrams in order:

### **Priority 1 (Essential):**
- [ ] Use Case Diagram
- [ ] Activity Diagram: Room Application Process
- [ ] Class Diagram: User Management
- [ ] Class Diagram: Room Management

### **Priority 2 (Important):**
- [ ] Activity Diagram: Complaint Management
- [ ] Class Diagram: Complaint System
- [ ] Class Diagram: Notice Board

### **Priority 3 (Nice to have):**
- [ ] Activity Diagram: Visitor Registration
- [ ] Class Diagram: Complete System
- [ ] Sequence Diagrams (if needed)

Each diagram should take 30-60 minutes to create in Draw.io with these instructions!
