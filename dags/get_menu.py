import requests
from configparser import ConfigParser
import json
import logging
    
    
def get_menu(year, week, session=None):
    """
    retrieve all recipes for the specified week menu by calling API and save the json object into a file 
    """
    if not session:
        session = requests.Session()
        
    # read config file
    cp = ConfigParser()
    cp.read("config.ini")

    # get url from config file
    url = cp["menu_api"]["url"]
    outfile = cp["other"]["json_out_fname"]

    # API call to read weekly menu
    try:
        response = session.get(url + "{0}-W{1}".format(year, week))
    except requests.exceptions.HTTPError as e:
        logging.error("Http Error:%s",e)
    except requests.exceptions.ConnectionError as e:
        logging.error("Connection Error:%s",e)
    except requests.exceptions.Timeout as e:
        logging.error("Timeout Error:%s",e)
    except requests.exceptions.RequestException as e:
        logging.error("%s",e)
    else:
        if response.ok:
            try:
                # read JSON object
                data = response.json()
            except json.decoder.JSONDecodeError as e:
                logging.error("JSON Decode Error:%s",e)
            else:
                logging.info("Weekly menu retieved.")
                
                with open(outfile, 'w') as f:
                    json.dump(data, f)
        else:
            logging.error("Error 404:Page not found.")
