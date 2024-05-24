CREATE TABLE casos_covid ( 
    num_item INTEGER,
    city TEXT,
    city_ibge_code INTEGER,
    date TEXT,
    epidemiological_week INTEGER,
    estimated_population REAL,
    estimated_population_2019 REAL,
    is_last INTEGER,
    is_repeated INTEGER,
    last_available_confirmed REAL,
    last_available_confirmed_per_100k_inhabitants REAL,
    last_available_date REAL,
    last_available_death_rate REAL,
    last_available_deaths REAL,
    order_for_place INTEGER,
    place_type TEXT,
    state TEXT,
    new_confirmed REAL,
    new_deaths REAL,
    sent_to_broker INTEGER DEFAULT 0);

.mode csv
.import casos_alt.csv casos_covid
.mode table


update casos_covid SET is_last=0 where is_repeated='False';
update casos_covid SET is_last=1 where is_repeated='True';
update casos_covid SET is_repeated=0 where is_repeated='False';
update casos_covid SET is_repeated=1 where is_repeated='True';
update casos_covid SET sent_to_broker=0 where 1=1;

select * from casos_covid where date in (select date from casos_covid where sent_to_broker <> 1 order by date limit(1)) and sent_to_broker=0;
