from petcare import app, mongo

# This script is a utility for performing one-off manual database tasks
# directly on your MongoDB database. It is not part of the main application flow.

# To use it, you would typically uncomment a command and run the file
# from your terminal.

with app.app_context():
    # Example: Create a new collection in MongoDB
    # mongo.db.create_collection("new_collection_name")

    print("Database utility script loaded. No automatic operations were performed.")