import os
import argparse
import pandas as pd
from sqlalchemy import create_engine

def main(args):
    user_name = args.user_name
    password = args.password
    db = args.db
    host = args.host
    port = args.port
    url = args.url

    downloaded_csv_name = 'taxi.csv'
    
    print("Downloading Taxi CSV")
    os.system(f"wget {url} -O {downloaded_csv_name}")
    print("CSV file downloaded")
    # Create SQLAlchemy engine - adjust the connection string based on your setup
    engine = create_engine(f'postgresql://{user_name}:{password}@{host}:{port}/{db}')

    # Read CSV in chunks
    df_iter = pd.read_csv(downloaded_csv_name, compression='gzip', iterator=True, chunksize=50000)

    # Process each chunk
    for i, df in enumerate(df_iter):
        # Convert datetime columns
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        
        # Insert data
        df.to_sql(
            name='green_taxi_data', 
            con=engine, 
            if_exists='append' if i > 0 else 'replace',
            index=False
        )
        
        print(f'Inserted chunk {i+1}')


if __name__ == "__main__":
    print("Starting ingestion")
    parser = argparse.ArgumentParser(description = 'Ingest CSV data to Postgres')
    parser.add_argument('--user_name', help='user name for test')
    parser.add_argument('--password', help='password for test')
    parser.add_argument('--db', help='database for test')
    parser.add_argument('--host', help='host for test')
    parser.add_argument('--port', help='port for test')
    parser.add_argument('--url', help='url for the csv file')
    args = parser.parse_args()
    main(args)