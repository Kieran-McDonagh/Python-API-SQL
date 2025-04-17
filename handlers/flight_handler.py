from tabulate import tabulate
from utils.utils import Utils as u


class FlightHandler:
    def __init__(self, flights_service, destination_service, pilot_service):
        self.flights_service = flights_service
        self.destination_service = destination_service
        self.pilot_service = pilot_service

    # Parent method to present user with initial CRUD options.

    def handle_flight_queries(self):
        options = {
            "Create Flights": self._handle_create_flights,
            "View Flights": self._handle_read_flights,
            "Update Flights": self._handle_update_flights,
            "Delete Flights": self._handle_delete_flight,
        }

        u.present_standard_options(options)

    # CREATE

    # Creates a new flight, accepts a destination ID, departure date,
    # departure time, and pilot IDs. Defaults status to 'scheduled'.

    def _handle_create_flights(self):
        all_destinations = self.destination_service.get_all_destinations()
        if all_destinations is None:
            print("No destination data")
            return

        selected_destination = u.select_from_records(
            "Choose a destination for new flight:", all_destinations
        )
        if selected_destination is None:
            return

        destination_id = selected_destination[0]

        date_input = u.prompt_text("Enter departure date (YYYY-MM-DD)")
        if date_input is None:
            return

        departure_date = u.parse_date(date_input)
        if departure_date is None:
            return

        time_input = u.prompt_text("Enter departure time (HH:MM)")
        if time_input is None:
            return

        departure_time = u.parse_time(time_input)
        if departure_time is None:
            return

        # Only display pilots that do not already have flights on the same departure date.

        available_pilots = self.pilot_service.get_available_pilots_for_date(
            departure_date
        )
        if available_pilots is None:
            print("No pilots available for date")
            return

        selected_pilots = u.prompt_checkbox(
            "Select from available pilots:", available_pilots
        )
        if selected_pilots is None:
            return

        pilot_ids = [pilot[0] for pilot in selected_pilots]

        status = "scheduled"

        result = self.flights_service.create_flight(
            departure_date, departure_time, destination_id, pilot_ids, status
        )
        if result is None:
            return

        print(result)

    # READ

    # Parent method for read queries.

    def _handle_read_flights(self):
        options = {
            "View all flights": self._view_all_flights,
            "View flights by ID": self._view_flight_by_id,
            "View flights by active destinations": self._view_flights_by_destination,
            "View flights by status": self._view_flights_by_status,
            "View flights by departure dates": self._view_flights_by_departure,
            "View flights by active pilots": self._view_flights_by_pilot,
            "View pilots for flights": self._view_pilots_for_flight,
            "View flights with no assigned pilots": self._view_flights_with_no_pilots,
        }

        u.present_standard_options(options)

    # Fetch all flights not marked as deleted.

    def _view_all_flights(self):
        result = self.flights_service.get_all_flights()
        if result is None:
            print("No flight data found")
            return

        table = tabulate(
            result,
            headers=[
                "Flight ID",
                "Destination",
                "Departure Date",
                "Departure Time",
                "Status",
            ],
            tablefmt="fancy_grid",
        )
        print(table)

    # Fetch single flight by flight ID.

    def _view_flight_by_id(self):
        flight_id = u.prompt_id("Enter flight ID")
        if flight_id is None:
            return

        result = self.flights_service.get_flight_by_id(flight_id)
        if result is None:
            print(f"No flight found with ID '{flight_id}'.")
            return

        table = tabulate(
            result,
            headers=[
                "Flight ID",
                "Destination",
                "Departure Date",
                "Departure Time",
                "Status",
            ],
            tablefmt="fancy_grid",
        )
        print(table)

    # Fetch single flight by destination ID.

    def _view_flights_by_destination(self):
        options = {
            "View number of flights for a destination": self._view_number_of_flights_for_destination,
            "View all flights for a destination": self._view_all_flights_for_destination,
        }

        u.present_standard_options(options)

    # Parent method for fetching flight count by destination.

    def _view_number_of_flights_for_destination(self):
        options = {
            "View number of completed flights for a destination": lambda: self._view_flight_count_for_destination(
                True
            ),
            "View number of active flights for a destination": lambda: self._view_flight_count_for_destination(
                False
            ),
        }

        u.present_standard_options(options)

    # Method for fetching the count of flights per destination,
    # allows for count by either completed or active flights.

    def _view_flight_count_for_destination(self, completed):
        destination_id, destination_name = self._select_destination_record()

        result = self.flights_service.get_flight_count_by_destination_id(
            destination_id, completed
        )
        if result is None:
            print(
                f"No {'completed' if completed else 'active'} flights found for '{destination_name}'"
            )
            return

        print(
            f"{result} {'completed' if completed else 'active'} flights found for {destination_name}"
        )

    # Fetch all flights for a destination, regardless of flight status.

    def _view_all_flights_for_destination(self):
        destination_id, destination_name = self._select_destination_record()

        result = self.flights_service.get_flights_by_destination_id(destination_id)
        if result is None:
            print(f"No flights found for '{destination_name}'")
            return

        table = tabulate(
            result,
            headers=[
                "Flight ID",
                "Destination",
                "Departure Date",
                "Departure Time",
                "Status",
            ],
            tablefmt="fancy_grid",
        )
        print(table)

    # Fetch all flights by status.

    def _view_flights_by_status(self):
        options = [
            "scheduled",
            "on time",
            "delayed",
            "cancelled",
            "arrived",
            "completed",
        ]

        status = u.prompt_select_from_list("Select status", options)
        if status is None:
            return

        result = self.flights_service.get_flights_by_status(status)
        if result is None:
            print(f"No flights found with status {status}")

        table = tabulate(
            result,
            headers=[
                "Flight ID",
                "Destination",
                "Departure Date",
                "Departure Time",
                "Status",
            ],
            tablefmt="fancy_grid",
        )
        print(table)

    # Parent method for fetching flights queried by pilots.

    def _view_flights_by_pilot(self):
        options = {
            "View number of flights for a pilot": self._view_number_of_flights_for_pilot,
            "View all flights for a pilot": self._view_all_flights_for_pilot,
        }

        u.present_standard_options(options)

    # Parent method to fetch flight count per pilot.

    def _view_number_of_flights_for_pilot(self):
        options = {
            "View number of completed flights for a pilot": lambda: self._view_flight_count_for_pilot(
                True
            ),
            "View number of active flights for a pilot": lambda: self._view_flight_count_for_pilot(
                False
            ),
        }

        u.present_standard_options(options)

    # Method to fetch flight count for pilot, by either completed or active flights.

    def _view_flight_count_for_pilot(self, completed):
        pilot_id, pilot_name = self._select_pilot_record()

        result = self.flights_service.get_flight_count_by_pilot(pilot_id, completed)
        if result is None:
            print(
                f"No {'completed' if completed else 'active'} flights found for {pilot_name}"
            )
            return

        print(
            f"{result} {'completed' if completed else 'active'} flights found for {pilot_name}"
        )

    # Fetch all the flights that a pilot is assigned to.

    def _view_all_flights_for_pilot(self):
        pilot_id, pilot_name = self._select_pilot_record()

        result = self.flights_service.get_flights_by_pilot(pilot_id)
        if result is None:
            print(f"No schedule found for {pilot_name}")
            return

        table = tabulate(
            result,
            headers=[
                "Flight ID",
                "Destination",
                "Departure Date",
                "Departure Time",
                "Status",
            ],
            tablefmt="fancy_grid",
        )
        print(table)

    # Parent method for fetching the pilots assigned to a flight.
    # Allows the user to search for a specific flight or select from all flights.

    def _view_pilots_for_flight(self):
        options = {
            "Search by flight ID": self._view_pilots_for_flight_by_id,
            "Select from all flights": self._view_pilots_for_flight_selection,
        }

        u.present_standard_options(options)

    # Search for flight by ID.

    def _view_pilots_for_flight_by_id(self):
        flight_id = u.prompt_id("Enter flight ID")
        if flight_id is None:
            return

        self._get_pilots_for_flight(flight_id)

    # Select from all flights.

    def _view_pilots_for_flight_selection(self):
        all_flights = self.flights_service.get_all_flights()
        if all_flights is None:
            print("No flights found")
            return

        selected_flight = u.select_flight_from_records(
            "Select flight:", all_flights
        )
        if selected_flight is None:
            return

        flight_id = selected_flight[0]

        self._get_pilots_for_flight(flight_id)

    # Parent method for fetching flights by departure date, passing down the date range.

    def _view_flights_by_departure(self):
        options = {
            "View all flights on specified date": lambda: self._get_flights_for_departure_date(
                "on"
            ),
            "View all flights before specified date": lambda: self._get_flights_for_departure_date(
                "before"
            ),
            "View all flights after specified date": lambda: self._get_flights_for_departure_date(
                "after"
            ),
        }

        u.present_standard_options(options)

    # Fetch flights on specific date, before a specific date or after specific date (exclusive).

    def _get_flights_for_departure_date(self, date_range):
        user_input = u.prompt_text("Enter departure date (YYYY-MM-DD)")
        if user_input is None:
            return

        date = u.parse_date(user_input)
        if date is None:
            return

        result = self.flights_service.get_flights_for_departure_date(date_range, date)
        if result is None:
            print(f"No flights {date_range} date {date}")
            return

        table = tabulate(
            result,
            headers=[
                "Flight ID",
                "Destination",
                "Departure Date",
                "Departure Time",
                "Status",
            ],
            tablefmt="fancy_grid",
        )
        print(table)

    # Fetch all flights with no associated pilots.

    def _view_flights_with_no_pilots(self):
        result = self.flights_service.get_flights_with_no_pilots()
        if result is None:
            print("No flights found without pilots")
            return

        table = tabulate(
            result,
            headers=[
                "Flight ID",
                "Destination",
                "Departure Date",
                "Departure Time",
                "Status",
            ],
            tablefmt="fancy_grid",
        )
        print(table)

    # UPDATE

    # Parent method for updating flights. Allows user to search for a flight
    # or select from all flights.

    def _handle_update_flights(self):
        options = {
            "Search for a flight to update": self._handle_update_flight_by_id,
            "View all flights to update": self._handle_find_all_and_update,
        }

        u.present_standard_options(options)

    # Search for a flight to update.

    def _handle_update_flight_by_id(self):
        flight_id = u.prompt_id("Enter flight ID")
        if flight_id is None:
            return

        flight = self.flights_service.get_flight_by_id(flight_id)
        if flight is None:
            print(f"No flight found with ID: '{flight_id}'")
            return

        flight_to_update = flight[0]

        self._confirm_update_flight(flight_to_update)

    # Select flight to update from all flights.

    def _handle_find_all_and_update(self):
        all_flights = self.flights_service.get_all_flights()
        if all_flights is None:
            print("No flights found")
            return

        selected_flight = u.select_flight_from_records("Select flight:", all_flights)
        if selected_flight is None:
            return

        self._confirm_update_flight(selected_flight)

    # Method to update flight destination.

    def _update_flight_destination(self, flight_id):
        all_destinations = self.destination_service.get_all_destinations()
        if all_destinations is None:
            print("No destination data")
            return

        selected_destination = u.select_from_records(
            "Choose a new destination:", all_destinations
        )
        if selected_destination is None:
            return

        destination_id = selected_destination[0]
        field_to_update = "destination_id"

        self._update_flight_field(flight_id, field_to_update, destination_id)

    # Method to update flight departure date.

    def _update_flight_departure_date(self, flight_id):
        date_input = u.prompt_text("Enter new departure date (YYYY-MM-DD)")
        if date_input is None:
            return

        departure_date = u.parse_date(date_input)
        if departure_date is None:
            return

        field_to_update = "departure_date"

        self._update_flight_field(flight_id, field_to_update, departure_date)

    # Method to update flight departure time.

    def _update_flight_departure_time(self, flight_id):
        time_input = u.prompt_text("Enter new departure time (HH:MM)")
        if time_input is None:
            return

        departure_time = u.parse_time(time_input)
        if departure_time is None:
            return

        field_to_update = "departure_time"

        self._update_flight_field(flight_id, field_to_update, departure_time)

    # Method to update flight status.

    def _update_flight_status(self, flight_id):
        options = [
            "scheduled",
            "on time",
            "delayed",
            "cancelled",
            "arrived",
            "completed",
        ]

        status = u.prompt_select_from_list("Select status:", options)
        if status is None:
            return

        field_to_update = "status"

        self._update_flight_field(flight_id, field_to_update, status)

    # Parent method to update flight pilots. Allows for addition or removal.

    def _update_flight_pilots(self, flight_id, departure_date):
        options = ["Assign pilots to flight"]

        # Only provide option to remove pilots if there is existing pilots.

        current_pilots = self.flights_service.get_pilots_for_flight(flight_id)
        if current_pilots is not None:
            options.append("Remove pilots from flight")

        selected_option = u.prompt_select_from_list("Select option:", options)
        if selected_option is None:
            return

        if selected_option == "Assign pilots to flight":
            return self._assign_pilots_to_flight(flight_id, departure_date)

        if selected_option == "Remove pilots from flight":
            return self._remove_pilots_from_flight(flight_id, current_pilots)

    # Method to remove pilots from flight.

    def _remove_pilots_from_flight(self, flight_id, current_pilots):
        pilot_ids = self._select_pilots_from_checkbox(current_pilots)
        if pilot_ids is None:
            return

        result = self.flights_service.remove_pilots_from_flight(flight_id, pilot_ids)
        if result is None:
            return

        print(result)

    # Method to assign pilots to flight. Only display pilots who are not
    # on existing flights with the same departure date as the current edited flight,
    # or who are not already on the flight.

    def _assign_pilots_to_flight(self, flight_id, departure_date):
        available_pilots = self.pilot_service.get_available_pilots_for_flight(
            flight_id, departure_date
        )
        if available_pilots is None:
            print("No pilots available for this assignment")
            return

        pilot_ids = self._select_pilots_from_checkbox(available_pilots)
        if pilot_ids is None:
            return

        result = self.flights_service.assign_pilots_to_flight(flight_id, pilot_ids)
        if result is None:
            return

        print(result)

    # DELETE

    # Parent method for soft deleting a flight. Flights are not permanently deleted
    # but instead marked as deleted by setting the 'is_deleted' boolean to TRUE.
    # Method allows users to search for flight to delete or select from all flights.

    def _handle_delete_flight(self):
        options = {
            "Search for a flight to delete": self._handle_delete_flight_by_id,
            "View all flights to delete": self._handle_find_all_and_delete,
        }

        u.present_standard_options(options)

    # Search for a flight to delete.

    def _handle_delete_flight_by_id(self):
        flight_id = u.prompt_id("Enter flight ID")
        if flight_id is None:
            return

        flight_to_delete = self.flights_service.get_flight_by_id(flight_id)
        if flight_to_delete is None:
            print(f"No flight found with ID: '{flight_id}'")
            return

        flight = flight_to_delete[0]

        self._confirm_delete_flight(flight)

    # Select flight to delete from all flights.

    def _handle_find_all_and_delete(self):
        all_flights = self.flights_service.get_all_flights()
        if all_flights is None:
            print("No flights found")
            return

        selected_flight = u.select_flight_from_records("Select flight:", all_flights)
        if selected_flight is None:
            return

        self._confirm_delete_flight(selected_flight)

    # Shared methods

    # Returns the destination ID and destination name from selected destination.

    def _select_destination_record(self):
        all_destinations = self.destination_service.get_all_destinations()
        if all_destinations is None:
            print("No destination data")
            return

        selected_destination = u.select_from_records(
            "Choose a destination:", all_destinations
        )
        if selected_destination is None:
            return

        destination_id = selected_destination[0]
        destination_name = selected_destination[1]

        return destination_id, destination_name

    # Returns the pilot ID and pilot name from selected pilot.

    def _select_pilot_record(self):
        all_pilots = self.pilot_service.get_all_pilots()
        if all_pilots is None:
            print("No pilot data found")
            return

        selected_pilot = u.select_from_records("Choose a pilot:", all_pilots)
        if selected_pilot is None:
            return

        pilot_id = selected_pilot[0]
        pilot_name = selected_pilot[1]

        return pilot_id, pilot_name

    # Returns a list of pilot IDs from a multi-select.

    def _select_pilots_from_checkbox(self, pilots):
        selected_pilots = u.prompt_checkbox("Select from available pilots:", pilots)
        if selected_pilots is None:
            return

        pilot_ids = [pilot[0] for pilot in selected_pilots]

        return pilot_ids

    # Display update confirmation message and handle update operations.

    def _confirm_update_flight(self, flight_to_update):
        flight_id, destination, departure_date, departure_time, status = (
            flight_to_update
        )

        confirm_update = u.prompt_confirm(
            f"Selected flight with ID: {flight_id}, destination: {destination}, date: {departure_date}, time: {departure_time}, status: {status} \nUpdate this flight? (y/n)"
        )
        if not confirm_update:
            print("Update cancelled.")
            return

        options = {
            "Destination": lambda: self._update_flight_destination(flight_id),
            "Departure Date": lambda: self._update_flight_departure_date(flight_id),
            "Departure Time": lambda: self._update_flight_departure_time(flight_id),
            "status": lambda: self._update_flight_status(flight_id),
            "Pilots": lambda: self._update_flight_pilots(flight_id, departure_date),
        }

        u.present_standard_options(options, "Choose an option to update:")

    # Used to send the selected update field and value to the update method in the flights service.

    def _update_flight_field(self, flight_id, field_to_update, value):
        result = self.flights_service.update_flight(flight_id, field_to_update, value)
        if result is None:
            return

        print(result)

    # Display delete confiirmation and handle delete operations.

    def _confirm_delete_flight(self, flight_to_delete):
        flight_id, destination, departure_date, departure_time, status = (
            flight_to_delete
        )

        confirm_delete = u.prompt_confirm(
            f"Selected flight with ID: {flight_id}, destination: {destination}, date: {departure_date}, time: {departure_time}, status: {status} \nDelete this flight? (y/n)"
        )
        if not confirm_delete:
            print("Deletion cancelled.")
            return

        result = self.flights_service.delete_filght(flight_id)
        if result is None:
            return

        print(result)

    # Used to display pilots for flight. Used by search and select methods.

    def _get_pilots_for_flight(self, flight_id):
        result = self.flights_service.get_pilots_for_flight(flight_id)
        if result is None:
            print(f"No pilots found for flight '{flight_id}'.")
            return

        table = tabulate(
            result,
            headers=["Pilot ID", "Pilot Name"],
            tablefmt="fancy_grid",
        )
        print(table)
