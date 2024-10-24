#!/usr/bin/env python3

import os
import sys
import datetime
import shutil
import csv
import PySimpleGUI as sg
from cryptography.fernet import Fernet
from fpdf import FPDF

# Constants for directories and files
BASE_DIR = os.path.expanduser("~/logger")
LOG_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
ARCHIVE_DIR = os.path.join(LOG_DIR, "archive")
TIMESHEET_LOG_ENC = os.path.join(LOG_DIR, "timesheet.log.enc")
PROGRESS_LOG_ENC = os.path.join(LOG_DIR, "progress.log.enc")
KEY_FILE = os.path.join(BASE_DIR, "key.key")

# Ensure necessary directories exist
for directory in [LOG_DIR, REPORTS_DIR, ARCHIVE_DIR]:
    os.makedirs(directory, exist_ok=True)

# Data Security: Encryption Setup
def generate_key():
    """Generate and save a key for encryption."""
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load the encryption key from the key file."""
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read()
    return key

# Initialize encryption
key = load_key()
fernet = Fernet(key)

def encrypt_file(file_path, enc_file_path):
    """Encrypt a file and save it."""
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(enc_file_path, 'wb') as enc_file:
        enc_file.write(encrypted)
    os.remove(file_path)

def decrypt_file(enc_file_path, file_path):
    """Decrypt a file and save it."""
    with open(enc_file_path, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_path, 'wb') as file:
        file.write(decrypted)

def log_action(action, client="N/A"):
    """Log an action with a timestamp and client."""
    timestamp = current_timestamp()
    with open(TIMESHEET_LOG_ENC, 'ab') as log_file:
        # Encrypt the log entry before writing
        entry = f"{timestamp},{client},{action}\n".encode()
        encrypted_entry = fernet.encrypt(entry)
        log_file.write(encrypted_entry + b'\n')

def current_timestamp():
    """Return current timestamp in ISO 8601 format."""
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def view_log(log_file_path, log_type="Timesheet"):
    """Return the decrypted contents of a log file."""
    if os.path.isfile(log_file_path):
        try:
            decrypt_file(log_file_path, "temp.log")
            with open("temp.log", 'r') as log_file:
                reader = csv.reader(log_file)
                entries = [row for row in reader if len(row) == 3]
            os.remove("temp.log")
            if log_type == "Progress":
                formatted_entries = "\n".join([", ".join(entry) for entry in entries])
            else:
                formatted_entries = "\n".join([f"{row[0]} | Client: {row[1]} | Action: {row[2]}" for row in entries])
            return formatted_entries
        except Exception as e:
            return f"Error decrypting {log_type.lower()} log: {str(e)}"
    else:
        return f"No {log_type.lower()} log found.\n"

def consolidate_logs():
    """Consolidate timesheet logs into progress.log with headers and directory structure."""
    try:
        # Decrypt timesheet.log
        decrypt_file(TIMESHEET_LOG_ENC, "temp_timesheet.log")
        
        with open(PROGRESS_LOG_ENC, 'ab') as progress_file_enc:
            # Write header
            header = f"\n===== Progress Log Consolidation (Updated: {current_timestamp()}) =====\n".encode()
            encrypted_header = fernet.encrypt(header)
            progress_file_enc.write(encrypted_header + b'\n')
            
            # Add directory structure
            dir_structure = "\n--- Log Directory Structure ---\n"
            encrypted_dir_structure = fernet.encrypt(dir_structure.encode())
            progress_file_enc.write(encrypted_dir_structure + b'\n')
            for root, dirs, files in os.walk(LOG_DIR):
                level = root.replace(LOG_DIR, '').count(os.sep)
                indent = ' ' * 4 * level
                dir_line = f"{indent}{os.path.basename(root)}/\n"
                encrypted_dir_line = fernet.encrypt(dir_line.encode())
                progress_file_enc.write(encrypted_dir_line + b'\n')
                sub_indent = ' ' * 4 * (level + 1)
                for f in files:
                    file_line = f"{sub_indent}{f}\n"
                    encrypted_file_line = fernet.encrypt(file_line.encode())
                    progress_file_enc.write(encrypted_file_line + b'\n')
            dir_end = "\n--- End of Directory Structure ---\n\n"
            encrypted_dir_end = fernet.encrypt(dir_end.encode())
            progress_file_enc.write(encrypted_dir_end + b'\n')
            
            # Append timesheet.log
            if os.path.isfile("temp_timesheet.log"):
                append_header = "\n--- Concatenated Timesheet Log ---\n".encode()
                encrypted_append_header = fernet.encrypt(append_header)
                progress_file_enc.write(encrypted_append_header + b'\n')
                with open("temp_timesheet.log", 'rb') as timesheet:
                    for line in timesheet:
                        encrypted_line = fernet.encrypt(line)
                        progress_file_enc.write(encrypted_line + b'\n')
                append_end = "\n--- End of Timesheet Log ---\n\n".encode()
                encrypted_append_end = fernet.encrypt(append_end)
                progress_file_enc.write(encrypted_append_end + b'\n')
                os.remove("temp_timesheet.log")
            else:
                no_timesheet = "\nNo timesheet log to append.\n\n".encode()
                encrypted_no_timesheet = fernet.encrypt(no_timesheet)
                progress_file_enc.write(encrypted_no_timesheet + b'\n')
        
        sg.popup("Logs Consolidated", "All logs have been consolidated into progress.log.", title="Success")
    except Exception as e:
        sg.popup(f"Error Consolidating Logs: {str(e)}", title="Error")

def generate_weekly_report():
    """Generate a weekly report summarizing work hours per client."""
    try:
        # Decrypt timesheet.log
        decrypt_file(TIMESHEET_LOG_ENC, "temp_timesheet.log")
        
        report_date = datetime.datetime.now().strftime("%Y-%m-%d")
        report_file = os.path.join(REPORTS_DIR, f"weekly_report_{report_date}.pdf")
        
        # Data structure to hold work sessions
        work_sessions = {}
        
        # Read the timesheet log
        with open("temp_timesheet.log", 'r') as log_file:
            reader = csv.reader(log_file)
            for row in reader:
                if len(row) != 3:
                    continue  # Skip malformed lines
                timestamp_str, client, action = row
                try:
                    timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    continue  # Skip lines with invalid timestamp
                date = timestamp.date()
                if date not in work_sessions:
                    work_sessions[date] = {}
                if client not in work_sessions[date]:
                    work_sessions[date][client] = {'Clock In': None, 'Start Break': None, 'Resume Work': None, 'Clock Out': None}
                if action in work_sessions[date][client]:
                    work_sessions[date][client][action] = timestamp
        
        # Initialize PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Weekly Report - {report_date}", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 10, "Date", 1)
        pdf.cell(40, 10, "Client", 1)
        pdf.cell(30, 10, "Clock In", 1)
        pdf.cell(30, 10, "Start Break", 1)
        pdf.cell(30, 10, "Resume Work", 1)
        pdf.cell(30, 10, "Clock Out", 1)
        pdf.cell(30, 10, "Total Hours", 1)
        pdf.ln()
        
        pdf.set_font("Arial", '', 12)
        
        total_week_hours = 0
        
        for date in sorted(work_sessions.keys()):
            for client in work_sessions[date]:
                session = work_sessions[date][client]
                if session['Clock In'] and session['Clock Out']:
                    clock_in = session['Clock In']
                    clock_out = session['Clock Out']
                    start_break = session['Start Break']
                    resume_work = session['Resume Work']
                    
                    total_seconds = (clock_out - clock_in).total_seconds()
                    
                    if start_break and resume_work:
                        break_seconds = (resume_work - start_break).total_seconds()
                        total_seconds -= break_seconds
                        
                    hours = int(total_seconds // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    total_hours = f"{hours}:{minutes:02d}"
                    total_week_hours += hours
                else:
                    clock_in = start_break = resume_work = clock_out = "Incomplete"
                    total_hours = "-"
                
                pdf.cell(40, 10, str(date), 1)
                pdf.cell(40, 10, client, 1)
                pdf.cell(30, 10, clock_in.strftime('%H:%M:%S') if isinstance(clock_in, datetime.datetime) else clock_in, 1)
                pdf.cell(30, 10, start_break.strftime('%H:%M:%S') if isinstance(start_break, datetime.datetime) else start_break, 1)
                pdf.cell(30, 10, resume_work.strftime('%H:%M:%S') if isinstance(resume_work, datetime.datetime) else resume_work, 1)
                pdf.cell(30, 10, clock_out.strftime('%H:%M:%S') if isinstance(clock_out, datetime.datetime) else clock_out, 1)
                pdf.cell(30, 10, total_hours, 1)
                pdf.ln()
        
        # Append total hours
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 10, "Total Hours Worked This Week:", 0)
        pdf.cell(30, 10, f"{total_week_hours} hours", 0)
        
        # Output PDF
        pdf.output(report_file)
        
        os.remove("temp_timesheet.log")  # Clean up temporary file
        
        sg.popup("Report Generated", f"Weekly report generated at:\n{report_file}", title="Success")
        
        # Archive the current timesheet.log
        archive_filename = f"timesheet_{report_date}.log.enc"
        shutil.move(TIMESHEET_LOG_ENC, os.path.join(ARCHIVE_DIR, archive_filename))
        
        sg.popup("Logs Archived", "All individual logs have been archived and the current log has been reset.", title="Success")
    except Exception as e:
        sg.popup(f"Error Generating Report: {str(e)}", title="Error")
        if os.path.exists("temp_timesheet.log"):
            os.remove("temp_timesheet.log")

def cleanup_logs():
    """Clean up logs by archiving progress.log and removing other logs."""
    try:
        # Archive progress.log
        if os.path.isfile(PROGRESS_LOG_ENC):
            progress_archive = f"progress_{datetime.datetime.now().strftime('%Y-%m-%d')}.log.enc"
            shutil.move(PROGRESS_LOG_ENC, os.path.join(ARCHIVE_DIR, progress_archive))
            sg.popup("Progress Log Archived", "progress.log has been archived.", title="Success")
        
        # Remove any other log files except progress.log.enc and timesheet.log.enc
        removed_files = []
        for file in os.listdir(LOG_DIR):
            file_path = os.path.join(LOG_DIR, file)
            if os.path.isfile(file_path) and file not in ["progress.log.enc", "timesheet.log.enc"]:
                os.remove(file_path)
                removed_files.append(file)
        
        if removed_files:
            removed_str = "\n".join(removed_files)
            sg.popup("Logs Removed", f"Removed log files:\n{removed_str}", title="Cleanup Complete")
        else:
            sg.popup("No Logs Removed", "No unnecessary log files found to remove.", title="Cleanup Complete")
    except Exception as e:
        sg.popup(f"Error Cleaning Up Logs: {str(e)}", title="Error")

def get_active_client():
    """Find the last active client that hasn't been clocked out yet."""
    if not os.path.isfile(TIMESHEET_LOG_ENC):
        return None
    
    try:
        # Decrypt timesheet.log
        decrypt_file(TIMESHEET_LOG_ENC, "temp_timesheet.log")
        
        with open("temp_timesheet.log", 'r') as log_file:
            reader = csv.reader(log_file)
            entries = list(reader)
        
        os.remove("temp_timesheet.log")
        
        # Traverse the log in reverse to find the last 'Clock In' without 'Clock Out'
        for idx in range(len(entries)-1, -1, -1):
            row = entries[idx]
            if len(row) != 3:
                continue
            _, client, action = row
            if action == "Clock In":
                # Check if there's a corresponding 'Clock Out' after this 'Clock In' for the same client
                has_clocked_out = False
                for subsequent_row in entries[idx+1:]:
                    if len(subsequent_row) != 3:
                        continue
                    _, sub_client, sub_action = subsequent_row
                    if sub_action == "Clock Out" and sub_client == client:
                        has_clocked_out = True
                        break
                if not has_clocked_out:
                    return client
        return None
    except Exception as e:
        sg.popup(f"Error Finding Active Client: {str(e)}", title="Error")
        return None

def clock_out():
    """Handle the Clock Out action by associating it with the correct client."""
    active_client = get_active_client()
    if active_client:
        log_action("Clock Out", active_client)
        sg.popup("Clock Out Successful", f"You have clocked out at {current_timestamp()} for client '{active_client}'.", title="Success")
    else:
        sg.popup("Error", "No active client found. Please Clock In first.", title="Error")

def select_client():
    """Prompt the user to select or enter a client."""
    clients = set()
    if os.path.isfile(TIMESHEET_LOG_ENC):
        try:
            decrypt_file(TIMESHEET_LOG_ENC, "temp_timesheet.log")
            with open("temp_timesheet.log", 'r') as log_file:
                reader = csv.reader(log_file)
                for row in reader:
                    if len(row) == 3:
                        clients.add(row[1])
            os.remove("temp_timesheet.log")
        except Exception as e:
            sg.popup(f"Error Decrypting Logs: {str(e)}", title="Error")
            return "N/A"
    clients = sorted(list(clients))
    
    layout = [
        [sg.Text("Select a client from the list below or enter a new client name:")],
        [sg.Listbox(values=clients, size=(40, 10), key='-CLIENT_LIST-', enable_events=True)],
        [sg.Text("New Client:"), sg.Input(key='-NEW_CLIENT-')],
        [sg.Button("Select"), sg.Button("Cancel")]
    ]
    
    window = sg.Window("Select Client", layout, modal=True)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            window.close()
            return "N/A"
        elif event == "Select":
            if values['-CLIENT_LIST-']:
                selected_client = values['-CLIENT_LIST-'][0]
                window.close()
                return selected_client
            elif values['-NEW_CLIENT-'].strip():
                new_client = values['-NEW_CLIENT-'].strip()
                window.close()
                return new_client
            else:
                sg.popup("Please select an existing client or enter a new client name.", title="Input Required")
    
def export_logs():
    """Export logs in different formats (CSV and PDF)."""
    layout = [
        [sg.Text("Select Export Format:")],
        [sg.Radio("CSV", "FORMAT", default=True, key='-CSV-')],
        [sg.Radio("PDF", "FORMAT", key='-PDF-')],
        [sg.Button("Export"), sg.Button("Cancel")]
    ]
    
    window = sg.Window("Export Logs", layout, modal=True)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            window.close()
            return
        elif event == "Export":
            if values['-CSV-']:
                export_csv()
                sg.popup("Export Successful", f"Logs exported as CSV.", title="Success")
                window.close()
                return
            elif values['-PDF-']:
                export_pdf()
                sg.popup("Export Successful", f"Logs exported as PDF.", title="Success")
                window.close()
                return
            else:
                sg.popup("Please select an export format.", title="Input Required")

def export_csv():
    """Export timesheet.log to a CSV file."""
    try:
        # Decrypt timesheet.log
        decrypt_file(TIMESHEET_LOG_ENC, "temp_timesheet.log")
        
        export_file = os.path.join(REPORTS_DIR, f"export_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv")
        shutil.copy("temp_timesheet.log", export_file)
        
        os.remove("temp_timesheet.log")
    except Exception as e:
        sg.popup(f"Error Exporting CSV: {str(e)}", title="Error")

def export_pdf():
    """Export timesheet.log to a PDF file."""
    try:
        # Decrypt timesheet.log
        decrypt_file(TIMESHEET_LOG_ENC, "temp_timesheet.log")
        
        report_date = datetime.datetime.now().strftime("%Y-%m-%d")
        report_file = os.path.join(REPORTS_DIR, f"export_{report_date}.pdf")
        
        # Initialize PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Exported Logs - {report_date}", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(60, 10, "Timestamp", 1)
        pdf.cell(60, 10, "Client", 1)
        pdf.cell(60, 10, "Action", 1)
        pdf.ln()
        
        pdf.set_font("Arial", '', 12)
        
        # Read the log and add to PDF
        with open("temp_timesheet.log", 'r') as log_file:
            reader = csv.reader(log_file)
            for row in reader:
                if len(row) != 3:
                    continue
                timestamp, client, action = row
                pdf.cell(60, 10, timestamp, 1)
                pdf.cell(60, 10, client, 1)
                pdf.cell(60, 10, action, 1)
                pdf.ln()
        
        # Output PDF
        pdf.output(report_file)
        
        os.remove("temp_timesheet.log")  # Clean up temporary file
    except Exception as e:
        sg.popup(f"Error Exporting PDF: {str(e)}", title="Error")

def main_menu():
    """Display the main menu and handle user input."""
    sg.theme('DarkBlue3')  # You can choose any theme you like

    # Status Indicator Variables
    status = "Not Clocked In"
    active_client = "N/A"

    layout = [
        [sg.Text("Time Logger", font=("Helvetica", 16), justification='center', expand_x=True)],
        [sg.Text(f"Status: {status}", key='-STATUS-', font=("Helvetica", 12))],
        [sg.Text(f"Active Client: {active_client}", key='-CLIENT_STATUS-', font=("Helvetica", 12))],
        [sg.Button("Clock In", size=(20, 2))],
        [sg.Button("Start Break", size=(20, 2))],
        [sg.Button("Resume Work", size=(20, 2))],
        [sg.Button("Clock Out", size=(20, 2))],
        [sg.Button("View Timesheet Log", size=(20, 2))],
        [sg.Button("View Progress Log", size=(20, 2))],
        [sg.Button("Generate Weekly Report", size=(20, 2))],
        [sg.Button("Export Logs", size=(20, 2))],
        [sg.Button("Consolidate Logs", size=(20, 2))],
        [sg.Button("Cleanup Logs", size=(20, 2))],
        [sg.Button("Quit", size=(20, 2))]
    ]

    window = sg.Window("PayLogger", layout, keep_on_top=True, finalize=True, resizable=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Quit":
            # Confirm before quitting
            if sg.popup_yes_no("Are you sure you want to quit?") == 'Yes':
                # Consolidate and clean up logs before exiting
                consolidate_logs()
                cleanup_logs()
                break
        elif event == "Clock In":
            client = select_client()
            if client != "N/A":
                log_action("Clock In", client)
                sg.popup("Clock In Successful", f"You have clocked in at {current_timestamp()} for client '{client}'.", title="Success")
                # Update status indicators
                status = "Clocked In"
                active_client = client
                window['-STATUS-'].update(f"Status: {status}")
                window['-CLIENT_STATUS-'].update(f"Active Client: {active_client}")
            else:
                sg.popup("Clock In Cancelled", "No client selected.", title="Cancelled")
        elif event == "Start Break":
            if status == "Clocked In":
                log_action("Start Break")
                sg.popup("Break Started", f"Break started at {current_timestamp()}.", title="Success")
                # Update status indicators
                status = "On Break"
                window['-STATUS-'].update(f"Status: {status}")
            else:
                sg.popup("Cannot Start Break", "You must be clocked in to start a break.", title="Error")
        elif event == "Resume Work":
            if status == "On Break":
                log_action("Resume Work")
                sg.popup("Work Resumed", f"Work resumed at {current_timestamp()}.", title="Success")
                # Update status indicators
                status = "Clocked In"
                window['-STATUS-'].update(f"Status: {status}")
            else:
                sg.popup("Cannot Resume Work", "You are not currently on a break.", title="Error")
        elif event == "Clock Out":
            # Handle clock out with client association
            previous_active_client = active_client  # Store previous client
            clock_out()
            # Update status indicators
            active_client = "N/A"
            status = "Not Clocked In"
            window['-STATUS-'].update(f"Status: {status}")
            window['-CLIENT_STATUS-'].update(f"Active Client: {active_client}")
        elif event == "View Timesheet Log":
            log_contents = view_log(TIMESHEET_LOG_ENC, "Timesheet")
            sg.popup_scrolled(log_contents, title="Timesheet Log", size=(80, 20))
        elif event == "View Progress Log":
            log_contents = view_log(PROGRESS_LOG_ENC, "Progress")
            sg.popup_scrolled(log_contents, title="Progress Log", size=(80, 20))
        elif event == "Generate Weekly Report":
            generate_weekly_report()
        elif event == "Export Logs":
            export_logs()
        elif event == "Consolidate Logs":
            consolidate_logs()
        elif event == "Cleanup Logs":
            cleanup_logs()
        # Update active_client and status based on log entries
        # (This could be improved by parsing the logs to determine the current state)
    
    window.close()

if __name__ == "__main__":
    main_menu()
