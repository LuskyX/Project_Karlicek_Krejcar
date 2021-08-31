import pandas as pd
import matplotlib.pyplot as plt


# Loading the data
data = pd.read_csv("https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovaci-mista.csv")
# Choose the vaccination center to perform the analysis
vacc_center = "Oblastní nemocnice Kolín, a.s."

def generate_plots(data, vacc_center):
    stat = data[data["zarizeni_nazev"] == vacc_center]["vakcina"].value_counts()
    indices = [x for x in stat.index]
    numbers = [x for x in stat.values]
    # Pie chart
    sizes = numbers
    # Colors
    colors = ["#AE5552","#D69A80","#D63B59", "#AE5552"]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, colors=colors, labels=indices, autopct='%1.1f%%', startangle=-20)
    # Draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # To ensure a circle is drown equally
    ax1.axis('equal')
    plt.tight_layout()
    plt.show(
    #Time series of daily vaccinations for past month
    information = data[data["zarizeni_nazev"] == vacc_center]
    table = information["datum"].value_counts().sort_index()
    indices = [x for x in table.index]
    numbers = [x for x in table.values]
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(indices[-30:-1], numbers[-30:-1], color='tab:orange')
    # Same as above
    ax.set_xlabel('Date')
    plt.xticks(rotation=70)
    ax.set_ylabel('Daily Vaccines used')
    ax.set_title(f'Trend of vaccination for {vacc_center} in past 30 days')
    plt.show()