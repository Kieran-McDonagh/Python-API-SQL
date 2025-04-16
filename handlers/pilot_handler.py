from tabulate import tabulate
from utils.utils import Utils as u


class PilotHandler:
    def __init__(self, pilots_service):
        self.pilots_service = pilots_service

    # Parent method for pilot CRUD operations.

    def handle_pilot_queries(self):
        options = {
            "Create Pilots": self._handle_create_pilots,
            "View Pilots": self._handle_read_pilots,
            "Update Pilots": self._handle_update_pilots,
            "Delete Pilots": self._handle_delete_pilots,
        }

        u.present_standard_options(options)

    # CREATE

    # Method to create a new pilot. Accepts pilot name.

    def _handle_create_pilots(self):
        name_input = u.prompt_text("Enter new pilot name")
        if name_input is None:
            return

        result = self.pilots_service.create_pilot(name_input)
        if result is None:
            return

        print(result)

    # READ

    # Parent method for reading pilots.

    def _handle_read_pilots(self):
        options = {
            "View all pilots": self._view_all_pilots,
            "View pilot by ID": self._view_pilot_by_id,
        }

        u.present_standard_options(options)

    # fetch all pilots not marked as deleted.

    def _view_all_pilots(self):
        result = self.pilots_service.get_all_pilots()
        if result is None:
            print("No pilot data found")
            return

        table = tabulate(
            result, headers=["Pilot ID", "Pilot Name"], tablefmt="fancy_grid"
        )
        print(table)

    # Fetch single pilot by pilot ID.

    def _view_pilot_by_id(self):
        id_input = u.prompt_id("Enter pilot ID")
        if id_input is None:
            return

        result = self.pilots_service.get_pilot_by_id(id_input)
        if result is None:
            print(f"No pilot found with ID '{id_input}'.")
            return

        table = tabulate(
            result, headers=["Pilot Number", "Pilot Name"], tablefmt="fancy_grid"
        )
        print(table)

    # UPDATE

    # Parent method for updating pilot. Allows update by ID or
    # Select from all pilots.

    def _handle_update_pilots(self):
        options = {
            "Search for a pilot to update": self._handle_update_pilot_by_id,
            "View all pilots to update": self._handle_find_all_and_update,
        }

        u.present_standard_options(options)

    # Search and update.

    def _handle_update_pilot_by_id(self):
        pilot_id = u.prompt_id("Enter pilot ID")
        if pilot_id is None:
            return

        pilot = self.pilots_service.get_pilot_by_id(pilot_id)
        if pilot is None:
            print(f"No pilot found with ID: '{pilot_id}'")
            return

        pilot_to_update = pilot[0]

        self._confirm_update_pilot(pilot_to_update)

    # Select from all pilots and update.

    def _handle_find_all_and_update(self):
        all_pilots = self.pilots_service.get_all_pilots()
        if all_pilots is None:
            print("No pilot data found")
            return

        selected_pilot = u.select_from_records("Choose a pilot to update:", all_pilots)
        if selected_pilot is None:
            return

        self._confirm_update_pilot(selected_pilot)

    # Update name field for pilot. Not unique.

    def _update_pilot_name(self, pilot_id):
        pilot_name = u.prompt_text("Enter new pilot name")
        if pilot_name is None:
            return

        field_to_update = "pilot_name"

        result = self.pilots_service.update_pilot(pilot_id, field_to_update, pilot_name)
        if result is None:
            return

        print(f"{result}, new pilot name: {pilot_name}")

    # DELETE

    # Parent method for soft deleting pilots.

    def _handle_delete_pilots(self):
        options = {
            "View all pilots to delete": self._handle_find_all_and_delete,
        }

        u.present_standard_options(options)

    # Select pilot to delete from all pilots.

    def _handle_find_all_and_delete(self):
        # Only fetch pilots that are assigned to completed flights or who have no flight assignments.

        eligible_pilots = self.pilots_service.get_all_pilots_for_deletion()
        if eligible_pilots is None:
            print("No pilot found for deletion")
            return

        selected_pilot = u.select_from_records(
            "Only displaying pilots assigned to completed flights or who have no flight assignments. \n Choose a pilot to delete:",
            eligible_pilots,
        )
        if selected_pilot is None:
            return

        pilot_id, pilot_name = selected_pilot

        confirm_delete = u.prompt_confirm(
            f"Selected pilot with ID: {pilot_id}, name: {pilot_name} \nDelete this pilot? (y/n)"
        )
        if not confirm_delete:
            print("Delete cancelled.")
            return

        result = self.pilots_service.delete_pilot_by_id(pilot_id)
        if result is None:
            return

        print(result)

    # Shared methods

    # Display update confirmation and handle update operation.

    def _confirm_update_pilot(self, pilot_to_update):
        pilot_id, pilot_name = pilot_to_update

        confirm_update = u.prompt_confirm(
            f"Selected pilot with ID: {pilot_id}, name: {pilot_name} \nUpdate this pilot? (y/n)"
        )
        if not confirm_update:
            print("Update cancelled.")
            return

        options = {
            "Pilot name": lambda: self._update_pilot_name(pilot_id),
        }

        u.present_standard_options(options, "Choose an option to update:")
