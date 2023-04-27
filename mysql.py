import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="bidding_system"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Define a function to place a bid on an item
def place_bid(user_id, item_id, amount):
  # Get the current highest bid on the item
  query = "SELECT MAX(amount) FROM bids WHERE item_id = %s"
  values = (item_id,)
  cursor.execute(query, values)
  highest_bid = cursor.fetchone()[0]
  
  # Check if the bid amount is higher than the current highest bid
  if amount > highest_bid:
    # Insert the new bid into the database
    query = "INSERT INTO bids (item_id, user_id, amount) VALUES (%s, %s, %s)"
    values = (item_id, user_id, amount)
    cursor.execute(query, values)
    db.commit()
    print("Bid placed successfully")
  else:
    print("Bid amount must be higher than the current highest bid")

# Place a bid on an item
place_bid(1, 1, 100)

# Define a function to get all the bids placed by a user
def get_user_bids(user_id):
  query = "SELECT * FROM bids WHERE user_id = %s"
  values = (user_id,)
  cursor.execute(query, values)
  return cursor.fetchall()

# Get all the bids placed by a user
bids = get_user_bids(1)
print("Bids placed by user:")
for bid in bids:
  print("Item:", bid[1], "Amount:", bid[3])
