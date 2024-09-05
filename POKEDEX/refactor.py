# Function to make names lowercase and combine with subname if available
def process_pokemon_names(row):
    name = row['name'].lower() if pd.notna(row['name']) else ''
    subname = row['subname'].lower().replace(' ', '-') if pd.notna(row['subname']) else ''

    # Combine name and subname with a hyphen if subname exists
    if subname:
        return f"{name}-{subname}"
    return name


# Apply the function to the DataFrame
df['processed_name'] = df.apply(process_pokemon_names, axis=1)

# Display the processed DataFrame to the user
import ace_tools as tools;

tools.display_dataframe_to_user(name="Processed Pokémon Data", dataframe=df)

# Show the first few rows to verify the transformation
df[['name', 'subname', 'processed_name']].head()
