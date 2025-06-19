# Bank Statement Analyzer

This is a Streamlit web application for analyzing bank statements (currently supports HDFC Bank in XLS format).

## Features
- Upload your bank statement (XLS)
- Automatic parsing and cleaning of transactions
- Transaction summary and statistics
- Monthly withdrawal, deposit, and balance trend charts
- UPI transaction analysis with pie charts and statistics
- Download processed data as CSV

## How to Run Locally
1. Clone this repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Start the app:
   ```
   streamlit run main.py
   ```

## Deployment
- Deploy easily on [Streamlit Community Cloud](https://streamlit.io/cloud) or any cloud that supports Python and Streamlit.
- Ensure your `requirements.txt` is up to date for all dependencies (including `xlrd`).

## File Structure
- `main.py` - Main entry point for the Streamlit app
- `processors/` - Statement processors (e.g., HDFC)
- `analysis/` - Transaction analysis logic
- `ui/` - Dashboard and UI components
- `requirements.txt` - Python dependencies

## Notes
- Only HDFC Bank statements in `.xls` format are supported by default. Add more processors for other banks as needed.
- For any issues, ensure your environment has all dependencies installed.

---

Made with ❤️ using Streamlit.
