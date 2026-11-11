"""Input processors used for the Lab 7 fuzz-testing exercise."""


def parse_int_list(value):
    """Parse comma-separated integers, rejecting malformed or oversized input."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    if len(value) > 10_000:
        raise ValueError("input is too long")
    if not value.strip():
        return []

    parts = value.split(",")
    if len(parts) > 1_000:
        raise ValueError("too many values")
    parsed = []
    for part in parts:
        token = part.strip()
        if not token:
            raise ValueError("empty integer value")
        if len(token) > 100:
            raise ValueError("integer token is too long")
        parsed.append(int(token, 10))
    return parsed


def normalize_username(value):
    """Normalize a username to lowercase after validating its shape."""
    if not isinstance(value, str):
        raise TypeError("username must be a string")
    normalized = value.strip().lower()
    if not normalized or len(normalized) > 32:
        raise ValueError("username must contain 1 to 32 characters")
    if not all(char.isalnum() or char in "-_" for char in normalized):
        raise ValueError("username contains unsupported characters")
    return normalized


def calculate_average(values):
    """Return the arithmetic mean of a bounded list of finite numbers."""
    if not isinstance(values, (list, tuple)):
        raise TypeError("values must be a list or tuple")
    if not values:
        raise ValueError("values cannot be empty")
    if len(values) > 1_000:
        raise ValueError("too many values")
    total = 0.0
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("every value must be a number")
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError("values must be finite")
        total += value
    result = total / len(values)
    if result != result or result in (float("inf"), float("-inf")):
        raise ValueError("average is outside the supported range")
    return result


def main():
    print("Parsed integers:", parse_int_list("2, 4, 6"))
    print("Normalized username:", normalize_username("  Transit_User-7  "))
    print("Average:", calculate_average([10, 20, 30]))


if __name__ == "__main__":
    main()
