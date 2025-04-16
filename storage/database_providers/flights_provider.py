import sqlite3


class FlightsProvider:
    def __init__(self, db_storage):
        self.db_storage = db_storage

    # Provider that interacts with the database to perform CRUD operations related to flight queries.

    # CREATE

    # Used to insert new flight.
    # Returns string or None.

    def create_flight(
        self, departure_date, departure_time, destination_id, pilot_ids, status
    ):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")

                if status not in ["scheduled"]:
                    print("Failed to create flight")
                    return

                cur.execute(
                    """
                    INSERT INTO flights 
                    (departure_date, departure_time, destination_id, status) 
                    VALUES(?, ?, ?, ?);""",
                    (
                        departure_date,
                        departure_time,
                        destination_id,
                        status,
                    ),
                )

                flight_id = cur.lastrowid

                cur.executemany(
                    "INSERT INTO flight_pilots (flight_id, pilot_id) VALUES (?, ?);",
                    [(flight_id, pilot_id) for pilot_id in pilot_ids],
                )
                return f"Flight {flight_id} created with {len(pilot_ids)} pilot(s)."

        except sqlite3.Error as e:
            print(f"Error creating flight: {e}")
            return None

    # READ

    # Used to fetch all flights.
    # Returns rows or None.

    def get_all_flights(self):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """
                    SELECT flights.flight_id, destinations.destination_name, flights.departure_date, flights.departure_time, flights.status
                    FROM flights
                    JOIN destinations
                    ON flights.destination_id = destinations.destination_id
                    WHERE flights.is_deleted = FALSE;
                    """
                )
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print("Error retrieving flights information: ", e)
            return None

    # Fetch single flight by flight ID.
    # Returns row or None.

    def get_flight_by_id(self, flight_id):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """
                    SELECT flights.flight_id, destinations.destination_name, flights.departure_date, flights.departure_time, flights.status
                    FROM flights
                    JOIN destinations
                    ON flights.destination_id = destinations.destination_id
                    WHERE flights.flight_id = ? AND flights.is_deleted = FALSE;
                    """,
                    (flight_id,),
                )
                row = cur.fetchone()
                return [row] if row else None

        except sqlite3.Error as e:
            print("Error retrieving flight information: ", e)
            return None

    # Fetch all flights by destination ID.
    # Returns rows or None.

    def get_flights_by_destination_id(self, destination_id):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """
                    SELECT flights.flight_id, destinations.destination_name, flights.departure_date, flights.departure_time, flights.status
                    FROM flights
                    JOIN destinations
                    ON flights.destination_id = destinations.destination_id
                    WHERE destinations.destination_id = ? AND flights.is_deleted = FALSE;
                    """,
                    (destination_id,),
                )
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print("Error retrieving information: ", e)
            return None

    # Fetch count of flights by destination ID.
    # If completed is true return count for all completed flights else
    # return count for active flights.
    # Returns int or None

    def get_flight_count_by_destination_id(self, destination_id, completed):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")

                status_condition = "=" if completed else "!="
                query = f"""
                    SELECT COUNT(*) FROM flights
                    WHERE destination_id = ? 
                    AND status {status_condition} 'completed'
                    AND is_deleted = FALSE;
                """
                cur.execute(query, (destination_id,))
                count = cur.fetchone()[0]
                return count if count > 0 else None

        except sqlite3.Error as e:
            print("Error retrieving information: ", e)
            return None

    # Fetch all flights by status.
    # Returns rows or None.

    def get_flights_by_status(self, status):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """
                    SELECT flights.flight_id, destinations.destination_name, flights.departure_date, flights.departure_time, flights.status
                    FROM flights
                    JOIN destinations
                    ON flights.destination_id = destinations.destination_id
                    WHERE flights.status = ? AND flights.is_deleted = FALSE;
                    """,
                    (status,),
                )
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print("Error retrieving information: ", e)
            return None

    # Fetch all flights by pilot ID.
    # Returns rows or None.

    def get_flights_by_pilot(self, pilot_id):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """
                    SELECT flights.flight_id, destinations.destination_name, flights.departure_date, flights.departure_time, flights.status
                    FROM flight_pilots
                    JOIN flights ON flight_pilots.flight_id = flights.flight_id
                    JOIN destinations ON flights.destination_id = destinations.destination_id
                    WHERE flight_pilots.pilot_id = ? AND flights.is_deleted = FALSE;
                    """,
                    (pilot_id,),
                )
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print(f"Error retrieving flights for pilot: {e}")
            return None

    # Fetch count of flights by pilot ID.
    # If completed is true return count for all completed flights else
    # return count for active flights.
    # Returns int or None

    def get_flight_count_by_pilot(self, pilot_id, completed):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")

                status_condition = "=" if completed else "!="
                query = f"""
                    SELECT COUNT(*) FROM flight_pilots
                    JOIN flights ON flight_pilots.flight_id = flights.flight_id
                    WHERE flight_pilots.pilot_id = ?
                    AND flights.status {status_condition} 'completed'
                    AND flights.is_deleted = FALSE;
                """
                cur.execute(query, (pilot_id,))
                count = cur.fetchone()[0]
                return count if count > 0 else None

        except sqlite3.Error as e:
            print(f"Error retrieving flight count for pilot: {e}")
            return None

    # Fetch the pilots for a flight by flight ID.
    # Returns rows or None.

    def get_pilots_by_flight_id(self, flight_id):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """
                    SELECT pilots.pilot_id, pilots.pilot_name 
                    FROM flight_pilots
                    JOIN pilots ON pilots.pilot_id = flight_pilots.pilot_id
                    JOIN flights ON flights.flight_id = flight_pilots.flight_id
                    WHERE flight_pilots.flight_id = ? AND flights.is_deleted = FALSE;
                    """,
                    (flight_id,),
                )
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print("Error retrieving information: ", e)
            return None

    # Fetch all flights with no associated pilots.
    # Returns rows or None.

    def get_flights_with_no_pilots(self):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    """
                    SELECT flights.flight_id, destinations.destination_name, flights.departure_date, flights.departure_time, flights.status
                    FROM flights
                    LEFT JOIN flight_pilots ON flights.flight_id = flight_pilots.flight_id
                    JOIN destinations ON flights.destination_id = destinations.destination_id
                    WHERE flight_pilots.pilot_id IS NULL
                    AND flights.is_deleted = FALSE;
                    """
                )
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print("Error retrieving flights information: ", e)
            return None

    # Fetch all flights that match provided date range.
    # Map "on" to "=", "before" to "<", "after" to ">" for filtering.
    # Returns rows or None.

    def get_flights_for_departure_date(self, date_range, date):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")

                operator_map = {"on": "=", "before": "<", "after": ">"}

                operator = operator_map.get(date_range)
                if not operator:
                    print(
                        f"Invalid date range: '{date_range}'. Must be 'on', 'before', or 'after'."
                    )
                    return None

                query = f"""
                    SELECT flights.flight_id, destinations.destination_name, 
                        flights.departure_date, flights.departure_time, flights.status
                    FROM flights
                    JOIN destinations ON flights.destination_id = destinations.destination_id
                    WHERE flights.departure_date {operator} ?
                    AND flights.is_deleted = FALSE;
                """

                cur.execute(query, (date,))
                rows = cur.fetchall()
                return rows if rows else None

        except sqlite3.Error as e:
            print("Error retrieving information: ", e)
            return None

    # UPDATE

    # Update single field. Early return if field fails validation.
    # Returns string or None.

    def update_flight(self, flight_id, field_to_update, value):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")

                if field_to_update not in [
                    "departure_date",
                    "departure_time",
                    "status",
                    "destination_id",
                ]:
                    print("Failed to update flight")
                    return None

                if field_to_update == "status" and value not in [
                    "scheduled",
                    "on time",
                    "delayed",
                    "cancelled",
                    "arrived",
                    "completed",
                ]:
                    print("Failed to update flight")
                    return None

                query = f"UPDATE flights SET {field_to_update} = ? WHERE flight_id = ?"
                cur.execute(
                    query,
                    (
                        value,
                        flight_id,
                    ),
                )
                return "Flight updated"

        except sqlite3.Error as e:
            print(f"Error updating flight: {e}")
            return None

    # Updates 'flight_pilots' table. recieves list of pilot IDs.
    # Creates record for each pilot ID.
    # Returns string or None.

    def assign_pilots_to_flight(self, flight_id, pilot_ids):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.executemany(
                    "INSERT INTO flight_pilots (flight_id, pilot_id) VALUES (?, ?);",
                    [(flight_id, pilot_id) for pilot_id in pilot_ids],
                )
                return f"Assigned {len(pilot_ids)} new pilot(s) to flight {flight_id}"

        except sqlite3.Error as e:
            print(f"Error assigning pilots to flight: {e}")
            return None

    # Deletes records from 'flight_pilots' table. recieves list of pilot IDs.
    # Deleted record for each pilot ID.
    # Returns string or None.

    def remove_pilots_from_flight(self, flight_id, pilot_ids):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.executemany(
                    "DELETE FROM flight_pilots WHERE flight_id = ? AND pilot_id = ?;",
                    [(flight_id, pilot_id) for pilot_id in pilot_ids],
                )
                return f"{len(pilot_ids)} pilot(s) removed from flight {flight_id}"

        except sqlite3.Error as e:
            print(f"Error removing pilots from flight: {e}")
            return None

    # DELETE

    # Soft delete flight. Update the 'is_deleted' field to TRUE rather than
    # permanently delete record.
    # Returns string or None.

    def delete_flight(self, flight_id):
        try:
            with sqlite3.connect(self.db_storage) as con:
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute(
                    "UPDATE flights SET is_deleted = TRUE WHERE flight_id = ?;",
                    (flight_id,),
                )
                return "Flight marked as deleted"

        except sqlite3.Error as e:
            print(f"Error soft deleting flight: {e}")
            return None
