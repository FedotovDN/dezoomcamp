from time import time
import pandas as pd
from sqlalchemy import create_engine
import os
import tarfile


def ingest_callable(user, password, host, port, db, table_name, csv_file, year, execution_date):
    print(table_name, str(year), execution_date)

    tar = tarfile.open(csv_file, "r:gz")
    tar.extractall('./' + str(year))
    tar.close()

    files = os.listdir(str(year))

    print('host=' + host)
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    print('connection established successfully, instering data...')

    flag = True
    for f in files:
        t_start = time()
        df = pd.read_csv(str(year) + '/' + f)
        df.STATION = df.STATION.astype(str)
        df.NAME = df.NAME.astype(str)

        if flag:
            df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
            flag = False
        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()

        print('inserted ' + f + ', took %.3f second' % (t_end - t_start))
