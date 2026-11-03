from stock_control.store import Store


def query_audit_log(
        store, requesting_user, user=None, action=None, start_date=None,
        end_date=None):
    """R8 (Member 4): As David, I want a log of every change made so that I can
    see who changed what and when.

    Rules:
        1. Every add, edit and delete is logged with user, time, old and
           new value
        2. Filter by user, action and date
        3. Only admin and managers can view it
    """
    raise NotImplementedError("R8 query_audit_log is not implemented yet")
