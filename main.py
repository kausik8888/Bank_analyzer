import streamlit as st
import os
from processors.hdfc_processor import HDFCStatementProcessor
from analysis.transaction_analyzer import TransactionAnalyzer
from ui.dashboard import DashboardUI

class BankAnalyzer:
    def __init__(self):
        self.supported_banks = {
            "HDFC Bank": "hdfc",
            # Add more banks here as needed
        }
        self.processors = {
            "hdfc": HDFCStatementProcessor()
        }
        self.analyzer = TransactionAnalyzer()
        self.ui = DashboardUI()
    
    def run(self):
        """Run the bank statement analyzer application"""
        self.ui.render_header()
        
        # Get bank selection and file upload
        selected_bank = self.ui.render_bank_selector(self.supported_banks)
        uploaded_file = self.ui.render_file_upload()
        
        if uploaded_file is not None:
            try:
                # Process the statement
                df = self._process_statement(uploaded_file, selected_bank)
                
                # Analyze transactions
                analysis = self.analyzer.analyze_transactions(df)
                
                # Display results
                self.ui.render_summary(analysis['summary'])
                self.ui.render_charts(
                    self.analyzer,
                    analysis['monthly_analysis'],
                    analysis['balance_trend']
                )
                self.ui.render_transaction_details(df)
                
            except Exception as e:
                st.error(f"Error processing the statement: {str(e)}")
    
    def _process_statement(self, uploaded_file, selected_bank):
        """Process the uploaded statement file"""
        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        try:
            # Process the statement
            bank_type = self.supported_banks[selected_bank]
            processor = self.processors[bank_type]
            df = processor.process(temp_path)
            return df
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    analyzer = BankAnalyzer()
    analyzer.run()
