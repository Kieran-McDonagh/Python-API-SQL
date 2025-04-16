import sqlite3


class DestinationsProvider:
    def __init__(self, db_storage):
        self.db_storage = db_storage

    # Provider that interacts with the database to perform CRUD operations related to destination queries.

    # CREATE

    # Create new destination.
    # Returns string or None.

    def create_destination(self, destination_name):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    "INSERT INTO destinations (destination_name) VALUES(?);",
                    (destination_name,),
                )
                return "Destination created"

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                print("A destination with that name already exists")
                return None

        except sqlite3.Error as e:
            print(f"Error creating destination: {e}")
            return None

    # READ

    # Fetch all destinations.
    # Returns rows or None.

    def get_all_destinations(self):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """SELECT destination_id, destination_name 
                    FROM destinations
                    WHERE is_deleted = FALSE;"""
                )
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print("Error retrieving destination information: ", e)
            return None

    # Fetch single destination by ID.
    # Returns row or None

    def get_destination_by_id(self, destination_id):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """
                    SELECT destination_id, destination_name FROM destinations
                    WHERE destination_id = ? AND is_deleted = FALSE;
                    """,
                    (destination_id,),
                )
                row = cur.fetchone()
                return [row] if row else None

        except sqlite3.Error as e:
            print("Error retrieving destination information: ", e)
            return None

    # Fetch single destination by name (unique).
    # Returns row or None

    def get_destination_by_name(self, destination_name):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """
                    SELECT destination_id, destination_name FROM destinations
                    WHERE destination_name = ? AND is_deleted = FALSE;
                    """,
                    (destination_name,),
                )
                row = cur.fetchone()
                return [row] if row else None

        except sqlite3.Error as e:
            print("Error retrieving destination information: ", e)
            return None

    # Fetch all destinatinations for deletion, where the destination
    # is not assigned to an active flight.
    # Returns rows or None.

    def get_all_destinations_for_deletion(self):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute("""
                    SELECT destination_id, destination_name FROM destinations
                    WHERE is_deleted = FALSE
                    AND destination_id NOT IN (
                        SELECT destination_id
                        FROM flights
                        WHERE status != 'completed'
                    );
                """)
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print(f"Error retrieving deletable destinations: {e}")
            return None

    # UPDATE

    # Update destination. Early return if field fails validation.
    # Returns string or None.

    def update_destination(self, destination_id, field_to_update, value):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")

                if field_to_update not in ["destination_name"]:
                    print("Failed to update destination")
                    return None

                query = f"UPDATE destinations SET {field_to_update} = ? WHERE destination_id = ?"
                cur.execute(query, (value, destination_id))
                return "Destination updated"

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                print("A destination with that name already exists")
                return None

        except sqlite3.Error as e:
            print(f"Error updating destination: {e}")
            return None

    # DELETE

    # Soft delete destination. Update the 'is_deleted' field to TRUE rather than
    # permanently delete record.
    # Returns string or None.

    def delete_destination(self, destination_id):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    "UPDATE destinations SET is_deleted = TRUE WHERE destination_id = ?;",
                    (destination_id,),
                )
                return "Destination marked as deleted"

        except sqlite3.Error as e:
            print(f"Error soft deleting destination: {e}")
            return None
