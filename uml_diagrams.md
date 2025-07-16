# Use Case Diagram - Hostel Management System

```mermaid
graph TB
    %% Actors
    Student[👤 Student]
    Staff[👥 Hostel Staff]
    Provost[🏛️ Provost]
    Admin[⚙️ System Admin]
    Security[🔒 Security Personnel]

    %% System Boundary
    subgraph HMS["🏠 Hostel Management System"]
        %% Authentication Use Cases
        Login[Login to System]
        Logout[Logout from System]
        ChangePassword[Change Password]

        %% Student Management Use Cases
        ViewProfile[View Student Profile]
        UpdateProfile[Update Contact Info]
        RegisterStudent[Register New Student]
        ManageStudents[Manage Student Records]

        %% Room Management Use Cases
        ViewRoomStatus[View Room Status]
        ApplyForRoom[Apply for Room]
        AllocateRoom[Allocate Room]
        ApproveApplication[Approve Room Application]
        ViewAllocation[View Room Allocation]

        %% Complaint Management Use Cases
        SubmitComplaint[Submit Complaint]
        ViewComplaintStatus[View Complaint Status]
        HandleComplaint[Handle Complaint]
        UpdateComplaintStatus[Update Complaint Status]

        %% Notice Board Use Cases
        ViewNotices[View Notices]
        PostNotice[Post Notice]
        ManageNotices[Manage Notices]

        %% Stipend Management Use Cases
        ViewStipendHistory[View Stipend History]
        ProcessStipend[Process Stipend]
        GenerateStipendReport[Generate Stipend Report]

        %% Lost & Found Use Cases
        ReportLostItem[Report Lost Item]
        SearchLostItems[Search Lost Items]
        MarkItemFound[Mark Item as Found]

        %% Visitor Management Use Cases
        RegisterVisitor[Register Visitor]
        ViewVisitorLog[View Visitor Log]
        CheckInVisitor[Check-in Visitor]

        %% Reporting Use Cases
        GenerateReports[Generate Reports]
        ViewDashboard[View Dashboard]
    end

    %% Student Use Cases
    Student --> Login
    Student --> Logout
    Student --> ChangePassword
    Student --> ViewProfile
    Student --> UpdateProfile
    Student --> ViewRoomStatus
    Student --> ApplyForRoom
    Student --> ViewAllocation
    Student --> SubmitComplaint
    Student --> ViewComplaintStatus
    Student --> ViewNotices
    Student --> ViewStipendHistory
    Student --> ReportLostItem
    Student --> SearchLostItems
    Student --> RegisterVisitor

    %% Staff Use Cases
    Staff --> Login
    Staff --> Logout
    Staff --> ChangePassword
    Staff --> RegisterStudent
    Staff --> ManageStudents
    Staff --> ViewRoomStatus
    Staff --> AllocateRoom
    Staff --> HandleComplaint
    Staff --> UpdateComplaintStatus
    Staff --> PostNotice
    Staff --> ManageNotices
    Staff --> ProcessStipend
    Staff --> MarkItemFound
    Staff --> ViewVisitorLog
    Staff --> ViewDashboard

    %% Provost Use Cases
    Provost --> Login
    Provost --> Logout
    Provost --> ApproveApplication
    Provost --> ViewAllocation
    Provost --> HandleComplaint
    Provost --> GenerateReports
    Provost --> ViewDashboard

    %% Admin Use Cases
    Admin --> Login
    Admin --> Logout
    Admin --> ManageStudents
    Admin --> GenerateReports
    Admin --> ViewDashboard

    %% Security Use Cases
    Security --> Login
    Security --> Logout
    Security --> ViewVisitorLog
    Security --> CheckInVisitor

    %% Relationships
    AllocateRoom -.-> ApproveApplication : <<extends>>
    HandleComplaint -.-> UpdateComplaintStatus : <<includes>>
    PostNotice -.-> ManageNotices : <<includes>>
    ProcessStipend -.-> GenerateStipendReport : <<includes>>

    %% Styling
    classDef actor fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef usecase fill:#f3e5f5,stroke:#4a148c,stroke-width:1px
    classDef system fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px

    class Student,Staff,Provost,Admin,Security actor
    class Login,Logout,ChangePassword,ViewProfile,UpdateProfile,RegisterStudent,ManageStudents,ViewRoomStatus,ApplyForRoom,AllocateRoom,ApproveApplication,ViewAllocation,SubmitComplaint,ViewComplaintStatus,HandleComplaint,UpdateComplaintStatus,ViewNotices,PostNotice,ManageNotices,ViewStipendHistory,ProcessStipend,GenerateStipendReport,ReportLostItem,SearchLostItems,MarkItemFound,RegisterVisitor,ViewVisitorLog,CheckInVisitor,GenerateReports,ViewDashboard usecase
    class HMS system
```
