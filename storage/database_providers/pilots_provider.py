import sqlite3


class PilotsProvider:
    def __init__(self, db_storage):
        self.db_storage = db_storage

    # Provider that interacts with the database to perform CRUD operations related to pilot queries.

    # CREATE

    # Used to insert new pilot.
    # Returns string or None.

    def create_pilot(self, pilot_name):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute("INSERT INTO pilots (pilot_name) VALUES(?);", (pilot_name,))
                return "Pilot created"

        except sqlite3.Error as e:
            print(f"Error creating pilot: {e}")
            return None

    # READ

    # Fetches all pilots.
    # Returns rows or None.

    def get_all_pilots(self):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    "SELECT pilot_id, pilot_name FROM pilots WHERE is_deleted = FALSE;"
                )
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print(f"Error retrieving pilot information: {e}")
            return None

    # Fetch single pilot by ID.
    # Returns row or None.

    def get_pilot_by_id(self, pilot_id):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    "SELECT pilot_id, pilot_name FROM pilots WHERE pilot_id = ? AND is_deleted = FALSE;",
                    (pilot_id,),
                )
                row = cur.fetchone()
                return [row] if row else None

        except sqlite3.Error as e:
            print(f"Error retrieving pilot information: {e}")
            return None

    # Fetch all pilots who are:
    #   Not marked as deleted.
    #   Not assigned to any non-completed flights.
    # Returns rows or None.

    def get_all_pilots_for_deletion(self):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute("""
                    SELECT pilot_id, pilot_name FROM pilots
                    WHERE is_deleted = FALSE
                    AND pilot_id NOT IN (
                        SELECT flight_pilots.pilot_id
                        FROM flight_pilots
                        JOIN flights 
                        ON flight_pilots.flight_id = flights.flight_id
                        WHERE flights.status != 'completed'
                    );
                """)
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print(f"Error retrieving deletable pilots: {e}")
            return None

    # Fetch all pilots who:
    #   Do not have a flight on the provided departure date.
    #   Are not already assigned to the provided flight.
    # Returns rows or None.

    def get_available_pilots_for_flight(self, flight_id, departure_date):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """
                    SELECT pilot_id, pilot_name FROM pilots
                    WHERE is_deleted = FALSE
                    AND pilot_id NOT IN (
                        SELECT pilot_id FROM flight_pilots WHERE flight_id = ?
                    )
                    AND pilot_id NOT IN (
                        SELECT flight_pilots.pilot_id
                        FROM flight_pilots
                        JOIN flights 
                        ON flight_pilots.flight_id = flights.flight_id
                        WHERE flights.departure_date = ?
                    );
                """,
                    (
                        flight_id,
                        departure_date,
                    ),
                )
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print(f"Error retrieving available pilots: {e}")
            return None

    # Fetch pilots who do not have a flight on the provided date.
    # Returns rows or None.

    def get_available_pilots_for_date(self, departure_date):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """
                    SELECT pilot_id, pilot_name FROM pilots
                    WHERE is_deleted = FALSE
                    AND pilot_id NOT IN (
                        SELECT flight_pilots.pilot_id
                        FROM flight_pilots
                        JOIN flights 
                        ON flight_pilots.flight_id = flights.flight_id
                        WHERE flights.departure_date = ?
                    );
                """,
                    (departure_date,),
                )
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print(f"Error retrieving available pilots: {e}")
            return None

    # UPDATE

    # Method to update pilot. Early return if validation fails.
    # Returns string or None.

    def update_pilot(self, pilot_id, field_to_update, value):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")

                if field_to_update not in ["pilot_name"]:
                    print("Failed to update pilot")
                    return None

                query = f"UPDATE pilots SET {field_to_update} = ? WHERE pilot_id = ?"
                cur.execute(query, (value, pilot_id))
                return "Pilot updated"

        except sqlite3.Error as e:
            print(f"Error updating pilot: {e}")
            return None

    # DELETE

    # Soft delete pilot. Update the 'is_deleted' field to TRUE rather than
    # permanently delete record.
    # Returns string or None.

    def delete_pilot_by_id(self, pilot_id):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    "UPDATE pilots SET is_deleted = TRUE WHERE pilot_id = ?;",
                    (pilot_id,),
                )
                return "Pilot marked as deleted"

        except sqlite3.Error as e:
            print(f"Error soft deleting pilot: {e}")
            return None
