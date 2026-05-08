# GmailAutomation
📧 Automated Email System with Gmail API &amp; Streamlit Dashboard - Send scheduled emails, track history, and manage campaigns with an intuitive web interface.

# 📧 Gmail Automation Dashboard

A powerful, user-friendly email automation system built with Python, Gmail API, and Streamlit. Schedule emails, send manually, track delivery history, and monitor real-time activity through an intuitive web dashboard.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)
![Gmail API](https://img.shields.io/badge/Gmail-API-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 📤 Email Management
- **Manual Sending**: Send emails instantly with custom content
- **Quick Templates**: Pre-built templates for Daily Reports, Reminders, and Weekly Summaries
- **Scheduled Emails**: Set up recurring emails at specific times
- **Batch Operations**: Manage multiple scheduled emails

### 📊 Tracking & Monitoring
- **Email History**: Complete log of all sent emails with status tracking
- **Live Logs**: Real-time activity monitoring
- **Success Metrics**: Track delivery rates and failures
- **CSV Export**: Download email history for reporting

### 🎨 User Interface
- **Beautiful Dashboard**: Modern, responsive Streamlit interface
- **Light/Dark Themes**: Toggle between themes for comfort
- **Intuitive Controls**: Easy-to-use buttons and forms
- **Mobile Friendly**: Access from any device

### 🔐 Security
- **OAuth 2.0 Authentication**: Secure Google account connection
- **Token Management**: Automatic token refresh
- **No Password Storage**: Uses Google's secure authentication

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- Gmail account with API access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gmail-automation-dashboard.git
   cd gmail-automation-dashboard

2. ### install dependencies
   pip install -r requirements.txt

3. ### setup Google cloud console
Set up Google Cloud Platform
Go to Google Cloud Console
Create a new project
Enable Gmail API
Create OAuth 2.0 credentials (Desktop app)
Download credentials.json and place it in the project root

3. ###  Add test user (for development)
Go to OAuth consent screen
Add your email as a test user
Run the application

### bash
streamlit run app.py

### Access the dashboard
Open browser to http://localhost:8501
Click "Connect Gmail" and authorize
Start sending emails!

 ### Project structure
gmail-automation/
├── app.py                  # Main Streamlit application
├── config.py               # Configuration settings
├── gmail_service.py        # Gmail API integration
├── logger.py               # Email logging utilities
├── main.py                 # Standalone scheduler (optional)
├── requirements.txt        # Python dependencies
├── credentials.json        # OAuth credentials (download from GCP)
├── token.json              # Auto-generated auth token
├── schedules.json          # Scheduled emails storage
├── live_logs.txt           # Real-time activity logs
└── logs/
    └── email_history.csv   # Email send history

### 🎯 Usage Guide
1. Connecting Gmail
2. Launch the app: streamlit run app.py
3. Click "🔐 Connect Gmail" in the sidebar
4. Authorize the application in the browser popup
5. You're connected! ✅

### sending
1. Sending Manual Emails
2. Go to "📤 Send Manual" tab
3. Fill in recipient, subject, and body
4. Or use Quick Templates:
5. 📝 Daily Report
6. 🔔 Reminder
7. 📊 Weekly Summary
8. Click "🚀 Send Email Now"

### Scheduling Emails
1. Go to "⏰ Schedule Manager" tab
2. Click "➕ Add New Scheduled Email"
3. Set time, recipient, subject, and body
4. Click "✅ Add Schedule"
5. Go to sidebar and click "▶️ Start" to activate scheduler

### Viewing History
1. Go to "📊 Email History" tab
2. Filter by status (All/Success/Error)
3. Search by recipient or subject
4. Download as CSV for reporting
   
### Monitoring Activity
Go to "📜 Live Logs" tab
Enable "🔄 Auto-refresh" for real-time updates
View scheduler activity and email sends
Clear logs when needed

### 🔐 Security Notes
1. Never commit credentials.json or token.json to version control
2. Add them to .gitignore (already included)
3. Use environment variables for sensitive data in production
4. Keep your Google Cloud project in "Testing" mode during development

### 📦 Dependencies
1. streamlit - Web interface
2. google-api-python-client - Gmail API access
3. google-auth-oauthlib - OAuth 2.0 authentication
4. google-auth-httplib2 - HTTP transport
5. schedule - Task scheduling
6. pandas - Data handling and CSV export

### 🐛 Troubleshooting
1. "Access blocked" error
2. Add your email as a test user in Google Cloud Console
3. Ensure Gmail API is enabled

### "UnicodeEncodeError"
1. Delete live_logs.txt and restart
2. Files now use UTF-8 encoding
3. Email not appearing in history
4. Check logs/email_history.csv exists
5. Verify setup_logger() is called
6. Check file permissions
7. Scheduler not running
8. Ensure Gmail is connected
9. Click "▶️ Start" in sidebar
10. Check schedules are marked as "Active"

### 🤝 Contributing
1. Contributions are welcome! Please follow these steps:
2. Fork the repository
3. Create a feature branch: git checkout -b feature/AmazingFeature
4. Commit changes: git commit -m 'Add AmazingFeature'
5. Push to branch: git push origin feature/AmazingFeature
6. Open a Pull Request

### 👨‍💻 Author
1. Kashan Abid Magasi
2. GitHub: @kashan1272
3. Email: chandkhan199014@gmail.com

### 🙏 Acknowledgments
1. Google Gmail API
2. Streamlit team for the amazing framework
3. All contributors and users

### 📬 Support
For issues and questions:
1. Open an issue on GitHub
2. Email: chandkhan199014@gmail.com
3. Made with ❤️ using Python & Streamlit
