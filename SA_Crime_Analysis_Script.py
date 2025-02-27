import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "data-sa-crime-2023-24-full-fy.csv"
df = pd.read_csv(file_path)

# Convert 'Reported Date' to datetime format
df["Reported Date"] = pd.to_datetime(df["Reported Date"], format="%d/%m/%Y")

# Extract month-year for trend analysis
df["Month"] = df["Reported Date"].dt.to_period("M")

# Crime Trends Over Time
crime_trends = df.groupby("Month")["Offence count"].sum().reset_index()
crime_trends["Month"] = crime_trends["Month"].astype(str)
crime_trends["Month"] = pd.to_datetime(crime_trends["Month"])

plt.figure(figsize=(12, 5))
sns.lineplot(x="Month", y="Offence count", data=crime_trends, marker="o", color="red")
plt.title("Monthly Crime Trends in SA (2023-24)")
plt.xlabel("Month")
plt.ylabel("Total Crimes")
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Crime by Location
# Remove "Not Disclosed" and "Adelaide" category
df_filtered = df[(df["Suburb - Incident"].str.lower() != "not disclosed") & 
                 (df["Suburb - Incident"].str.lower() != "adelaide")]

# Top 10 crime-affected suburbs
top_crime_suburbs = df_filtered.groupby("Suburb - Incident")["Offence count"].sum().reset_index()
top_crime_suburbs = top_crime_suburbs.sort_values(by="Offence count", ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(y=top_crime_suburbs["Suburb - Incident"], x=top_crime_suburbs["Offence count"], palette="Reds_r")
plt.title("Top 10 Crime-Affected Suburbs in SA (2023-24)")
plt.xlabel("Total Crimes")
plt.ylabel("Suburb")
plt.show()

# Crime Type Analysis
top_crime_types = df.groupby("Offence Level 1 Description")["Offence count"].sum().reset_index()
top_crime_types = top_crime_types.sort_values(by="Offence count", ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(y=top_crime_types["Offence Level 1 Description"], x=top_crime_types["Offence count"], palette="Blues_r")
plt.title("Most Common Crime Types in SA (2023-24)")
plt.xlabel("Total Crimes")
plt.ylabel("Crime Category")
plt.show()

# Crime Distribution by Day of the Week
df["Day of Week"] = df["Reported Date"].dt.day_name()
crime_by_day = df.groupby("Day of Week")["Offence count"].sum().reset_index()
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
crime_by_day["Day of Week"] = pd.Categorical(crime_by_day["Day of Week"], categories=day_order, ordered=True)

plt.figure(figsize=(10, 5))
sns.barplot(x="Day of Week", y="Offence count", data=crime_by_day, palette="coolwarm")
plt.title("Crime Distribution by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Total Crimes")
plt.show()
