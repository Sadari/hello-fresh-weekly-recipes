import unittest
import pandas as pd
import os
import requests_mock
from configparser import ConfigParser
import requests
import sys
sys.path.append('../')


from datetime import date
from dags.get_menu import get_menu
from dags.read_recipes import read_recipes, get_top_recipes
from dags.upload_to_s3 import upload_to_s3


class Test_Weekly_Menu(unittest.TestCase):

    def setUp(self):        
        with open("response.json", "r") as response_file:
            mock_response = response_file.read()
        
        self.adapter = requests_mock.Adapter()
        self.session = requests.Session()
        self.session.mount('mock://', self.adapter)

        self.adapter.register_uri('GET', 'mock://hellofresh-au.free.beeceptor.com/menus/2021-W30',
                                  text=mock_response)
           

    def test_get_menu(self):
        if os.path.exists("out.json"):
            os.remove("out.json")
            
        year = 2021
        week = 30
    
        get_menu(year, week, self.session)
        self.assertTrue(os.path.exists("out.json"))
            
    
    def test_get_top_recipes(self):
        name = ['BBQ Chicken','Veggie','Mexican Beef','Cheeseburger','Garlic Fish']
        ratingsCount = [25,34,12,6,25]
        favoritesCount = [2,4,7,10,5]
        recipes = pd.DataFrame(list(zip(name,ratingsCount,favoritesCount)),
                          columns = ["Name","RatingsCount","FavoritesCount"])
 
        expected_df = recipes.iloc[[1,4,0],:]

        params = {"names": ["RatingsCount","FavoritesCount"],
                  "order": [False, False]
                  }
        top_recipes = get_top_recipes(recipes, sort_params=params, count=3)

        pd.testing.assert_frame_equal(expected_df, top_recipes)


    def test_read_recipes(self):
        """
        check the two csv files created by ETL process
        """

        # delete the existing csv files
        if os.path.exists("2021_30_menu.csv"):
            os.remove("2021_30_menu.csv")

        if os.path.exists("2021_30_TOP_10.csv"):
            os.remove("2021_30_TOP_10.csv")
        
        year = 2021
        week = 30
    
        read_recipes(year, week)

        self.assertTrue(os.path.exists("2021_30_menu.csv"))
        self.assertTrue(os.path.exists("2021_30_TOP_10.csv"))


if __name__ == "__main__":
     unittest.main()
    
