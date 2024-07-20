from eventregistry import *
import json

# Initialize EventRegistry with your API key
er = EventRegistry(apiKey="7f3e1d23-cead-4c5b-8a7b-5e47da1e9586")

# Define your query
q = QueryEvents(keywords="Copa America")
q.setRequestedResult(RequestEventsInfo(sortBy="date", count=50))   # request event details for latest 50 events

# Execute the query and get the results
results = er.execQuery(q)

# Define the file path where you want to save the results
file_path = "event_results.txt"

# Write the results to a text file
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)

print(f"Saved {len(results)} events to {file_path}")
