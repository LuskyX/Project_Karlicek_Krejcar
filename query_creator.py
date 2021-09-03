from config import VACCINES_SET, AGE_GROUP_SET


def create_query(vaccine=None, age_group="adult", without_registration=None, self_payer=False, monday=None,
                 tuesday=None, wednesday=None, thursday=None, friday=None, saturday=None, sunday=None):

    open_hours = {'monday': monday, 'tuesday': tuesday, 'wednesday': wednesday, 'thursday': thursday, 'friday': friday,
                  'saturday': saturday, 'sunday': sunday}

    query = """
    SELECT loc.vacc_id, loc.latitude, loc.longitude
    FROM vacc_center_location as loc
    INNER JOIN vacc_center_type as typ USING(vacc_id)
    """
    if age_group not in AGE_GROUP_SET: raise Exception()
    if int(self_payer) not in [0, 1]: raise Exception()
    query_where = f"""WHERE typ.{age_group} = 1
    AND typ.self_payers = {int(self_payer)}
    """
    if without_registration is not None:
        if int(without_registration) not in [0, 1]: raise Exception()
        query_where += f"AND typ.without_registration = {int(without_registration)} \n"

    if vaccine is not None:
        if vaccine.lower() not in VACCINES_SET:
            raise Exception()
        query += "INNER JOIN vacc_center_vaccines AS vacc USING(vacc_id) \n"
        query_where += f"AND vacc.{vaccine.lower()} = 1 \n"

    open_hours = {day: hour for (day, hour) in open_hours.items() if hour is not None}
    if len(open_hours) != 0:
        query += "INNER JOIN vacc_center_hours as hour USING(vacc_id) \n"
        list_hours = []
        for (day, hour) in open_hours.items():
            if (hour < 0) or (hour > 24): raise Exception()
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
