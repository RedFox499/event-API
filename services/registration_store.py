from models.registration import Registration

class RegistrationStore:
    def __init__(self):
        self.registrations = []
        self.next_registrations_id = 1

    def get_registrations(self):
        return self.registrations

    def add_registration(self, event_id, user_id):
        registration = Registration(id=self.next_registrations_id, event_id=event_id, user_id=user_id)
        self.registrations.append(registration)
        self.next_registrations_id += 1
        return registration

    def delete_registration(self, registration_id):
        return self.registrations.pop(registration_id)
