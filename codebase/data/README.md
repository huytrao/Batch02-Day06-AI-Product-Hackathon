# Data Format & Schema Notes

## Database: SQLite (`sample_data.sqlite`)

### Tables
1. **restaurants**
   - `id`: Primary Key
   - `name`: Name of the restaurant
   - `vendor`: Delivery partner (e.g., GrabFood, ShopeeFood)
   - `eta_history_json`: JSON string array of historical delivery times in minutes
   - `cuisine`: Type of food
   - `tags`: Comma-separated tags
   - `evidence_links`: Pipe-separated URLs for evidence/reviews
   - `location`: Delivery zone (e.g., Ocean Park 1)

2. **eta_logs**
   - `id`: Primary Key
   - `restaurant_id`: Foreign key to `restaurants.id`
   - `logged_at`: Timestamp
   - `eta`: Delivery time in minutes

3. **feedback_submissions**
   - `id`: Primary Key
   - `query`: User's original query
   - `suggestion_id`: The ID of the suggested restaurant
   - `rating`: Star rating (1-5)
   - `feedback_text`: Optional text
   - `submitted_at`: Timestamp

## Importing Data
Run the following script from the root `codebase` directory:
```bash
python scripts/import_csv_to_sqlite.py
```