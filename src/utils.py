def is_valid_status_code(status_code: int) -> bool:
    """Verifies if the status code is considered as valid status code

    Args:
        status_code: The status code to check

    Returns:
        True if the status code is valid else returns False
    """
    # To follow feedback from part one submission.
    return 200 <= status_code <= 299 or status_code == 304
