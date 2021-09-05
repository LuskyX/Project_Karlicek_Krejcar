from config import VACCINES_SET, AGE_GROUP_SET


def create_query(vaccine=None, age_group="adult", without_registration=None, self_payer=False, monday=None,
                 tuesday=None, wednesday=None, thursday=None, friday=None, saturday=None, sunday=None):
    """
    Based on given paramaters create query for SQL filtering
    """

    open_hours = {'monday': monday, 'tuesday': tuesday, 'wednesday': wednesday, 'thursday': thursday, 'friday': friday,
                  'saturday': saturday, 'sunday': sunday}

    query = """
    SELECT loc.vacc_id, loc.latitude, loc.longitude
    FROM vacc_center_location as loc
    INNER JOIN vacc_center_type as typ USING(vacc_id)
    """
    if age_group not in AGE_GROUP_SET: raise Exception('age_group argument can be only: adult, teenage, child')
    if int(self_payer) not in [0, 1]: raise Exception('self_payer argument can be only: True, False')
    query_where = f"""WHERE typ.{age_group} = 1
    AND typ.self_payers = {int(self_payer)}
    """
    if without_registration is not None:
        if int(without_registration) not in [0, 1]: raise Exception('without_registration argument can be only: True, False, None')
        query_where += f"AND typ.without_registration = {int(without_registration)} \n"

    if vaccine is not None:
        if vaccine.lower() not in VACCINES_SET:
            raise Exception('vaccine argument can be only: COMIRNATY, SPIKEVAX, JANSSEN, Vaxzevria, None')
        query += "INNER JOIN vacc_center_vaccines AS vacc USING(vacc_id) \n"
        query_where += f"AND vacc.{vaccine.lower()} = 1 \n"

    open_hours = {day: hour for (day, hour) in open_hours.items() if hour is not None}
    if len(open_hours) != 0:
        query += "INNER JOIN vacc_center_hours as hour USING(vacc_id) \n"
        list_hours = []
        for (day, hour) in open_hours.items():
            if not ((hour >= 0) and (hour <= 24)): raise Exception('days arguments can be only set to None or number between 0 to 24')
            list_hours.append(f"(hour.{day}_open <= {hour} AND hour.{day}_closed >= {hour})")

        query_hours = "AND ("
        n = len(list_hours)
        for i in range(n):
            query_hours += list_hours[i]
            if (i+1) == n:
                query_hours += ")"
            else:
                query_hours += " OR "
        query_where += query_hours
    return query + query_where
