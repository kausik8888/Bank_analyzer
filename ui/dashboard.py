import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

class DashboardUI:
    def __init__(self):
        st.set_page_config(page_title="Bank Statement Analyzer", layout="wide")
    
    def render_header(self):
        """Render the dashboard header"""
        st.title("Bank Statement Analyzer")
    
    def render_bank_selector(self, supported_banks):
        """Render bank selection dropdown"""
        return st.selectbox(
            "Select your bank",
            options=list(supported_banks.keys()),
            index=0
        )
    
    def render_file_upload(self):
        """Render file upload widget"""
        return st.file_uploader("Upload your bank statement (XLS format)", type=['xls'])
    
    def render_summary(self, summary):
        """Render transaction summary"""
        st.subheader("Transaction Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"Total Transactions: {summary['total_transactions']}")
            st.write(
                f"Date Range: {summary['date_range'][0].strftime('%Y-%m-%d')} to "
                f"{summary['date_range'][1].strftime('%Y-%m-%d')}"
            )
        
        with col2:
            st.write(f"Total Withdrawals: ₹{summary['total_withdrawals']:,.2f}")
            st.write(f"Total Deposits: ₹{summary['total_deposits']:,.2f}")
            st.write(f"Current Balance: ₹{summary['final_balance']:,.2f}")
    
    def render_charts(self, analyzer, monthly_analysis, balance_trend):
        """Render analysis charts"""
        """if df is not None and not df.empty:
            user_txn_counts = df['upi_transaction_name'].value_counts()
            frequent_users_mask = df['upi_transaction_name'].isin(user_txn_counts[user_txn_counts > 5].index)
            df_filtered= df[(frequent_users_mask) & ((df['Withdrawal Amt.'] > 1000) | (df['Deposit Amt.'] > 1000))]
            df=df_filtered
        st.subheader("Transaction Analysis")"""
        
        col1, col2, col3= st.columns(3)
        
        with col1:
            fig = analyzer.create_withdrawal_chart(monthly_analysis['withdrawals'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = analyzer.create_deposit_chart(monthly_analysis['deposits'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            fig = analyzer.create_balance_chart(balance_trend)
            st.plotly_chart(fig, use_container_width=True)
       
             
    
    def render_transaction_details(self, df):
        """Render transaction details table"""
        st.subheader("Transaction Details")
        # Display the main transaction table
        st.subheader("All Transactions")
        st.dataframe(df)
            
            # Add CSV download button
        csv = df.to_csv(index=False)
        st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="bank_statement_analysis.csv",
                mime="text/csv"
            )
        
        if df is not None and not df.empty:
            # Use upi_transaction_name column as provided by TransactionAnalyzer
            user_txn_counts = df['upi_transaction_name'].value_counts()
            frequent_users = user_txn_counts[user_txn_counts > 3].index.tolist()
            
            # Calculate total amounts for each UPI transaction name
            user_amounts = df.groupby('upi_transaction_name').agg({
                'Withdrawal Amt.': 'sum',
                'Deposit Amt.': 'sum'
            }).reset_index()
            
            # Filter users based on amount condition
            amount_filter = (user_amounts['Withdrawal Amt.'] < 1000) | (user_amounts['Deposit Amt.'] > 1000)
            eligible_users = user_amounts[amount_filter]['upi_transaction_name'].tolist()
            
            # Get final list of eligible users (frequent and within amount limit)
            final_eligible_users = [user for user in frequent_users if user in eligible_users and user is not None]
            
            if final_eligible_users:
                st.subheader("UPI Transaction Analysis")
                
                # Create multiselect for users
                selected_users = st.multiselect(
                    "Select UPI Transaction Names",
                    options=final_eligible_users,
                    default=final_eligible_users[:2] if len(final_eligible_users) > 2 else final_eligible_users
                )
                
                # Add a generate chart button
                if st.button("Generate Pie Chart"):
                    if selected_users:
                        # Create figure and subplot
                        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 5),facecolor='#5b5459')
                        
                        # Filter data for selected users
                        filtered_data = df[df['upi_transaction_name'].isin(selected_users)]
                        
                        # Prepare data for withdrawals pie chart
                        withdrawals = filtered_data.groupby('upi_transaction_name')['Withdrawal Amt.'].sum()
                        deposits = filtered_data.groupby('upi_transaction_name')['Deposit Amt.'].sum()
                        
                        ax1.axis('equal')
                        ax2.axis('equal')
                        # Set background color to transparent
                        ax1.set_facecolor('none')
                        ax2.set_facecolor('none')
                        # Plot withdrawals pie chart
                        ax1.pie(withdrawals, labels=withdrawals.index, shadow=False, autopct='%1.1f%%')
                        ax1.set_title('Withdrawal Distribution')
                        
                        # Plot deposits pie chart
                        ax2.pie(deposits, labels=deposits.index, shadow=False, autopct='%1.1f%%')
                        ax2.set_title('Deposit Distribution')
                        
                        # Adjust layout and display
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                        # Display transaction statistics
                        st.subheader("Transaction Statistics")
                        stats_col1, stats_col2 = st.columns(2)
                        
                        with stats_col1:
                            st.write("Withdrawal Statistics:")
                            st.write(pd.DataFrame({
                                'Total Amount': withdrawals,
                                'Transaction Count': filtered_data[filtered_data['Withdrawal Amt.'] > 0].groupby('upi_transaction_name').size()
                            }))
                        
                        with stats_col2:
                            st.write("Deposit Statistics:")
                            st.write(pd.DataFrame({
                                'Total Amount': deposits,
                                'Transaction Count': filtered_data[filtered_data['Deposit Amt.'] > 0].groupby('upi_transaction_name').size()
                            }))
            
           

