class Property:
    def __init__(self, value, location, property_type):
        self.value = value
        self.location = location
        self.property_type = property_type

    def __repr__(self):
        return f"<Property value={self.value} location={self.location} type={self.property_type}>" 