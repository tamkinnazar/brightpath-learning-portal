# Database Authentication Backend Summary

## Role
Mohammad Qader – Backend Engineer

## Work Completed
I upgraded the BrightPath Learning Portal backend from temporary in-memory data to a working SQLite database demo.

## Features Added
- SQLite database integration
- Users table
- Courses table
- Assignments table
- Grades table
- Password hashing using Werkzeug
- Login sessions using Flask session
- Logout route
- Login-required route protection
- Role-based access control
- Administrator-only admin page
- Sample database records for courses, assignments, and grades

## Routes Updated
- /
- /register
- /login
- /logout
- /dashboard
- /courses
- /assignments
- /grades
- /admin

## Security Improvements
- Passwords are no longer stored in plain text.
- Passwords are stored as password hashes.
- Users must log in before accessing dashboard, courses, assignments, and grades.
- Admin page is restricted to users with the administrator role.

## Database
The local demo uses SQLite with a database file named:

```text
brightpath.db
```

This is suitable for local testing and demonstration. For production, the project README recommends PostgreSQL using Google Cloud SQL.
