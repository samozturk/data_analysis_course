import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df_wide = pd.read_csv('data.csv')

df_wide.head()

# Identify the columns to keep (id variables)
id_vars = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']

# Identify the columns to melt (value variables - the years)
# Filter out any non-year columns that might be present after the id_vars
value_vars = [col for col in df_wide.columns if col not in id_vars]

# Melt the DataFrame from wide to long format
df_long = pd.melt(df_wide,
                  id_vars=id_vars,
                  value_vars=value_vars,
                  var_name='Year',
                  value_name='GDP (current US$)')

# Convert 'Year' column to numeric (optional, but good practice)
# Errors='coerce' will turn any non-numeric years into NaN
df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')

# Drop rows where 'Year' could not be converted to numeric (if any)
df_long.dropna(subset=['Year'], inplace=True)

# Convert Year to integer type
df_long['Year'] = df_long['Year'].astype(int)

# Display the first few rows of the long format DataFrame
print("Original Wide DataFrame shape:", df_wide.shape)
print("Converted Long DataFrame shape:", df_long.shape)
print("\nFirst 5 rows of the long format DataFrame:")
print(df_long.head())

# Display the last few rows to see recent years
print("\nLast 5 rows of the long format DataFrame:")
print(df_long.tail())

# --- Exploratory Data Analysis ---

# Basic descriptive statistics for GDP
print("\nDescriptive Statistics for GDP (current US$):")
print(df_long['GDP (current US$)'].describe())

# Check for missing GDP values
missing_gdp_count = df_long['GDP (current US$)'].isnull().sum()
print(f"\nNumber of missing GDP values: {missing_gdp_count}")

# You can now save this long format DataFrame if needed
# df_long.to_csv('data_long_format.csv', index=False)

# --- Data Visualization ---

# --- Plot 1: Single Country Trend (Example: United States) ---
# (Keeping the previous plot code as an example, but commenting it out
#  to focus on the multi-country comparison below)
country_name_single = 'United States'
df_country_single = df_long[df_long['Country Name'] == country_name_single].copy()
df_country_single.dropna(subset=['GDP (current US$)'], inplace=True)
df_country_single.sort_values('Year', inplace=True)
plt.figure(figsize=(12, 6))
plt.plot(df_country_single['Year'], df_country_single['GDP (current US$)'], marker='o', linestyle='-')
plt.title(f'GDP (current US$) Trend for {country_name_single}')
plt.xlabel('Year')
plt.ylabel('GDP (current US$)')
plt.grid(True)
years_single = df_country_single['Year'].unique()
if len(years_single) > 10:
    plt.xticks(years_single[::5], rotation=45)
plt.tight_layout()
plt.show()


# --- Plot 2: Comparing GDP Trends of Multiple Countries ---
countries_to_compare = ['United States', 'China', 'Germany', 'Japan', 'India']
df_compare = df_long[df_long['Country Name'].isin(countries_to_compare)].copy()

# Drop rows with missing GDP values for the selected countries before plotting
df_compare.dropna(subset=['GDP (current US$)'], inplace=True)

# Sort by country and year for consistent plotting
df_compare.sort_values(['Country Name', 'Year'], inplace=True)

# Create the plot
plt.figure(figsize=(14, 7)) # Adjust figure size

# Plot GDP trend for each country
for country in countries_to_compare:
    df_subset = df_compare[df_compare['Country Name'] == country]
    plt.plot(df_subset['Year'], df_subset['GDP (current US$)'], marker='.', linestyle='-', label=country) # Smaller marker

# Add titles and labels
plt.title('GDP (current US$) Comparison for Selected Countries')
plt.xlabel('Year')
plt.ylabel('GDP (current US$)')
plt.legend() # Add legend to identify countries
plt.grid(True) # Add a grid

# Improve x-axis labels - find common range or use representative ticks
all_years = df_compare['Year'].unique()
all_years.sort()
if len(all_years) > 10:
     # Show fewer ticks if range is large, e.g., every 5 or 10 years
     tick_frequency = 5 if len(all_years) <= 60 else 10
     plt.xticks(all_years[::tick_frequency], rotation=45)
else:
    plt.xticks(rotation=45) # Rotate labels if fewer years

plt.tight_layout() # Adjust layout
plt.show() # Display the plot


# --- Plot 3: Bar Chart Comparison for the Most Recent Year ---

# Find the most recent year available for each country in the comparison set
latest_years = df_compare.loc[df_compare.groupby('Country Name')['Year'].idxmax()]

# Sort by GDP for better visualization
latest_years = latest_years.sort_values('GDP (current US$)', ascending=False)

# Create the bar chart
plt.figure(figsize=(12, 6))
plt.bar(latest_years['Country Name'], latest_years['GDP (current US$)'], color='skyblue')

# Add titles and labels
plt.title(f'GDP (current US$) Comparison for Selected Countries (Latest Available Year)')
plt.xlabel('Country')
plt.ylabel('GDP (current US$)')
plt.xticks(rotation=45, ha='right') # Rotate country names for readability
plt.grid(axis='y', linestyle='--') # Add horizontal grid lines

# Add value labels on top of bars (optional, can be cluttered)
# for index, value in enumerate(latest_years['GDP (current US$)']):
#     plt.text(index, value, f'{value:,.0f}', ha='center', va='bottom')

plt.tight_layout() # Adjust layout
plt.show() # Display the plot


# --- Plot 4: GDP Growth Rate Comparison ---

# Calculate Year-over-Year GDP Growth Rate (%)
# Ensure data is sorted by Country then Year for correct pct_change calculation
df_compare.sort_values(['Country Name', 'Year'], inplace=True)
# Calculate pct_change within each group (country)
df_compare['GDP Growth Rate (%)'] = df_compare.groupby('Country Name')['GDP (current US$)'].pct_change() * 100

# Create the growth rate plot
plt.figure(figsize=(14, 7))

# Plot growth rate for each country
for country in countries_to_compare:
    df_subset = df_compare[df_compare['Country Name'] == country]
    # Plotting without the first year (NaN growth rate)
    plt.plot(df_subset['Year'][1:], df_subset['GDP Growth Rate (%)'][1:], marker='.', linestyle='-', label=country)

# Add titles and labels
plt.title('Annual GDP Growth Rate (%) Comparison for Selected Countries')
plt.xlabel('Year')
plt.ylabel('GDP Growth Rate (%)')
plt.axhline(0, color='grey', linestyle='--', linewidth=0.8) # Add a line at 0% growth
plt.legend() # Add legend
plt.grid(True) # Add a grid

# Improve x-axis labels
# Using the same logic as Plot 2
if len(all_years) > 10:
     tick_frequency = 5 if len(all_years) <= 60 else 10
     plt.xticks(all_years[::tick_frequency], rotation=45)
else:
    plt.xticks(rotation=45)

plt.tight_layout() # Adjust layout
plt.show() # Display the plot


# --- Plot 5: Distribution of GDP Across All Countries (Most Recent Year) ---

# Find the most recent year in the entire dataset
latest_overall_year = df_long['Year'].max()

# Filter data for the most recent year
df_latest_year = df_long[df_long['Year'] == latest_overall_year].copy()

# Drop countries with missing GDP for that year
df_latest_year.dropna(subset=['GDP (current US$)'], inplace=True)

# Create the histogram
plt.figure(figsize=(12, 6))
# Using a logarithmic scale for the x-axis due to large GDP range
plt.hist(df_latest_year['GDP (current US$)'], bins=30, color='purple', log=False) # Plot counts on linear scale first
plt.title(f'Distribution of GDP (current US$) Across Countries in {latest_overall_year}')
plt.xlabel('GDP (current US$)')
plt.ylabel('Number of Countries')
plt.grid(axis='y', linestyle='--')

# Optional: Try with log scale on x-axis if distribution is heavily skewed
# plt.figure(figsize=(12, 6))
# plt.hist(df_latest_year['GDP (current US$)'], bins=30, color='purple', log=False) # Keep y linear
# plt.xscale('log') # Set x-axis to logarithmic scale
# plt.title(f'Distribution of GDP (current US$) Across Countries in {latest_overall_year} (Log Scale)')
# plt.xlabel('GDP (current US$) (Log Scale)')
# plt.ylabel('Number of Countries')
# plt.grid(axis='y', linestyle='--')


plt.tight_layout() # Adjust layout
plt.show() # Display the plot


# --- Plot 6: Box Plot of GDP Growth Rates for Selected Countries ---

# Prepare data for box plot - need growth rates per country
# Use df_compare which already has 'GDP Growth Rate (%)' calculated
# Drop NaN values which occur for the first year of data for each country
df_growth_box = df_compare.dropna(subset=['GDP Growth Rate (%)']).copy()

# Create the box plot
plt.figure(figsize=(12, 7))

# We need to group data by country to create the box plot correctly
# Matplotlib's boxplot can take a list of arrays/Series, one for each box
growth_data_to_plot = [df_growth_box[df_growth_box['Country Name'] == country]['GDP Growth Rate (%)']
                       for country in countries_to_compare]

plt.boxplot(growth_data_to_plot, labels=countries_to_compare, patch_artist=True, showfliers=False) # patch_artist for fill, showfliers=False to hide outliers for cleaner look

# Add titles and labels
plt.title('Distribution of Annual GDP Growth Rates (%) for Selected Countries (Full Period)')
plt.xlabel('Country')
plt.ylabel('GDP Growth Rate (%)')
plt.axhline(0, color='grey', linestyle='--', linewidth=0.8) # Line at 0% growth
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--')

plt.tight_layout() # Adjust layout
plt.show() # Display the plot
