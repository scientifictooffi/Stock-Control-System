from stock_control.store import Store


def save_data(store, file_path):
    """R9 (Member 4): As Sam, I want the data saved with a backup so that
    nothing is lost if a file gets damaged.

    Rules:
        1. Saved as JSON
        2. Backup made before each save
        3. Missing file starts empty
        4. Damaged file loads the backup
        5. If both fail, a clear error is shown
    """
    raise NotImplementedError("R9 save_data is not implemented yet")


def load_data(file_path):
    """R9 (Member 4): As Sam, I want the data saved with a backup so that
    nothing is lost if a file gets damaged.

    Rules:
        1. Saved as JSON
        2. Backup made before each save
        3. Missing file starts empty
        4. Damaged file loads the backup
        5. If both fail, a clear error is shown
    """
    raise NotImplementedError("R9 load_data is not implemented yet")
