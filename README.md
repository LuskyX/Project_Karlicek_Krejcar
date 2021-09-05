# Project_Karlicek_Krejcar
Data Processing in Python Project
This is a repository for our Data Processing in Python project. Collaborative work of Vilém Krejcar and Ondřej Karlíček. 

# Finding nearest vaccination centers

Based on arguments given by user (more below) our program find 3 nearest vaccination centers.

For this purpose we are scraping https://ockoreport.uzis.cz/ for obtaining data about centers.
This data we are merging with dataset from https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19
where we get gps coordinates of vaccination centers

Also, we are scraping wikipedia to obtain gps coordinates of locations in Czech Republic.

All data are then stored in SQLlite3 database.


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
    │   database_connector.py                 # class used for connecting to and manipulating database
    │   printer.py                            # script for printing output for resulting centers
    │   query_creator.py                      # creates query for filtering the data in database
    │   location_scraper.py                   # class for scraping wikipedia to obtain gps coordinates
    ├── vaccination_centers_scrapper.py       # class for scraping info about vaccinations centers
```

## Arguments 

* `location`
    * name of town / village in Czech Republic or name of part of Prague
    * for options see:
        * https://cs.wikipedia.org/wiki/Seznam_obc%C3%AD_v_%C4%8Cesku
        * https://cs.wikipedia.org/wiki/Praha#%C3%9Azemn%C3%AD_%C4%8Dlen%C4%9Bn%C3%AD
    * if some town is duplicit you need to specify region also:
        * format: "name (region)"
        * example: "Kozojedy (okres Plzeň-sever)"
    
* `vaccine`
    * specify desired vaccine, if None the vaccine won't be taken into account
    * default None
    * options: COMIRNATY, SPIKEVAX, JANSSEN, Vaxzevria, None
    
* `age_group`
    * specify your age group, default to "adult"
    * options:
        * adult: 18+
        * teenage: 16-17
        * child: 12-15
    
* `without_registration`
    * default None = you don't if you will go to center with registration or not
    * if True = you only want centers without registration
    * if False = you only want centers with registration
    
* `self_payer`
    * default False = you are not self-payer
    * if True = you want only centers for self-payers
    
* `monday`
    * specify your desired time on Monday, default None
    * accept int or float, thus for "10:30" set monday = 10.5
    
* `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday`
    * same as monday
    * if you specify more days, the program will find centers with opening hours which will meet conditions for atleast 1 day
    * if all days are None then opening hours will not be taken into account
    
* `update`
    * default to False = does nothing
    * if True = it downloads data and update database
    

## Update

For update set `update=True`. It should take around 70 minutes.


## How to run
Just open the **presentation.ipynb** and run `give_me_three_centers` from `main.py` with your specific arguments. 
