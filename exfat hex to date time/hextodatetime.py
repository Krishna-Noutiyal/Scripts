def decode_fat_timestamp(fat_timestamp):
    """
    Decodes a FAT timestamp into a readable date and time.

    Args:
        fat_timestamp (int): A 32-bit FAT timestamp.

    Returns:
        str: Date and time in "YYYY-MM-DD HH:MM:SS" format.
    """
    # Extract the date (lower 16 bits)
    date_part = fat_timestamp & 0xFFFF
    year = ((date_part >> 9) & 0x7F) + 1980  # Extract bits 9-15 and add 1980
    month = (date_part >> 5) & 0x0F  # Extract bits 5-8
    day = date_part & 0x1F  # Extract bits 0-4

    # Extract the time (upper 16 bits)
    time_part = (fat_timestamp >> 16) & 0xFFFF
    hour = (time_part >> 11) & 0x1F  # Extract bits 11-15
    minute = (time_part >> 5) & 0x3F  # Extract bits 5-10
    second = (time_part & 0x1F) * 2  # Extract bits 0-4, multiply by 2

    # Combine into a formatted string
    return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"


# Example usage
fat_timestamp = 0x7ef45e7d  # Example FAT timestamp
decoded_datetime = decode_fat_timestamp(fat_timestamp)
print(f"Decoded Date and Time: {decoded_datetime}")
