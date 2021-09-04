
def print_output(center):
    center = transform_open_hours(center)

    output = f"""
____________________________________________________________________________________________________
Name: \t {center.name}
Link: \t {center.link}
ID:   \t {center.vacc_id}

Region:     {center.region}
Address:    {center.info['address']}
            {center.info['address_spec']}

Phone:      {center.info['phone']}
Email:      {center.info['email']}

Note: {center.info['note']}

Vaccines:       {center.info['vaccines'].replace("'", "")}
Center type:    {center.info['add_info'].replace("'", "")}
Daily capacity: {center.info['capacity']}
Change of date: {center.info['changing_date'].replace("'", "")}

Opening hours:
_________________________________
               Open    |  Closed
Monday:       | {center.open_hours['monday'][0]}  |  {center.open_hours['monday'][1]} |
Tuesday:      | {center.open_hours['tuesday'][0]}  |  {center.open_hours['tuesday'][1]} |
Wednesday:    | {center.open_hours['wednesday'][0]}  |  {center.open_hours['wednesday'][1]} |
Thursday:     | {center.open_hours['thursday'][0]}  |  {center.open_hours['thursday'][1]} |
Friday:       | {center.open_hours['friday'][0]}  |  {center.open_hours['friday'][1]} |
Saturday:     | {center.open_hours['saturday'][0]}  |  {center.open_hours['saturday'][1]} |
Sunday:       | {center.open_hours['sunday'][0]}  |  {center.open_hours['sunday'][1]} |
____________________________________________________________________________________________________
    """
    print(output)


def transform_open_hours(center):
    for day in center.open_hours:
        center.open_hours[day] = [decimal_to_hour(center.open_hours[day][0]), decimal_to_hour(center.open_hours[day][1])]
    return center


def decimal_to_hour(decimal):
    if decimal is None:
        time = "None "
    else:
        hour = str(int(decimal))
        if len(hour) == 1:
            time = "0" + hour
        else:
            time = hour
        minutes = str(int(decimal % 1 * 60))
        if len(minutes) == 1:
            time += ":0" + minutes
        else:
            time += ":" + minutes
    return time
