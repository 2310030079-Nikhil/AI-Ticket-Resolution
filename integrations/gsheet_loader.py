import os
import time
import gspread
from gspread.exceptions import APIError, SpreadsheetNotFound, WorksheetNotFound
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetLoader:
    def __init__(self, sheet_name, worksheet_name, creds_path):
        self.sheet_name = sheet_name
        self.worksheet_name = worksheet_name
        self.creds_path = creds_path
        self.df = None
    
    def _authorize_google_sheet(self):
        if not os.path.exists(self.creds_path):
            raise FileNotFoundError(f"Credentials file not found at: {self.creds_path}")

        scope = [
            "https://spreadsheets.google.com/feeds", 
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_path, scope)
        client = gspread.authorize(creds)
        return client

    def load_data(self, max_retries=4, base_delay=2):
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                client = self._authorize_google_sheet()
                sheet = client.open(self.sheet_name).worksheet(self.worksheet_name)
                data = sheet.get_all_records()
                self.df = pd.DataFrame(data)
                return self.df
            except APIError as e:
                last_error = e
                err_msg = str(e)
                # Check for transient HTTP error codes: 503, 500, 502, 504, 429
                is_transient = any(code in err_msg for code in ["503", "500", "502", "504", "429"])
                if is_transient and attempt < max_retries:
                    delay = base_delay * (2 ** (attempt - 1))
                    print(f"Transient Google API error ({err_msg}). Retrying in {delay}s (attempt {attempt}/{max_retries})...")
                    time.sleep(delay)
                    continue
                raise
            except Exception as e:
                last_error = e
                err_msg = str(e)
                if ("503" in err_msg or "timed out" in err_msg.lower()) and attempt < max_retries:
                    delay = base_delay * (2 ** (attempt - 1))
                    print(f"Temporary connection error ({err_msg}). Retrying in {delay}s (attempt {attempt}/{max_retries})...")
                    time.sleep(delay)
                    continue
                raise
        if last_error:
            raise last_error
    
    def get_dataframe(self):
        if self.df is not None:
            return self.df
        else:
            raise ValueError("Data has not been loaded yet. Call load_data() first.")
    
    def preview_data(self, num_rows=5):
        if self.df is not None:
            return self.df.head(num_rows)
        else:
            raise ValueError("Data has not been loaded yet. Call load_data() first.")

if __name__ == "__main__":
    # Example usage
    SHEET_NAME = "tickets1"
    WORKSHEET_NAME = "Sheet1"
    CREDS_PATH = "credentials/service_account.json"
    
    google_sheet_loader = GoogleSheetLoader(SHEET_NAME, WORKSHEET_NAME, CREDS_PATH)
    google_sheet_loader.load_data()
    print(google_sheet_loader.preview_data())
    google_sheet_loader.df.to_csv("data/raw/tickets6.csv", index=False)
    print()
    print("Data saved to 'data/raw/tickets6.csv'.")