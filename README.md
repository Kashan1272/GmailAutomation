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

2. ##install dependencies
   pip install -r requirements.txt

3.#setup Google cloud console
Set up Google Cloud Platform
Go to Google Cloud Console
Create a new project
Enable Gmail API
Create OAuth 2.0 credentials (Desktop app)
Download credentials.json and place it in the project root

3. Add test user (for development)
Go to OAuth consent screen
Add your email as a test user
Run the application
bash

*##*Project structure
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

🎯 Usage Guide
Connecting Gmail
Launch the app: streamlit run app.py
Click "🔐 Connect Gmail" in the sidebar
Authorize the application in the browser popup
You're connected! ✅
Sending Manual Emails
Go to "📤 Send Manual" tab
Fill in recipient, subject, and body
Or use Quick Templates:
📝 Daily Report
🔔 Reminder
📊 Weekly Summary
Click "🚀 Send Email Now"
Scheduling Emails
Go to "⏰ Schedule Manager" tab
Click "➕ Add New Scheduled Email"
Set time, recipient, subject, and body
Click "✅ Add Schedule"
Go to sidebar and click "▶️ Start" to activate scheduler
Viewing History
Go to "📊 Email History" tab
Filter by status (All/Success/Error)
Search by recipient or subject
Download as CSV for reporting
Monitoring Activity
Go to "📜 Live Logs" tab
Enable "🔄 Auto-refresh" for real-time updates
View scheduler activity and email sends
Clear logs when needed

🔐 Security Notes
Never commit credentials.json or token.json to version control
Add them to .gitignore (already included)
Use environment variables for sensitive data in production
Keep your Google Cloud project in "Testing" mode during development
📦 Dependencies
streamlit - Web interface
google-api-python-client - Gmail API access
google-auth-oauthlib - OAuth 2.0 authentication
google-auth-httplib2 - HTTP transport
schedule - Task scheduling
pandas - Data handling and CSV export
🐛 Troubleshooting
"Access blocked" error
Add your email as a test user in Google Cloud Console
Ensure Gmail API is enabled
"UnicodeEncodeError"
Delete live_logs.txt and restart
Files now use UTF-8 encoding
Email not appearing in history
Check logs/email_history.csv exists
Verify setup_logger() is called
Check file permissions
Scheduler not running
Ensure Gmail is connected
Click "▶️ Start" in sidebar
Check schedules are marked as "Active"
🤝 Contributing
Contributions are welcome! Please follow these steps:
Fork the repository
Create a feature branch: git checkout -b feature/AmazingFeature
Commit changes: git commit -m 'Add AmazingFeature'
Push to branch: git push origin feature/AmazingFeature
Open a Pull Request
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
👨‍💻 Author
Your Name
GitHub: @kashan1272
Email: chandkhan199014@gmail.com
🙏 Acknowledgments
Google Gmail API
Streamlit team for the amazing framework
All contributors and users
📬 Support
For issues and questions:
Open an issue on GitHub
Email: chandkhan199014@gmail.com
Made with ❤️ using Python & Streamlit
