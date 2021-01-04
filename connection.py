#the connection between database and our server
import os
import psycopg2
import urllib




# We create a cursor of type RealDictCursor, thus it returns "real-indexed dictionaries", 
# which basically behave as lists of dictionaries, where within each dictionary,
# the column names are the keys.
from psycopg2.extras import RealDictCursor  # import the type RealDictCursor





def open_database():    
    urllib.parse.uses_netloc.append('postgres')     # uses the postgres syntax for the URI, namely: 
    #                                               # postgres://username:password@host:port/path/to/resource/on/host
    try:
        url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
    except:
        print('Could not find required environment variables!')
        raise OSError

    try:        
        connection = psycopg2.connect(
            database=url.path[1:],  # skip the leading / in the 'path' ?
            user=url.username,  # use the rest of the parsed variables from the URI
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        connection.autocommit = True    # leave True for now, maybe change later if needed
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection



# Creates a decorator to handle the database connection/cursor opening/closing.
#
# This simply says that a cursor (a fancy cursor, provided by psycopg2.extras
# which maps attributes in the PostgreSQL database to keywords in dictionaries) 
# will need to be obtained from a connection (itself obtained from open_database())
# and be discarded and the connection closed once it has been used (in function())
def connection_handler(function):

    # (*args and **kwargs are the convention, but this is for clarity)
    # *unspecified_args can be passed as a tuple
    # **unspecified_keyworded_args can be passed as a dictionary
    def wrapper(*unspecified_args, **unspecified_keyworded_args):

        
        # Begin the pre-block of the wrapper 
        ###### PRE #######
        connection = open_database()

        # we set the cursor_factory parameter to return with 
        # a RealDictCursor cursor (cursor which provides dictionaries)
        dict_cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # End pre-block
        ##### PRE ###########
        
        # The actual function to be wrapped ( named function() ) is used now:
        # any wrapped function() will be expected to have a (formal) argument representing a cursor
        # and which is of the RealDictCursor type (the rest are wildcards/unspecified)
        ret_value = function(dict_cursor, *unspecified_args, **unspecified_keyworded_args)

        # Begin the post-block of the wrapper
        ########## POST ##########
        dict_cursor.close()
        connection.close()
        # End post-block
        ######## POST ##########

        return ret_value

    return wrapper  # wrapper is a function (all decorators should map functions to functions)
    #               # ...but it is a function which returns ret_value