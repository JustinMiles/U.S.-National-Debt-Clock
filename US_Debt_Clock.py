import tkinter as tk
import requests
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger object
logger = logging.getLogger()

# Create a StringIO object to capture log messages
from io import StringIO
log_stream = StringIO()
stream_handler = logging.StreamHandler(log_stream)
logger.addHandler(stream_handler)

def fetch_debt():
    base_url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny'
    try:
        # Fetch the latest debt record
        latest_response = requests.get(f'{base_url}?sort=-record_date&page[size]=1')
        latest_response.raise_for_status()
        latest_data = latest_response.json()
        latest_record = latest_data['data'][0]
        latest_debt = float(latest_record['tot_pub_debt_out_amt'])
        latest_date = datetime.strptime(latest_record['record_date'], '%Y-%m-%d')

        # Fetch all debt records for the past year
        one_year_ago = latest_date - timedelta(days=365)
        one_year_ago_formatted = one_year_ago.strftime('%Y-%m-%d')
        year_response = requests.get(f'{base_url}?filter=record_date:gte:{one_year_ago_formatted}&sort=record_date')
        year_response.raise_for_status()
        year_data = year_response.json()

        # Compute total increase and daily average increase
        records = year_data['data']
        total_increase = 0
        for i in range(1, len(records)):
            previous_debt = float(records[i - 1]['tot_pub_debt_out_amt'])
            current_debt = float(records[i]['tot_pub_debt_out_amt'])
            total_increase += (current_debt - previous_debt)

        total_days = len(records) - 1  # Number of days in the dataset
        average_daily_increase = total_increase / total_days

        now = datetime.now()
        time_since_latest = (now - latest_date).total_seconds() / (60 * 60 * 24)
        estimated_current_debt = latest_debt + (average_daily_increase * time_since_latest)

        per_second_increase = average_daily_increase / (24 * 60 * 60)

        logger.info(f"Estimated current debt: {estimated_current_debt}")
        logger.info(f"Per second increase: {per_second_increase}")

        return estimated_current_debt, per_second_increase
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return "N/A", 0

def update_debt():
    global estimated_current_debt, per_second_increase
    if estimated_current_debt == "N/A":
        debt_label.config(text="Loading...")
    else:
        estimated_current_debt += per_second_increase
        debt_label.config(text=f"U.S. National Debt: ${estimated_current_debt:,.2f}")
    # Schedule the update_debt function to run again after 1000 milliseconds (1 second)
    root.after(1000, update_debt)

def show_logs():
    # Create a new window to display the logs
    log_window = tk.Toplevel(root)
    log_window.title("Log Messages")
    
    # Create a Text widget to display the log messages
    log_text = tk.Text(log_window, wrap='word')
    log_text.pack(expand=True, fill='both')
    
    # Insert the log messages into the Text widget
    log_text.insert(tk.END, log_stream.getvalue())
    
    # Make the Text widget read-only
    log_text.config(state=tk.DISABLED)

# Create the main Tkinter window
root = tk.Tk()
root.title("U.S. National Debt Clock")

# Create and pack the label to display the debt value
debt_label = tk.Label(root, font=("Helvetica", 24))
debt_label.pack(pady=20)

# Create and pack the button to show log messages
log_button = tk.Button(root, text="Show Logs", command=show_logs)
log_button.pack(pady=10)

# Fetch the initial debt data
estimated_current_debt, per_second_increase = fetch_debt()
logger.info(f"Initial estimated current debt: {estimated_current_debt}")
logger.info(f"Initial per second increase: {per_second_increase}")

# Start the first update
update_debt()

# Run the Tkinter main loop
root.mainloop()