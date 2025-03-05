import re


def format_duration(duration: str) -> str:
    # Regular expression to parse ISO 8601 duration
    pattern = re.compile(
        r'P'                         # Starts with 'P'
        r'(?:(?P<years>\d+)Y)?'      # Years
        r'(?:(?P<months>\d+)M)?'     # Months
        r'(?:(?P<weeks>\d+)W)?'      # Weeks
        r'(?:(?P<days>\d+)D)?'       # Days
        r'(?:T'                      # Time part starts with 'T'
        r'(?:(?P<hours>\d+)H)?'      # Hours
        r'(?:(?P<minutes>\d+)M)?'    # Minutes
        r'(?:(?P<seconds>\d+)S)?'    # Seconds
        r')?'                        # Time part is optional
    )

    match = pattern.fullmatch(duration)
    if not match:
        raise ValueError(f"Invalid ISO 8601 duration: {duration}")

    parts = []
    units = [
        ('years', 'year'),
        ('months', 'month'),
        ('weeks', 'week'),
        ('days', 'day'),
        ('hours', 'hour'),
        ('minutes', 'minute'),
        ('seconds', 'second')
    ]

    for key, label in units:
        value = match.group(key)
        if value:
            part = f"{value} {label}{'s' if int(value) != 1 else ''}"
            parts.append(part)

    return ', '.join(parts) if parts else '0 seconds'
