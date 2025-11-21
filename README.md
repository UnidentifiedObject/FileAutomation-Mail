# FileAutomation-Mail

Automates file organization with timestamped renaming, daily log rotation, and email summary reports.

---

## Features

- Automatically moves and renames files in a test folder with a timestamp.  
- Creates daily log files with automatic rotation (keeps logs from the last 7 days).  
- Sends an email summary of processed files and errors, with the log attached.  
- Secure handling of credentials via a `.env` file (no sensitive info stored in code).

---

## How to Use

1. **Set up credentials**  
   - Copy `env_template.txt`, rename it to `.env`, and fill in your Gmail credentials and app password.  

2. **Run the script**  
   - The script will automatically create the necessary folders (`TestFiles/` and `logs/`) if they don’t exist.  

3. **Add files to process**  
   - Place the files you want to automate inside the `TestFiles/` folder.  

4. **Check results**  
   - Processed files will be moved into a date-stamped folder.  
   - Logs will be written in the `logs/` folder, with a new log created each day and older logs automatically deleted after 7 days.  
   - An email summary of the processed files and any errors will be sent after each run.  

---

## Required Libraries

- `python-dotenv`  

Install with:

```bash
pip install python-dotenv
