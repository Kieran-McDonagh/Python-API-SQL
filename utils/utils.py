from datetime import datetime
import sys
import questionary

class Utils:
    # Method to select an option from provided options. If user selects exit quit the application.

    @staticmethod
    def prompt_select_exit(message, options):
        options = [*options, "Exit"] if "Exit" not in options else options
        result = questionary.select(message, choices=options).ask()
        if result == "Exit":
            sys.exit(0)
        return result
    
    # Return the result of a users selected input.

    @staticmethod
    def prompt_select(message, options):
        result = questionary.select(message, choices=options).ask()
        return result

    # Return the result of a users selected record.

    @staticmethod
    def select_from_records(message, records):
        choices = ["Back"] + [
            questionary.Choice(title=f"(ID {record[0]}) {record[1]}", value=record)
            for record in records
        ]

        selected = questionary.select(message, choices=choices).ask()

        if selected == "Back":
            return None

        return selected
    
    # Returns result of users selected flight record.

    @staticmethod
    def select_flight_from_records(message, records):
        choices = ["Back"] + [
            questionary.Choice(
                title=f"Flight ID: {record[0]}, Destination: {record[1]}, Departure Date: {record[2]}, Departure Time: {record[3]}, Status: {record[4]}",
                value=record,
            )
            for record in records
        ]

        selected = questionary.select(message, choices=choices).ask()

        if selected == "Back":
            return None

        return selected
    
    # Presents a multi-select to the user, returns the selected options.

    @staticmethod
    def prompt_checkbox(message, records):
        choices = ["Back"] + [
            questionary.Choice(title=f"(ID {record[0]}) {record[1]}", value=record)
            for record in records
        ]

        selected = questionary.checkbox(message, choices=choices).ask()

        if selected == "Back":
            return None

        if not selected:
            print("No option selected")
            return None

        return selected
    
    # Displays list of options but accepts list instead of dict.

    @staticmethod
    def prompt_select_from_list(message, options):
        choices = ["Back"] + options
        selection = questionary.select(message, choices=choices).ask()

        if selection == "Back":
            return None

        return selection

    # Returns result of users text input.

    @staticmethod
    def prompt_text(message):
        user_input = questionary.text(f"(Press Ctr+C to cancel) \n{message}:").ask()

        if not user_input:
            print("No input received.")
            return

        return user_input.strip().lower()

    # Returns the result of the ID the user has input.

    @staticmethod
    def prompt_id(message):
        user_input = questionary.text(f"(Press Ctr+C to cancel) \n{message}:").ask()

        if not user_input:
            print("No input received.")
            return

        if not user_input.isdigit():
            print("Input must be numerical.")
            return

        return user_input.strip().lower()

    # Display confirmation message and return result.

    @staticmethod
    def prompt_confirm(message):
        while True:
            user_input = questionary.text(message).ask()

            if not user_input:
                print("No input received. Please enter a value.")
                continue

            user_input = user_input.strip().lower()

            if user_input == "y":
                return True
            elif user_input == "n":
                return False
            else:
                print("Invalid input, must be y or n")
                continue

    # Method to parse a provided date input.

    @staticmethod
    def parse_date(user_input):
        try:
            parsed_date = datetime.strptime(user_input, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter as YYYY-MM-DD (e.g. 2025-04-01).")
            return None
        
    # Method to parse a provided time input.

    @staticmethod
    def parse_time(user_input):
        try:
            parsed_time = datetime.strptime(user_input, "%H:%M")
            formatted_time = parsed_time.strftime("%H:%M:%S")
            return formatted_time
        except ValueError:
            print("Invalid time format. Please enter time as HH:MM (e.g. 18:00).")
            return None

    # Displays initial options to user, top level of user menu, allows for exit.
    # Envoke the method of the selected option.

    @staticmethod
    def present_initial_options(
        options,
        message="Choose an option:",
    ):
        while True:
            option = Utils.prompt_select_exit(message, [*options.keys()])
            handler = options.get(option)
            if handler:
                handler()

    # Displays options to user with option to go back a level.
    # Envoke the method of the selected option.

    @staticmethod
    def present_standard_options(
        options,
        message="Choose an option:",
    ):
        while True:
            option = Utils.prompt_select(message, ["Back", *options.keys()])
            handler = options.get(option)
            if handler:
                handler()

            if option == "Back":
                break
