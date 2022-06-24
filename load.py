import sqlite3


def initialize():
    # Create the connection and cursor to the SQLite database
    # When ran for the first time, it'll create the database too
    conn = sqlite3.connect('storage.db')
    cursor = conn.cursor()

    return conn, cursor


def create_tables(conn, cursor, regions):
    # If the "Regions" table doesn't exist, then no table exists, so we check before crating them
    query = '''
        select * from sqlite_master
            where name = 'Regions' and type = 'table';
    '''
    cursor.execute(query)
    if cursor.fetchone() is not None:
        return

    # This next query creates all the tables in the database, specifying each column name and data type
    query = '''
        create table Dates ( extractionDate text primary key );

        create table Regions (
            regionCode text primary key,
            regionName text not null
        );

        create table Channels (
            channelId       text,
            channelName     text,
            creationDate    text,
            country         text,
            viewCount       integer,
            subscriberCount integer,
            videoCount      integer,
            extractionDate  text,
            
            primary key(channelId, extractionDate)
        );

        create table Videos (
            videoId        text,
            videoTitle     text,
            publishedDate  text,
            channelId      text,
            viewCount      integer,
            likeCount      integer,
            commentCount   integer,
            language       text,
            trendedRegion  text,
            extractionDate text,

            primary key(videoId, trendedRegion, extractionDate),
            foreign key (channelId)
                references Channels (channelId)
        );
    '''
    # Execute the above script
    cursor.executescript(query)

    # Since the regions are only inserted when the database is first created, this next insertion query only
    # Happens after the creation of the tables, and not with the other insertions
    query = '''
        insert into Regions values (?, ?);
    '''
    # Execute the query on the many values of the region list of records and commit the changes
    cursor.executemany(query, regions)
    conn.commit()


def insert_records(conn, cursor, videos, channels, now):
    # Insert the values to the database
    query = '''
        insert into Dates values (?);
    '''
    cursor.execute(query, (now,))

    query = '''
        insert into Videos values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    cursor.executemany(query, videos)

    query = '''
        insert into Channels values (?, ?, ?, ?, ?, ?, ?, ?);
    '''
    cursor.executemany(query, channels)

    conn.commit()


def load(regions, videos, channels, now):
    # Initialize the database connection and cursor
    conn, cursor = initialize()

    # Convert all the dataframes into records (list of tuples that represent each row)
    regions = regions.to_records(index=False)
    videos = videos.to_records(index=False)
    channels = channels.to_records(index=False)

    # Create the tables and insert  the values into them
    create_tables(conn, cursor, regions)
    insert_records(conn, cursor, videos, channels, now)
