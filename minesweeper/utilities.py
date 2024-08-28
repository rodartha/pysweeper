def generate_time_string(seconds):
    minutes, seconds = divmod(seconds, 60)
    time_string = f"{minutes:02}:{seconds:02}"

    return time_string
