from tabulate import tabulate
from utils.utils import Utils as u


class DestinationHandler:
    def __init__(self, destinations_service):
        self.destinations_service = destinations_service

    # Parent method to present user with initial CRUD options.

    def handle_destination_queries(self):
        options = {
            "Create Destination": self._handle_create_destinations,
            "View Destinations": self._handle_read_destinations,
            "Update Destinations": self._handle_update_destinations,
            "Delete Destinations": self._handle_delete_destinations,
        }

        u.present_standard_options(options)

    # CREATE

    # Creates new destination. Accepts destination name input (unique).

    def _handle_create_destinations(self):
        destination_name = u.prompt_text("Enter destination name")
        if destination_name is None:
            return

        result = self.destinations_service.create_destination(destination_name)
        if result is None:
            return

        print(result)

    # READ

    # Parent method for destination read queries.

    def _handle_read_destinations(self):
        options = {
            "View all destinations": self._view_all_destinations,
            "View destination by ID": self._view_destination_by_id,
            "View destination by name": self._view_destination_by_name,
        }

        u.present_standard_options(options)

    # Fetch all destinations.

    def _view_all_destinations(self):
        result = self.destinations_service.get_all_destinations()
        if result is None:
            print("No destination data found")
            return

        table = tabulate(
            result,
            headers=[
                "Destination ID",
                "Destination Name",
            ],
            tablefmt="fancy_grid",
        )
        print(table)

    # Fetch single destination by ID.

    def _view_destination_by_id(self):
        destination_id = u.prompt_id("Enter destination ID")
        if destination_id is None:
            return

        result = self.destinations_service.get_destination_by_id(destination_id)
        if result is None:
            print(f"No destination found with ID '{destination_id}'.")
            return

        table = tabulate(
            result,
            headers=[
                "Destination ID",
                "Destination name",
            ],
            tablefmt="fancy_grid",
        )
        print(table)

    # Fetch single destination by name (unique).

    def _view_destination_by_name(self):
        destination_name = u.prompt_text("Enter destination name")
        if destination_name is None:
            return

        result = self.destinations_service.get_destination_by_name(destination_name)
        if result is None:
            print(f"No destination found with name '{destination_name}'.")
            return

        table = tabulate(
            result,
            headers=[
                "Destination ID",
                "Destination name",
            ],
            tablefmt="fancy_grid",
        )
        print(table)

    # UPDATE

    # Parent method for updating destinations.

    def _handle_update_destinations(self):
        options = {
            "Search for a destination to update": self._handle_update_destination_by_id,
            "View all destinations to update": self._handle_find_all_and_update,
        }

        u.present_standard_options(options)

    # Search for a destination to update.

    def _handle_update_destination_by_id(self):
        destination_id = u.prompt_id("Enter destination ID")
        if destination_id is None:
            return

        destination_to_update = self.destinations_service.get_destination_by_id(
            destination_id
        )
        if destination_to_update is None:
            print(f"No destination found with ID: '{destination_id}'")
            return

        destination = destination_to_update[0]

        self._confirm_update_destination(destination)

    # Select destination to update from all destinations.

    def _handle_find_all_and_update(self):
        all_destinations = self.destinations_service.get_all_destinations()
        if all_destinations is None:
            print("No destination data found")
            return

        selected_destination = u.select_from_records(
            "Choose a destination to update:", all_destinations
        )
        if selected_destination is None:
            return

        self._confirm_update_destination(selected_destination)

    # Method to update destination name (unique).

    def _update_destination_name(self, destination_id):
        destination_name = u.prompt_text("Enter new destination name")
        if destination_name is None:
            return

        field_to_update = "destination_name"

        result = self.destinations_service.update_destination(
            destination_id, field_to_update, destination_name
        )

        if result is None:
            return

        print(f"{result}, new destination name: {destination_name}")
        return

    # DELETE

    # Parent method to soft delete destination.

    def _handle_delete_destinations(self):
        options = {
            "View all destinations to delete": self._handle_find_all_and_delete,
        }

        u.present_standard_options(options)

    # Select destination to delete from all destinations.

    def _handle_find_all_and_delete(self):
        eligible_destinations = (
            self.destinations_service.get_all_destinations_for_deletion()
        )
        if eligible_destinations is None:
            print("No available destination found for deletion")
            return

        selected_destination = u.select_from_records(
            "Only displaying destinations for completed flights. \n Choose a destination to delete:",
            eligible_destinations,
        )
        if selected_destination is None:
            return

        destination_id, destination_name = selected_destination

        confirm_delete = u.prompt_confirm(
            f"Selected destination with ID: {destination_id}, name: {destination_name} \nDelete this destination? (y/n)"
        )
        if not confirm_delete:
            print("Delete cancelled.")
            return

        result = self.destinations_service.delete_destination(destination_id)
        if result is None:
            return

        print(result)

    # Shared methods

    # Display update confirmation and handle update operation.

    def _confirm_update_destination(self, destination_to_update):
        destination_id, destination_name = destination_to_update

        confirm_update = u.prompt_confirm(
            f"Selected destination with ID: {destination_id}, name: {destination_name} \nUpdate this destination? (y/n)"
        )
        if not confirm_update:
            print("Update cancelled.")
            return

        options = {
            "Destination name": lambda: self._update_destination_name(destination_id),
        }

        u.present_standard_options(options, "Choose an option to update:")
