import DB

def to_int(num_str):
    if '.' in num_str:
        return float(num_str.replace(",", ""))
    else:
        return int(num_str.replace(",", ""))

def send_Results(name):
    with DB.Database_Manager("GuessTheCountry_DB.db") as db:
        try:
            query = """
                    SELECT * FROM Countries
                    WHERE Name = ?;
                    """

            result = db.execute_query(query, (name,))
            result = db.fetchall()[0]

            send_results = list(result[1:])

            send_results[1] = f"{int(send_results[1]):,}"
            
            send_results[2] = send_results[2].split('.0')
            if send_results[2][-1] != "":
                send_results[2] = f"{float(send_results[2][0])}"
            else:
                send_results[2] = f"{int(send_results[2][0]):,}"

            return send_results


        except Exception as e:
            print(f"Error querying database: {e}")


def get_Neighbors(name):
    with DB.Database_Manager("GuessTheCountry_DB.db") as db:
        try:
            query = """
                    SELECT Neighbor_Name FROM Country_Neighbors
                    WHERE Country_Name = ?;
                    """

            result = db.execute_query(query, (name,))
            result = db.fetchall()

            neighbors = []
            for r in result:
                neighbors.append(r[0])

            return neighbors


        except Exception as e:
            print(f"Error querying database: {e}")

def Comparison(country1, country2):

    results_country1 = send_Results(country1)
    results_country2 = send_Results(country2)

    if country1 == country2:
        colors = ['green', 'green', 'green', 'green', 'green', 'green']
    else:
        colors = []

        neighbors = get_Neighbors(country2)

        if country1 in neighbors: colors.append("yellow")
        else: colors.append("gray")

        # Population
        d_pp = to_int(results_country1[1]) - to_int(results_country2[1])

        if d_pp == 0: colors.append('green')
        elif abs(d_pp) <= 2000000: colors.append("yellow")
        elif d_pp > 0: colors.append('↑')
        else: colors.append('↓')

        # Territory
        d_ar = to_int(results_country1[2]) - to_int(results_country2[2])

        if d_ar == 0: colors.append('green')
        elif abs(d_ar) <= 5000: colors.append("yellow")
        elif d_ar > 0: colors.append('↑')
        else: colors.append('↓')

        # Continent
        if results_country1[3] == results_country2[3]: colors.append('green')
        else: colors.append('gray')

        # Currency
        if results_country1[4] == results_country2[4]: colors.append('green')
        else: colors.append('gray')

        # Time_zone
        t1 = float(results_country1[5])
        t2 = float(results_country2[5])

        d_t = t1 - t2

        if d_t == 0: colors.append('green')
        elif abs(d_t) <= 2: colors.append("yellow")
        elif d_t > 0: colors.append('↑')
        else: colors.append('↓')

    return results_country1, results_country2, colors
