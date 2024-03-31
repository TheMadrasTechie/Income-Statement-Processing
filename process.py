import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV file into a DataFrame
file_name = "2023 - 24 Income Statement.csv"
df = pd.read_csv(file_name)

# Selecting required columns
df = df[['Date', 'Client', 'Actual Amount', 'Bank Account']]

# Convert 'Date' column to datetime format (assuming DD-MM-YYYY format)
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

# Extracting month and year from the date
df['Month'] = df['Date'].dt.strftime('%b-%y')

# Group by 'Client' and sum 'Actual Amount' for each client
client_total = df.groupby('Client')['Actual Amount'].sum().reset_index()

# Group by 'Bank Account' and sum 'Actual Amount' for each account
account_total = df.groupby('Bank Account')['Actual Amount'].sum().reset_index()

# Combine specific clients into 'Others'
clients_to_combine = ['Pradeep', 'IT-Tax-returns', 'Divakar']
others_total = client_total[client_total['Client'].isin(clients_to_combine)]
others_total = pd.DataFrame([['Others', others_total['Actual Amount'].sum()]], columns=['Client', 'Actual Amount'])
client_total = client_total[~client_total['Client'].isin(clients_to_combine)]
client_total = pd.concat([client_total, others_total])

# Combine specific bank accounts into 'Others'
accounts_to_combine = ['ABC Bank', 'XYZ Bank']  # Add bank accounts to be combined here
others_account_total = account_total[account_total['Bank Account'].isin(accounts_to_combine)]
others_account_total = pd.DataFrame([['Others', others_account_total['Actual Amount'].sum()]], columns=['Bank Account', 'Actual Amount'])
account_total = account_total[~account_total['Bank Account'].isin(accounts_to_combine)]
account_total = pd.concat([account_total, others_account_total])

# Create a directory to store graphs and summary tables
folder_name = os.path.splitext(file_name)[0]
os.makedirs(folder_name, exist_ok=True)

# Plot and save bar chart for total income by client
plt.figure(figsize=(10, 6))
plt.bar(client_total['Client'], client_total['Actual Amount'], color='skyblue')
plt.title('Total Income by Client')
plt.xlabel('Client')
plt.ylabel('Total Income (USD)')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i, v in enumerate(client_total['Actual Amount']):
    plt.text(i, v + 500, f"Rs. {v:,.0f}", ha='center', va='bottom')
plt.tight_layout()
plt.savefig(f"{folder_name}/Total_Income_by_Client_Bar.png")
plt.close()

# Plot and save pie chart for total income by client
plt.figure(figsize=(8, 8))
explode = [0.1] * len(client_total)
plt.pie(client_total['Actual Amount'], labels=client_total['Client'], autopct='%1.1f%%', startangle=140, explode=explode,
        colors=plt.cm.Paired.colors)
plt.title('Total Income Distribution by Client')
plt.axis('equal')
plt.tight_layout()
plt.savefig(f"{folder_name}/Income_Distribution_by_Client_Pie.png")
plt.close()

# Plot and save bar chart for total income by bank account
plt.figure(figsize=(10, 6))
plt.bar(account_total['Bank Account'], account_total['Actual Amount'], color='lightgreen')
plt.title('Total Income by Bank Account')
plt.xlabel('Bank Account')
plt.ylabel('Total Income (USD)')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i, v in enumerate(account_total['Actual Amount']):
    plt.text(i, v + 500, f"Rs. {v:,.0f}", ha='center', va='bottom')
plt.tight_layout()
plt.savefig(f"{folder_name}/Total_Income_by_Bank_Account_Bar.png")
plt.close()

# Plot and save pie chart for total income by bank account
plt.figure(figsize=(8, 8))
explode = [0.1] * len(account_total)
plt.pie(account_total['Actual Amount'], labels=account_total['Bank Account'], autopct='%1.1f%%', startangle=140,
        explode=explode, colors=plt.cm.Paired.colors)
plt.title('Total Income Distribution by Bank Account')
plt.axis('equal')
plt.tight_layout()
plt.savefig(f"{folder_name}/Income_Distribution_by_Bank_Account_Pie.png")
plt.close()

# Group by 'Month' and sum 'Actual Amount' for each month
monthly_total = df.groupby('Month')['Actual Amount'].sum().reset_index()

# Plot and save pie chart for total income by month
plt.figure(figsize=(8, 8))
explode = [0.1] * len(monthly_total)
plt.pie(monthly_total['Actual Amount'], labels=monthly_total['Month'], autopct='%1.1f%%', startangle=140, explode=explode,
        colors=plt.cm.Paired.colors)
plt.title('Total Income Distribution by Month')
plt.axis('equal')
plt.tight_layout()
plt.savefig(f"{folder_name}/Income_Distribution_by_Month_Pie.png")
plt.close()

# Group by 'Month' and 'Client' and sum 'Actual Amount' for each month and client
monthly_client_total = df.groupby(['Month', 'Client'])['Actual Amount'].sum().unstack(fill_value=0)

# Plot and save bar graph for total income by month and client from APR 2023 to MAR 2024
plt.figure(figsize=(12, 8))
months_order = pd.date_range(start='2023-04-01', end='2024-03-01', freq='MS').strftime('%b-%y')
for client in monthly_client_total.columns:
    plt.bar(monthly_client_total.index, monthly_client_total[client], label=client)
plt.title('Total Income by Month and Client')
plt.xlabel('Month')
plt.ylabel('Total Income (USD)')
plt.xticks(months_order, rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(f"{folder_name}/Total_Income_by_Month_and_Client_Bar.png")
plt.close()

# Group by 'Month' and 'Bank Account' and sum 'Actual Amount' for each month and account
monthly_account_total = df.groupby(['Month', 'Bank Account'])['Actual Amount'].sum().unstack(fill_value=0)

# Plot and save bar graph for total income by month and bank account from APR 2023 to MAR 2024
plt.figure(figsize=(12, 8))
for account in monthly_account_total.columns:
    plt.bar(monthly_account_total.index, monthly_account_total[account], label=account)
plt.title('Total Income by Month and Bank Account')
plt.xlabel('Month')
plt.ylabel('Total Income (USD)')
plt.xticks(months_order, rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(f"{folder_name}/Total_Income_by_Month_and_Bank_Account_Bar.png")
plt.close()

# Plot and save line graph for total income by bank account
monthly_client_total = df.groupby(['Month', 'Client'])['Actual Amount'].sum().unstack(fill_value=0)
monthly_client_total = monthly_client_total.reindex(pd.date_range(start='2023-04-01', end='2024-03-01', freq='MS').strftime('%b-%y'), fill_value=0)

# Plot and save line graph for total income by client from APR 2023 to MAR 2024
plt.figure(figsize=(12, 8))

for client in monthly_client_total.columns:
    plt.plot(monthly_client_total.index, monthly_client_total[client], marker='o', label=client)
plt.title('Total Income by Client')
plt.xlabel('Month')
plt.ylabel('Total Income (USD)')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(f"{folder_name}/Total_Income_by_Client_Line.png")
plt.close()

# Group by 'Month' and 'Bank Account' and sum 'Actual Amount' for each month and account
monthly_account_total = df.groupby(['Month', 'Bank Account'])['Actual Amount'].sum().unstack(fill_value=0)
monthly_account_total = monthly_account_total.reindex(pd.date_range(start='2023-04-01', end='2024-03-01', freq='MS').strftime('%b-%y'), fill_value=0)

# Plot and save line graph for total income by bank account from APR 2023 to MAR 2024
plt.figure(figsize=(12, 8))
for account in monthly_account_total.columns:
    plt.plot(monthly_account_total.index, monthly_account_total[account], marker='o', label=account)
plt.title('Total Income by Bank Account')
plt.xlabel('Month')
plt.ylabel('Total Income (USD)')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(f"{folder_name}/Total_Income_by_Bank_Account_Line.png")
plt.close()


# Create summary tables and save to CSV files
client_total.to_csv(f"{folder_name}/Summary_Total_Income_by_Client.csv", index=False)
account_total.to_csv(f"{folder_name}/Summary_Total_Income_by_Bank_Account.csv", index=False)
monthly_total.to_csv(f"{folder_name}/Summary_Total_Income_by_Month.csv", index=False)
