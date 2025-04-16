class PilotService:
    def __init__(self, pilots_provider):
        self.pilots_provider = pilots_provider

    # Service responsible for passing data between handlers and pilot provider.

    # CREATE

    def create_pilot(self, pilot_name):
        result = self.pilots_provider.create_pilot(pilot_name)
        return result

    # READ

    def get_all_pilots(self):
        pilots = self.pilots_provider.get_all_pilots()
        return pilots

    def get_pilot_by_id(self, id_input):
        pilot = self.pilots_provider.get_pilot_by_id(id_input)
        return pilot

    def get_all_pilots_for_deletion(self):
        pilots = self.pilots_provider.get_all_pilots_for_deletion()
        return pilots

    def get_available_pilots_for_date(self, departure_date):
        pilots = self.pilots_provider.get_available_pilots_for_date(departure_date)
        return pilots

    def get_available_pilots_for_flight(self, flight_id, departure_date):
        pilots = self.pilots_provider.get_available_pilots_for_flight(
            flight_id, departure_date
        )
        return pilots

    # UPDATE

    def update_pilot(self, pilot_id, field_to_update, value):
        result = self.pilots_provider.update_pilot(pilot_id, field_to_update, value)
        return result

    # DELETE

    def delete_pilot_by_id(self, pilot_id):
        result = self.pilots_provider.delete_pilot_by_id(pilot_id)
        return result
