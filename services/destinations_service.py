class DestinationService:
    def __init__(self, destinations_provider):
        self.destinations_provider = destinations_provider

    # Service responsible for passing data between handlers and destination provider.

    # CREATE

    def create_destination(self, destination_name):
        result = self.destinations_provider.create_destination(destination_name)
        return result

    # READ

    def get_all_destinations(self):
        destinations = self.destinations_provider.get_all_destinations()
        return destinations

    def get_destination_by_id(self, destination_id):
        destination = self.destinations_provider.get_destination_by_id(destination_id)
        return destination

    def get_destination_by_name(self, destination_name):
        destination = self.destinations_provider.get_destination_by_name(
            destination_name
        )
        return destination

    def get_all_destinations_for_deletion(self):
        destinations = self.destinations_provider.get_all_destinations_for_deletion()
        return destinations

    # UPDATE

    def update_destination(self, destination_id, field_to_update, value):
        result = self.destinations_provider.update_destination(
            destination_id, field_to_update, value
        )
        return result

    # DELETE

    def delete_destination(self, destination_id):
        result = self.destinations_provider.delete_destination(destination_id)
        return result
