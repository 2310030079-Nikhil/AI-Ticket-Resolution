import os
import re
import pandas as pd

class TicketProcessor:
    def __init__(self, input_file=None, output_file=None, df=None, text_column="ticket_text"):
        if df is not None:
            self.df = df.copy()  # Use a copy of the provided DataFrame
        elif input_file is not None:
            self.df = pd.read_csv(input_file)  # Read from file if passed
        else:
            raise ValueError("Either 'df' or 'input_file' must be provided.")
        
        self.output_file = output_file
        self.text_column = text_column

    def clean_text(self, text):
        if not isinstance(text, str):
            text = str(text) if pd.notna(text) else ""
        return re.sub(r"[^a-zA-Z\s]", "", text.lower()).strip()

    def process_and_save(self):
        # Ensure ticket_id exists
        if "ticket_id" not in self.df.columns:
            id_candidates = ["ticket_id", "id", "ticketId", "TicketID", "ticket_no"]
            found_id = next((c for c in id_candidates if c in self.df.columns), None)
            if found_id:
                self.df["ticket_id"] = self.df[found_id].astype(str)
            else:
                self.df["ticket_id"] = [f"T{i+1:03d}" for i in range(len(self.df))]

        col = self.text_column
        if col not in self.df.columns:
            # Fallback candidates if the specified column is not present
            candidates = ["ticket_text", "text", "body", "description", "issue"]
            found = next((c for c in candidates if c in self.df.columns), None)
            if found:
                col = found
            else:
                raise KeyError(
                    f"Column '{self.text_column}' not found. Available columns in CSV: {list(self.df.columns)}"
                )
        self.df["clean_text"] = self.df[col].apply(self.clean_text)
        if self.output_file:
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            self.df.to_csv(self.output_file, index=False)
        return self.df

if __name__ == "__main__":
    processor = TicketProcessor("data/raw/tickets6.csv", "data/processed/preprocessed_tickets6.csv")
    processor.process_and_save()
    print(f"Preprocessed data saved to '{processor.output_file}'.")
