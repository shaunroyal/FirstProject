import pandas as pd
import os

def summarize_customers(path):
    df = pd.read_csv(os.path.join(path, 'customers.csv'))
    print('Customers.csv Summary:')
    print(df.describe(include='all'))
    print('\n')

def summarize_loans(path):
    df = pd.read_csv(os.path.join(path, 'loans.csv'))
    print('Loans.csv Summary:')
    print(df.describe(include='all'))
    print('Loan Status Counts:')
    print(df['status'].value_counts())
    print('\n')

def summarize_payments(path):
    df = pd.read_csv(os.path.join(path, 'payments.csv'))
    print('Payments.csv Summary:')
    print(df.describe(include='all'))
    print('\n')

def summarize_applications(path):
    df = pd.read_csv(os.path.join(path, 'applications.csv'))
    print('Applications.csv Summary:')
    print(df.describe(include='all'))
    print('Application Status Counts:')
    print(df['status'].value_counts())
    print('\n')

def main():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    summarize_customers(data_path)
    summarize_loans(data_path)
    summarize_payments(data_path)
    summarize_applications(data_path)

if __name__ == "__main__":
    main()
