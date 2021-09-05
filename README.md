# Project_Karlicek_Krejcar
Data Processing in Python Project
This is a repository for our Data Processing in Python project. Collaborative work of Vilém Krejcar and Ondřej Karlíček. 

# Finding nearest vaccination centers

Based on arguments given by the user (more below), our program finds three nearest vaccination centers.

For the purpose to obtain data about centers, we are scraping https://ockoreport.uzis.cz/.
Nextly, we are merging this data with a dataset from https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19,
where we get GPS coordinates of vaccination centers.

Also, we are scraping Wikipedia to obtain GPS coordinates of municipalities in the Czech Republic.

All data are then stored in the SQLlite3 database.


## Project structure


```
│   main.py                                   # script which connects and runs all others scripts
│   config.py                                 # variables used in scripts
│   README.md
│   presentation.ipynb                        # main output of our project. 
│   
├───db
│   ├───database.db                           # SQLlite3 database
│               
└───tools
    │   data_classes.py                       # classes for storing data
    │   database_connector.py                 # class used to connect and manipulate with database
    │   printer.py                            # script printing output for resulting centers
    │   query_creator.py                      # creates a query for filtering the data in a database
    │   location_scraper.py                   # class for scraping Wikipedia to obtain GPS coordinates
    ├── vaccination_centers_scrapper.py       # class for scraping info about vaccinations centers
```

## Arguments 

* `location`
    * a name of town/village in the Czech Republic or Prague's district
    * for options, see:
        * https://cs.wikipedia.org/wiki/Seznam_obc%C3%AD_v_%C4%8Cesku
        * https://cs.wikipedia.org/wiki/Praha#%C3%9Azemn%C3%AD_%C4%8Dlen%C4%9Bn%C3%AD
    * if a municipality is a duplicate, the user is obliged to specify the region of such city:
        * format: "name (region)"
        * example: "Kozojedy (okres Plzeň-sever)"
    
* `vaccine`
    * specify the desired vaccine - if "None", the vaccine supplier won't be taken into account
    * default is set to "None"
    * options: COMIRNATY, SPIKEVAX, JANSSEN, Vaxzevria, None
    
* `age_group`
    * specify your age group, the default set to "adult"
    * options:
        * adult: 18+
        * teenager: 16-17
        * child: 12-15
    
* `without_registration`
    * default is set to "None" -> no preference regarding the registration
    * if "True" -> you only search centers without registration
    * if "False" ->  you only want centers with registration
    
* `self_payer`
    * default set to "False" -> you are not a self-payer
    * if "True" -> you only want centers for self-payers
    
* `monday`
    * specify your desired time on Monday, default None
    * accepts int or float, thus for "10:30" set monday = 10.5
    
* `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday`
    * same as monday
    * if you specify multiple days, the program will find centers with opening hours meeting conditions for atleast one day
    * if all days are "None", then the opening hours will not be taken into account
    
* `update`
    * default to "False" -> does nothing
    * if "True" -> it downloads data and updates the database
    

## Update

For update set `update=True`. It should take around 70 minutes.


## How to run
Simply open the **presentation.ipynb** and run `give_me_three_centers` from `main.py` with specific arguments of choosing. 


## Requirements

tqdm, requests, beautifulsoup4, mechanicalsoup
