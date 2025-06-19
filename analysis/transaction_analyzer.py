import pandas as pd
import plotly.graph_objects as go

class TransactionAnalyzer:
    def analyze_transactions(self, df):
        """Analyze transaction data and return insights"""
        try:
            analysis = {
                'summary': self._get_summary(df),
                'monthly_analysis': self._get_monthly_analysis(df),
                'balance_trend': self._get_balance_trend(df)
            }
            return analysis
        except Exception as e:
            raise Exception(f"Error analyzing transactions: {str(e)}")
    
    def _get_summary(self, df):
        if df is not None and not df.empty:
            # Create UPI transaction name column
            df['upi_transaction_name'] = None  # Initialize with None
            
            # Extract UPI transaction names
            mask = df['Narration'].str.startswith('UPI-', na=False)
            df.loc[mask, 'upi_transaction_name'] = df.loc[mask, 'Narration'].apply(
                lambda x: x.split('-')[1] if len(x.split('-')) > 1 else None
            )
        """Get basic transaction summary""" 
        return {
            'total_transactions': len(df),
            'date_range': (df['Date'].min(), df['Date'].max()),
            'total_withdrawals': df['Withdrawal Amt.'].sum(),
            'total_deposits': df['Deposit Amt.'].sum(),
            'final_balance': df['Closing Balance'].iloc[-1]
        }
    
    def _get_monthly_analysis(self, df):
        """Get monthly transaction analysis"""
        monthly_df = df.copy()
        monthly_df['Month'] = monthly_df['Date'].dt.to_period('M')
        
        withdrawals = monthly_df.groupby('Month')['Withdrawal Amt.'].agg(['sum', 'count'])
        deposits = monthly_df.groupby('Month')['Deposit Amt.'].agg(['sum', 'count'])
        
        return {
            'withdrawals': withdrawals,
            'deposits': deposits
        }
    
    def _get_balance_trend(self, df):
        """Get balance trend data"""
        return df[['Date', 'Closing Balance']].copy()
    
    def create_withdrawal_chart(self, monthly_data):
        """Create withdrawal visualization"""
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly_data.index.astype(str),
            y=monthly_data['sum'],
            name='Total Withdrawal'
        ))
        fig.add_trace(go.Scatter(
            x=monthly_data.index.astype(str),
            y=monthly_data['count'],
            name='Number of Withdrawals',
            yaxis='y2'
        ))
        fig.update_layout(
            title="Monthly Withdrawals",
            yaxis_title="Amount (₹)",
            yaxis2=dict(title="Count", overlaying="y", side="right"),
            height=400
        )
        return fig
    
    def create_deposit_chart(self, monthly_data):
        """Create deposit visualization"""
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly_data.index.astype(str),
            y=monthly_data['sum'],
            name='Total Deposits'
        ))
        fig.add_trace(go.Scatter(
            x=monthly_data.index.astype(str),
            y=monthly_data['count'],
            name='Number of Deposits',
            yaxis='y2'
        ))
        fig.update_layout(
            title="Monthly Deposits",
            yaxis_title="Amount (₹)",
            yaxis2=dict(title="Count", overlaying="y", side="right"),
            height=400
        )
        return fig
    
    def create_balance_chart(self, balance_data):
        """Create balance trend visualization"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=balance_data['Date'],
            y=balance_data['Closing Balance'],
            mode='lines+markers',
            name='Balance'
        ))
        fig.update_layout(
            title="Balance Trend",
            yaxis_title="Amount (₹)",
            height=400
        )
        return fig
