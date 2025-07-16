def calculate_property_tax(value, location, property_type):
    """
    Example property tax calculation logic.
    """
    # Dummy logic: 1% of value for demonstration
    try:
        value = float(value)
    except Exception:
        return 0
    return value * 0.01 