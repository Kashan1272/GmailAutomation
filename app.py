import streamlit as st
import sys
import os
import pandas as pd
import threading
import time
from datetime import datetime
import schedule
import json
from pathlib import Path

# Ensure project modules are importable
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import configuration and modules
from config import LOG_PATH, RECIPIENT, SUBJECT, BODY, SCHEDULE_TIMES
from gmail_service import get_gmail_service, send_email
from logger import setup_logger, log_email
# Debug: Show current working directory
import os
print(f"📁 Current Working Directory: {os.getcwd()}")
print(f"📁 LOG_PATH: {LOG_PATH}")
print(f"📁 Absolute LOG_PATH: {os.path.abspath(LOG_PATH)}")

# Debug section - remove after testing
with st.expander("🔧 Debug Info", expanded=False):
    st.write(f"**LOG_PATH:** `{LOG_PATH}`")
    st.write(f"**File exists:** `{os.path.exists(LOG_PATH)}`")
    if os.path.exists(LOG_PATH):
        st.write(f"**File size:** `{os.path.getsize(LOG_PATH)} bytes`")
        try:
            with open(LOG_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                st.write(f"**Lines in file:** `{len(lines)}`")
                if lines:
                    st.write("**Last 3 lines:**")
                    st.code("".join(lines[-3:]))
        except Exception as e:
            st.error(f"Error reading file: {e}")


# Page config
st.set_page_config(
    page_title="📧 Email Automation Dashboard",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Custom CSS - Teal & Terracotta Theme (No Black/Blue)
def inject_css():
    st.markdown("""
    <style>
    /* Light Theme Base */
    [data-testid="stAppViewContainer"] { 
        background: linear-gradient(135deg, #F4F6F8 0%, baidge 100%); 
    }
    [data-testid="stHeader"] { 
        background-color: transparent; 
    }
    
    /* Cards & Containers */
    .css-1r6slb0 { 
        background-color: #FFFFFF; 
        border-radius: 10px; 
        padding: 20px; 
        box-shadow: 0 2px 8px rgba(26, 188, 156, 0.1);
    }
    
    /* Buttons */
    .stButton button { 
        background: linear-gradient(135deg, #1ABC9C 0%, #16A085 100%) !important; 
        color: white !important; 
        font-weight: 600; 
        border: none; 
        border-radius: 8px;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(26, 188, 156, 0.4);
    }
    
    /* Inputs */
    .stTextInput input, .stTextArea textarea { 
        background-color: #FFFFFF !important; 
        color: #2C3E50 !important; 
        border: 2px solid #E0E6E8 !important;
        border-radius: 8px;
    }
    .stTextInput input:focus, .stTextArea textarea:focus { 
        border-color: #1ABC9C !important;
    }
    
    /* DataFrames */
    .stDataFrame { 
        background-color: #FFFFFF !important; 
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] { 
        color: #1ABC9C !important; 
    }
    
    /* Success/Error Boxes */
    .stAlert { 
        border-radius: 8px; 
        border: none;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #FFFFFF 0%, #baidge 100%); 
    }
    
    /* Headers */
    h1, h2, h3 { 
        color: #2C3E50 !important; 
        font-weight: 700;
    }
    
    /* Custom status badges */
    .status-running { 
        background-color: #1ABC9C; 
        color: white; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-size: 12px; 
        font-weight: 600;
        display: inline-block;
    }
    .status-stopped { 
        background-color: #E67E22; 
        color: white; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-size: 12px; 
        font-weight: 600;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# 📁 File paths
SCHEDULES_FILE = "schedules.json"
LIVE_LOG_FILE = "live_logs.txt"

# 🔧 Scheduler Manager Class
class EmailScheduler:
    def __init__(self):
        self.service = None
        self.is_running = False
        self.thread = None
        self.schedules = self.load_schedules()
        
    def load_schedules(self):
        """Load scheduled emails from JSON file"""
        if os.path.exists(SCHEDULES_FILE):
            with open(SCHEDULES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_schedules(self):
        """Save schedules to JSON file"""
        with open(SCHEDULES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.schedules, f, indent=2, ensure_ascii=False)
    
    def connect_gmail(self):
        """Authenticate with Gmail"""
        try:
            self.service = get_gmail_service()
            return True, "Connected successfully"
        except Exception as e:
            return False, str(e)
    
    def add_schedule(self, time_str, recipient, subject, body):
        """Add a new scheduled email"""
        schedule_id = f"schedule_{len(self.schedules) + 1}_{int(time.time())}"
        self.schedules.append({
            "id": schedule_id,
            "time": time_str,
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "active": True,
            "created_at": datetime.now().isoformat()
        })
        self.save_schedules()
        return schedule_id
    
    def remove_schedule(self, schedule_id):
        """Remove a scheduled email"""
        self.schedules = [s for s in self.schedules if s["id"] != schedule_id]
        self.save_schedules()
    
    def send_scheduled_email(self, schedule_item):
        """Send email for a schedule item"""
        if not self.service:
            self.log_message("❌ No Gmail connection available")
            return
        
        result = send_email(
            self.service,
            "me",
            schedule_item["recipient"],
            schedule_item["subject"],
            schedule_item["body"]
        )
        
        log_email(
            schedule_item["recipient"],
            schedule_item["subject"],
            result["status"],
            result.get("message_id") or result.get("error")
        )
        
        status_icon = "✅" if result["status"] == "success" else "❌"
        msg = f"{status_icon} [{datetime.now().strftime('%H:%M:%S')}] Sent to {schedule_item['recipient']}: {schedule_item['subject']}"
        self.log_message(msg)
    
    def log_message(self, message):
        """Write to live log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(LIVE_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def scheduler_job(self):
        """Background scheduler thread"""
        self.log_message("🚀 Scheduler started")
        
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.log_message(f"❌ Scheduler error: {str(e)}")
                time.sleep(5)
    
    def start_scheduler(self):
        """Start the scheduler in background thread"""
        if self.is_running:
            return False, "Scheduler already running"
        
        if not self.service:
            return False, "Please connect to Gmail first"
        
        # Clear existing jobs
        schedule.clear()
        
        # Register all active schedules
        for sched in self.schedules:
            if sched["active"]:
                schedule.every().day.at(sched["time"]).do(
                    self.send_scheduled_email,
                    schedule_item=sched
                )
                self.log_message(f"⏰ Scheduled: {sched['time']} → {sched['recipient']}")
        
        self.is_running = True
        self.thread = threading.Thread(target=self.scheduler_job, daemon=True)
        self.thread.start()
        
        return True, "Scheduler started successfully"
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.is_running = False
        schedule.clear()
        self.log_message("🛑 Scheduler stopped")
        return True, "Scheduler stopped"
    
    def get_status(self):
        """Get scheduler status"""
        return {
            "running": self.is_running,
            "service_connected": self.service is not None,
            "total_schedules": len(self.schedules),
            "active_schedules": len([s for s in self.schedules if s["active"]])
        }

# Initialize scheduler in session state
if "scheduler" not in st.session_state:
    st.session_state.scheduler = EmailScheduler()

scheduler = st.session_state.scheduler

# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("🎛️ Control Panel")
    
    # Connection Status
    st.subheader("🔗 Gmail Connection")
    status = scheduler.get_status()
    
    if status["service_connected"]:
        st.success("✅ Connected")
        if st.button("🔌 Disconnect", use_container_width=True):
            scheduler.service = None
            st.rerun()
    else:
        st.warning("⚠️ Not Connected")
        if st.button("🔐 Connect Gmail", use_container_width=True, type="primary"):
            success, msg = scheduler.connect_gmail()
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    
    st.divider()
    
    # Scheduler Controls
    st.subheader("⏰ Scheduler")
    
    col1, col2 = st.columns(2)
    with col1:
        if not status["running"]:
            if st.button("▶️ Start", use_container_width=True, type="primary"):
                success, msg = scheduler.start_scheduler()
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    
    with col2:
        if status["running"]:
            if st.button("⏹️ Stop", use_container_width=True):
                success, msg = scheduler.stop_scheduler()
                st.warning(msg)
                st.rerun()
    
    # Status Badge
    if status["running"]:
        st.markdown('<span class="status-running">● RUNNING</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-stopped">● STOPPED</span>', unsafe_allow_html=True)
    
    st.divider()
    
    # Stats
    st.subheader("📊 Statistics")
    st.metric("Total Schedules", status["total_schedules"])
    st.metric("Active Schedules", status["active_schedules"])
    
    # Quick Actions
    st.divider()
    st.subheader("⚡ Quick Actions")
    if st.button("🗑️ Clear All Logs", use_container_width=True):
        if os.path.exists(LOG_PATH):
            os.remove(LOG_PATH)
            st.success("Logs cleared!")
            st.rerun()

# ==================== MAIN CONTENT ====================
st.title("📧 Email Automation Dashboard")
st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📤 Send Manual", "⏰ Schedule Manager", "📜 Live Logs", "📊 Email History"])

# ==================== TAB 1: SEND MANUAL ====================
with tab1:
    st.header("📤 Send Manual Email")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        to = st.text_input("Recipient Email", value=RECIPIENT, key="manual_to")
        subject = st.text_input("Subject", value=SUBJECT, key="manual_subject")
        body = st.text_area("Message Body", value=BODY, height=200, key="manual_body")
    
    with col2:
        st.markdown("### 📋 Quick Templates")
        
        if st.button("📝 Daily Report", use_container_width=True):
            st.session_state.template_subject = "Daily Report - " + datetime.now().strftime("%Y-%m-%d")
            st.session_state.template_body = """Dear Team,

Here is your daily report for today:

✅ Tasks Completed:
- Task 1
- Task 2

🔄 In Progress:
- Task 3

📌 Pending:
- Task 4

Best regards,
Automation System"""
            st.success("✅ Daily Report template loaded!")
            st.rerun()
        
        if st.button("🔔 Reminder", use_container_width=True):
            st.session_state.template_subject = "Reminder: Action Required"
            st.session_state.template_body = """Dear Recipient,

This is a friendly reminder to complete your pending tasks.

⏰ Deadline: [Insert Date]
📋 Action Items:
- [ ] Complete task 1
- [ ] Review task 2
- [ ] Submit report

Please take action at your earliest convenience.

Thank you!"""
            st.success("✅ Reminder template loaded!")
            st.rerun()
        
        if st.button("📊 Weekly Summary", use_container_width=True):
            st.session_state.template_subject = "Weekly Summary - Week " + datetime.now().strftime("%W")
            st.session_state.template_body = """Weekly Activity Summary

📈 Statistics:
- Total Tasks: X
- Completed: Y
- Pending: Z

🎯 Key Achievements:
- Achievement 1
- Achievement 2

📝 Notes:
[Add your notes here]

Regards,
Automation System"""
            st.success("✅ Weekly Summary template loaded!")
            st.rerun()
        
        # Load template if set
        if "template_subject" in st.session_state and st.session_state.template_subject:
            st.info(f"**Loaded Template:** {st.session_state.template_subject}")
            if st.button("🗑️ Clear Template", use_container_width=True):
                st.session_state.template_subject = ""
                st.session_state.template_body = ""
                st.rerun()
    
    # Apply template values if available
    if "template_subject" in st.session_state and st.session_state.template_subject:
        subject = st.session_state.template_subject
    if "template_body" in st.session_state and st.session_state.template_body:
        body = st.session_state.template_body
    
    
    # THE SEND BUTTON - This was missing!
    st.divider()
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("🚀 Send Email Now", type="primary", use_container_width=True):
            if not scheduler.service:
                st.error("⚠️ Please connect to Gmail first! (Use the sidebar)")
            elif not to or not subject or not body:
                st.error("⚠️ Please fill in all fields!")
            elif "@" not in to:
                st.error("⚠️ Please enter a valid email address!")
            else:
                with st.spinner("📤 Sending email..."):
                    try:
                        result = send_email(scheduler.service, "me", to, subject, body)
                        log_email(to, subject, result["status"], 
                                 result.get("message_id") or result.get("error"))
                        
                        if result["status"] == "success":
                            st.success(f"✅ Email sent successfully to {to}!")
                            st.info(f"📧 Message ID: `{result['message_id']}`")
                            scheduler.log_message(f"Manual email sent to {to}: {subject}")
                            
                            # Clear form after successful send
                            if st.button("📝 Send Another Email"):
                                st.rerun()
                        else:
                            st.error(f"❌ Failed to send email: {result['error']}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("🔄 Reset Form", use_container_width=True):
            st.session_state.final_to = RECIPIENT
            st.session_state.final_subject = SUBJECT
            st.session_state.final_body = BODY
            st.session_state.template_subject = ""
            st.session_state.template_body = ""
            st.rerun()
    
    # Display Existing Schedules
# ==================== TAB 2: SCHEDULE MANAGER ====================
with tab2:
    st.header("⏰ Schedule Manager")
    
    # Add New Schedule
    with st.expander("➕ Add New Scheduled Email", expanded=False):
        with st.form("add_schedule_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                sched_time = st.time_input("Time (24h format)", value=None, key="sched_time_input")
                sched_recipient = st.text_input("Recipient", value=RECIPIENT, key="sched_recipient_input")
            with col2:
                sched_subject = st.text_input("Subject", value=SUBJECT, key="sched_subject_input")
                sched_body = st.text_area("Body", value=BODY, height=100, key="sched_body_input")
            
            submitted = st.form_submit_button("✅ Add Schedule", type="primary", use_container_width=True)
            
            if submitted:
                if sched_time is None:
                    st.error("⚠️ Please select a time!")
                elif not scheduler.service:
                    st.error("⚠️ Please connect to Gmail first!")
                else:
                    time_str = sched_time.strftime("%H:%M")
                    schedule_id = scheduler.add_schedule(
                        time_str,
                        sched_recipient,
                        sched_subject,
                        sched_body
                    )
                    st.success(f"✅ Schedule added successfully!")
                    st.info(f"⏰ Will run daily at {time_str}")
                    st.rerun()
    
    # Display Existing Schedules
    st.subheader("📅 Active Schedules")
    
    if scheduler.schedules:
        for idx, sched in enumerate(scheduler.schedules):
            with st.container():
                st.markdown("---")
                col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 1, 1])
                
                with col1:
                    st.markdown(f"⏰ **{sched['time']}**")
                    created_date = datetime.fromisoformat(sched['created_at']).strftime('%Y-%m-%d')
                    st.caption(f"Created: {created_date}")
                
                with col2:
                    st.markdown(f"📧 **{sched['recipient']}**")
                    subject_preview = sched['subject'][:40] + "..." if len(sched['subject']) > 40 else sched['subject']
                    st.caption(f"📝 {subject_preview}")
                
                with col3:
                    status_badge = "🟢 Active" if sched["active"] else "🔴 Inactive"
                    st.markdown(status_badge)
                
                with col4:
                    # Toggle active/inactive
                    new_status = st.toggle("On", value=sched["active"], key=f"toggle_{sched['id']}")
                    if new_status != sched["active"]:
                        sched["active"] = new_status
                        scheduler.save_schedules()
                        st.success("✅ Updated!")
                        st.rerun()
                
                with col5:
                    if st.button("🗑️", key=f"delete_{sched['id']}", help="Delete schedule"):
                        scheduler.remove_schedule(sched['id'])
                        st.success("🗑️ Deleted!")
                        st.rerun()
    else:
        st.info("📭 No schedules yet. Add one above!")
        st.markdown("""
        **How to use:**
        1. Click '➕ Add New Scheduled Email'
        2. Select time, recipient, subject, and body
        3. Click '✅ Add Schedule'
        4. Start the scheduler from the sidebar
        """)
    
    # Scheduler Status
    st.divider()
    st.subheader("🎯 Scheduler Status")
    status = scheduler.get_status()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Schedules", status["total_schedules"])
    col2.metric("Active", status["active_schedules"])
    col3.metric("Inactive", status["total_schedules"] - status["active_schedules"])
    col4.metric("Status", "🟢 Running" if status["running"] else "🔴 Stopped")

# ==================== TAB 3: LIVE LOGS ====================
with tab3:
    st.header("📜 Live Logs")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (every 5 seconds)", value=False)
    
    if os.path.exists(LIVE_LOG_FILE):
        try:
            # Read last 50 lines with UTF-8 encoding
            with open(LIVE_LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                if lines:
                    # Show last 50 lines
                    recent_logs = lines[-50:]
                    logs_text = "".join(recent_logs)
                    
                    # Display logs in a scrollable box
                    st.code(logs_text, language="bash")
                    
                    # Show line count
                    st.caption(f"📊 Showing last {len(recent_logs)} of {len(lines)} total log entries")
                else:
                    st.info("📭 No logs yet. Start the scheduler or send an email to see activity here.")
            
            # Clear logs button
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("🗑️ Clear Logs", use_container_width=True):
                    try:
                        with open(LIVE_LOG_FILE, 'w', encoding='utf-8') as f:
                            f.write("")
                        st.success("✅ Logs cleared!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error clearing logs: {e}")
        
        except UnicodeDecodeError:
            st.error("❌ Error reading log file. Encoding issue detected.")
            if st.button("🔄 Recreate Log File"):
                try:
                    os.remove(LIVE_LOG_FILE)
                    with open(LIVE_LOG_FILE, 'w', encoding='utf-8') as f:
                        f.write("")
                    st.success("✅ Log file recreated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"❌ Error reading logs: {str(e)}")
    else:
        st.info("📭 No log file found. Logs will appear here when you start the scheduler or send emails.")
        
        # Create log file button
        if st.button("📝 Create Log File"):
            try:
                with open(LIVE_LOG_FILE, 'w', encoding='utf-8') as f:
                    f.write("")
                st.success("✅ Log file created!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating log file: {e}")
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(5)
        st.rerun()
        
# ==================== TAB 4: EMAIL HISTORY ====================
with tab4:
    st.header("📊 Email History")
    
    # Ensure logger is setup
    setup_logger()
    
    if os.path.exists(LOG_PATH):
        try:
            # Read CSV with UTF-8 encoding
            df = pd.read_csv(LOG_PATH, encoding='utf-8')
            
            if len(df) > 0:
                # Convert timestamp to readable format
                df["Timestamp"] = pd.to_datetime(df["Timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
                
                # Filter options
                col1, col2, col3 = st.columns(3)
                with col1:
                    status_filter = st.selectbox("Filter by Status", ["All", "success", "error"], key="status_filter_hist")
                with col2:
                    search_term = st.text_input("🔍 Search", placeholder="Recipient or subject...", key="search_hist")
                with col3:
                    limit = st.number_input("Show last N emails", min_value=5, max_value=100, value=20, key="limit_hist")
                
                # Apply filters
                filtered_df = df.copy()
                if status_filter != "All":
                    filtered_df = filtered_df[filtered_df["Status"] == status_filter]
                if search_term:
                    filtered_df = filtered_df[
                        filtered_df["Recipient"].str.contains(search_term, case=False, na=False) |
                        filtered_df["Subject"].str.contains(search_term, case=False, na=False)
                    ]
                
                # Sort by timestamp (newest first)
                filtered_df = filtered_df.sort_values("Timestamp", ascending=False)
                filtered_df = filtered_df.head(limit)
                
                # Display stats
                st.divider()
                col1, col2, col3, col4 = st.columns(4)
                total_emails = len(filtered_df)
                success_count = len(filtered_df[filtered_df["Status"] == "success"])
                error_count = len(filtered_df[filtered_df["Status"] == "error"])
                success_rate = (success_count / total_emails * 100) if total_emails > 0 else 0
                
                col1.metric("📧 Total", total_emails)
                col2.metric("✅ Success", success_count)
                col3.metric("❌ Failed", error_count)
                col4.metric("📈 Success Rate", f"{success_rate:.1f}%")
                
                # Display table
                st.divider()
                st.subheader(f"📋 Email Records ({len(filtered_df)} emails)")
                
                st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Export button
                st.divider()
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"email_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("📭 No emails sent yet. Send an email to see it here!")
                
                # Test button
                if st.button("🧪 Send Test Email"):
                    if scheduler.service:
                        with st.spinner("Sending test email..."):
                            result = send_email(
                                scheduler.service,
                                "me",
                                RECIPIENT,
                                "Test Email",
                                "This is a test email to verify the logging system."
                            )
                            log_email(RECIPIENT, "Test Email", result["status"], 
                                    result.get("message_id") or result.get("error"))
                            st.success("✅ Test email sent! Refresh to see it in history.")
                            st.rerun()
                    else:
                        st.error("⚠️ Please connect to Gmail first!")
        
        except pd.errors.EmptyDataError:
            st.warning("⚠️ Log file is empty. Send an email to populate it.")
        except Exception as e:
            st.error(f"❌ Error reading log file: {str(e)}")
            with st.expander("Error Details"):
                st.exception(e)
    else:
        st.warning("⚠️ Log file not found at: " + LOG_PATH)
        st.info("📝 The log file will be created when you send your first email.")
        
        # Quick action
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Go to Send Manual", use_container_width=True):
                st.rerun()