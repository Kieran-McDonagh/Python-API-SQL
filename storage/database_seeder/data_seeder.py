import sqlite3
import sys
from storage.database_seeder.data import (
    flights,
    pilots,
    destinations,
    flight_pilot_assignments,
)
from utils.utils import Utils as u


class DataSeeder:
    def __init__(self, db_storage):
        self.db_storage = db_storage

    # Check if each table exists and if there is date in the table.
    # If not, prompt the user to seed the database.
    # If the user chooses not to seed, exit the program.

    def check_for_data(self):
        if not self._check_table_has_data("pilots"):
            self._prompt_and_seed("pilot", self.seed_pilot_data)

        if not self._check_table_has_data("destinations"):
            self._prompt_and_seed("destination", self.seed_destination_data)

        if not self._check_table_has_data("flights"):
            self._prompt_and_seed("flight", self.seed_flight_data)

        if not self._check_table_has_data("flight_pilots"):
            self._prompt_and_seed(
                "flight pilot assignment", self.seed_flight_pilots_data
            )

    # Method to prompt the user to seed

    def _prompt_and_seed(self, label, seed_func):
        while True:
            user_input = u.prompt_text(
                f"No {label} data found, seed {label}s database? \n(Program will exit if no {label} data) (y/n)"
            )
            if user_input is None:
                print(f"Exiting program due to no {label} data")
                sys.exit(0)

            if user_input == "y":
                seed_func()
                break
            elif user_input == "n":
                print(f"Exiting program due to no {label} data")
                sys.exit(0)
            else:
                print("Invalid input. Please type 'y' or 'n'")

    # Checks if the table exists, and if it has any data.

    def _check_table_has_data(self, table_name):
        try:
            with sqlite3.connect(self.db_storage) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{table_name}'"
                )
                if cursor.fetchone()[0] == 0:
                    return False

                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                return count > 0
        except sqlite3.Error as e:
            print(f"Error checking data in {table_name}: {e}")
            return False

    # Methods for seeding pilots, destinations, flights, flight_pilots tables.

    def seed_pilot_data(self):
        try:
            with sqlite3.connect(self.db_storage) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS pilots (
                        pilot_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        pilot_name TEXT NOT NULL,
                        is_deleted BOOLEAN NOT NULL DEFAULT 0
                    );
                    """
                )

                pilot_data = [
                    (
                        entry["pilot_id"],
                        entry["name"],
                    )
                    for entry in pilots.values()
                ]

                cursor.executemany(
                    "INSERT OR IGNORE INTO pilots (pilot_id, pilot_name) VALUES (?, ?);",
                    pilot_data,
                )

                print("Seeded pilot data successfully.")

        except sqlite3.Error as e:
            print(f"Error seeding pilot data: {e}")
            sys.exit(0)

    def seed_destination_data(self):
        try:
            with sqlite3.connect(self.db_storage) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS destinations (
                        destination_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        destination_name TEXT NOT NULL UNIQUE,
                        is_deleted BOOLEAN NOT NULL DEFAULT 0
                    );
                    """
                )

                destination_data = [
                    (
                        entry["destination_id"],
                        entry["destination_name"],
                    )
                    for entry in destinations.values()
                ]

                cursor.executemany(
                    "INSERT OR IGNORE INTO destinations (destination_id, destination_name) VALUES (?, ?);",
                    destination_data,
                )

                print("Seeded destination data successfully.")

        except sqlite3.Error as e:
            print(f"Error seeding destination data: {e}")
            sys.exit(0)

    def seed_flight_data(self):
        try:
            with sqlite3.connect(self.db_storage) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS flights (
                        flight_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        departure_date TEXT NOT NULL,
                        departure_time TEXT NOT NULL,
                        status TEXT NOT NULL CHECK(
                        status IN ('scheduled', 'on time', 'delayed', 'cancelled', 'arrived', 'completed')
                        ),
                        is_deleted BOOLEAN NOT NULL DEFAULT 0,
                        destination_id INTEGER,
                        FOREIGN KEY (destination_id)
                            REFERENCES destinations(destination_id)
                    );
                    """
                )

                flight_data = [
                    (
                        entry["flight_id"],
                        entry["departure_date"],
                        entry["departure_time"],
                        entry["status"],
                        entry["destination_id"],
                    )
                    for entry in flights.values()
                ]

                cursor.executemany(
                    "INSERT OR IGNORE INTO flights (flight_id, departure_date, departure_time, status, destination_id) VALUES (?, ?, ?, ?, ?);",
                    flight_data,
                )

                print("Seeded flight data successfully.")

        except sqlite3.Error as e:
            print(f"Error seeding flight data: {e}")
            sys.exit(0)

    def seed_flight_pilots_data(self):
        try:
            with sqlite3.connect(self.db_storage) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS flight_pilots (
                        flight_id INTEGER,
                        pilot_id INTEGER,
                        PRIMARY KEY (flight_id, pilot_id),
                        FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
                        FOREIGN KEY (pilot_id) REFERENCES pilots(pilot_id)
                    );
                    """
                )

                flight_pilot_data = [
                    (entry["flight_id"], entry["pilot_id"])
                    for entry in flight_pilot_assignments.values()
                ]

                cursor.executemany(
                    "INSERT OR IGNORE INTO flight_pilots (flight_id, pilot_id) VALUES (?, ?);",
                    flight_pilot_data,
                )

                print("Seeded flight pilot data successfully.")

        except sqlite3.Error as e:
            print(f"Error seeding flight pilots data: {e}")
            sys.exit(0)
