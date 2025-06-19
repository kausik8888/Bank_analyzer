import xlrd
import pandas as pd

class HDFCStatementProcessor:
    def __init__(self):
        self.expected_columns = [
            "Date", "Narration", "Chq./Ref.No.", "Value Dt",
            "Withdrawal Amt.", "Deposit Amt.", "Closing Balance"
        ]
    
    def process(self, file_path, export_csv_path=None):
        """Process HDFC bank statement
        Args:
            file_path: Path to the XLS bank statement
            export_csv_path: Optional path to export processed data as CSV
        """
        try:
            # Read the Excel file using xlrd
            workbook = xlrd.open_workbook(file_path)
            sheet = workbook.sheet_by_index(0)
            
            # Find delimiter rows (full rows of asterisks)
            delimiter_rows = self._find_delimiters(sheet)
            
            if len(delimiter_rows) < 2:
                raise ValueError("Could not find proper statement structure with '*' delimiters")
            
            # Get headers and validate
            headers = self._extract_headers(sheet, delimiter_rows[0])
            self._validate_headers(headers)
            
            # Extract and process transaction data
            data = self._extract_transactions(sheet, delimiter_rows[1], delimiter_rows[2])
            
            # Create and clean DataFrame
            df = self._create_dataframe(data, headers)
            
            # Export to CSV if path is provided
            if export_csv_path:
                df.to_csv(export_csv_path, index=False)
            
            return df
            
        except Exception as e:
            raise Exception(f"Error processing HDFC statement: {str(e)}")
    
    def _find_delimiters(self, sheet):
        """Find rows containing asterisk delimiters"""
        delimiter_rows = []
        for row_idx in range(sheet.nrows):
            row_values = [str(sheet.cell_value(row_idx, col_idx)).strip() 
                         for col_idx in range(sheet.ncols)]
            if any('*' * 5 in cell for cell in row_values):
                delimiter_rows.append(row_idx)
        return delimiter_rows
    
    def _extract_headers(self, sheet, delimiter_row):
        """Extract and return headers from the row after the delimiter"""
        header_row = delimiter_row + 1
        headers = [str(sheet.cell_value(header_row, col_idx)).strip() 
                  for col_idx in range(sheet.ncols)]
        return headers
    
    def _validate_headers(self, headers):
        """Validate that all expected columns are present"""
        missing_columns = set(self.expected_columns) - set(headers)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    def _extract_transactions(self, sheet, start_delimiter, end_delimiter):
        """Extract transaction data between delimiters"""
        data = []
        start_row = start_delimiter + 1
        end_row = end_delimiter
        
        for row_idx in range(start_row, end_row):
            row = [sheet.cell_value(row_idx, col_idx) 
                  for col_idx in range(sheet.ncols)]
            if any(str(cell).strip() for cell in row):
                data.append(row)
        
        return data
    
    def _create_dataframe(self, data, headers):
        """Create and clean DataFrame from transaction data"""
        df = pd.DataFrame(data, columns=headers)
        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')
        
        # Convert date columns
        for col in ['Date', 'Value Dt']:
            df[col] = pd.to_datetime(df[col], format='%d/%m/%y')
        
        # Convert amount columns
        amount_cols = ['Withdrawal Amt.', 'Deposit Amt.', 'Closing Balance']
        for col in amount_cols:
            df[col] = (df[col].astype(str)
                      .str.replace(',', '')
                      .str.replace('₹', '')
                      .str.strip())
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
