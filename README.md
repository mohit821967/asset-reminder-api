# 🛠️ Asset Reminder API

A RESTful API to manage assets with service and expiration reminders. Built with Flask + SQLite.

---

## ✅ Features

- Create and track assets
- Schedule service and expiration reminders
- Automatic notification system (within 15 minutes)
- Auto-logged violations for overdue service or expired assets
- SQLite database
- RESTful endpoints
- Unit tests included

---

## 🚀 API Endpoints

| Method | Endpoint            | Description                       |
|--------|---------------------|-----------------------------------|
| POST   | /assets             | Create a new asset                |
| GET    | /assets             | List all assets                   |
| PUT    | /assets/<id>        | Mark asset as serviced            |
| GET    | /run-checks         | Run reminder & violation checks   |
| GET    | /notifications      | List all notifications            |
| GET    | /violations         | List all violations               |

---

## 📦 Setup Instructions

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/mohit821967/asset-reminder-api.git
cd asset-reminder-api
