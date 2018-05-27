def dictfetch(cursor, N, offset=None):
    """Returns all rows from a cursor as a dict"""
    desc = cursor.description
    rows = []

    try:
        N = int(N)
    except:
        N = None
    if not N:
        rows = cursor.fetchall()
    else:
        try:
            offset = int(offset)
        except:
            pass
        if offset and type(offset) == int:
            N = offset + N
        else:
            offset = 0
        rows = cursor.fetchall()[offset:N]
    return [
        dict(zip([col[0] for col in desc], row))
        for row in rows
        ]