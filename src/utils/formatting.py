def format_currency(amount):
    """Format a number as currency (USD)."""
    try:
        return f"${float(amount):,.2f}"
    except Exception:
        return "$0.00" 