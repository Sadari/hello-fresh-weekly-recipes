import pandas as pd
import json
import logging
import os
from configparser import ConfigParser



def get_top_recipes(df, sort_params=None, count=10):
    """
    sort and retrieve top rows of df
    """
    if not sort_params:
        logging.warning("Column names to soty by are not defined.")
        return df

    return df.sort_values(sort_params["names"],
                                  ascending=sort_params["order"]).head(count)
    
    

def read_recipes(year, week):
    """
    1. parse the json object and extract name, headline, prepTime, ratingsCount, favoritesCount, nutrition and export to a csv file
    2. retrieve top 10 recipes based on ratingsCount, favoritesCount and export to a csv file
    """
    # read config file
    cp = ConfigParser()
    cp.read("config.ini")
    
    # load menu data
    fname_json = cp["other"]["json_out_fname"]
    if not os.path.exists(fname_json):
        logging.error("JSON file not found.")
        return
    
    with open(fname_json) as f:
      menu = json.load(f)
    
    # read recipes: items >> [courses] >> [recipes]
    recipes = []
    for item in menu["items"]:
        for course in item["courses"]:
            recipes.append(course["recipe"])
    logging.info("%d recipes found", len(recipes))

    data = []
    for recipe in recipes:
        recipe_data = []
        recipe_data.append(recipe["name"])
        recipe_data.append(recipe["headline"])
        recipe_data.append(recipe["prepTime"])
        recipe_data.append(recipe["ratingsCount"])
        recipe_data.append(recipe["favoritesCount"])

        # nutritions
        for  i in range(7):
            recipe_data.append(recipe["nutrition"][i]["amount"])

        data.append(recipe_data)

    column_names = ["Name","Headline","PrepTime","RatingsCount","FavoritesCount","Nutrition-Energy(KJ)","Nutrition-Fat",
                "Nutrition-of which saturates","Nutrition-Carbohydrate","Nutrition-of which sugars","Nutrition-Protein","Nutrition-Sodium"]
    df_recipes = pd.DataFrame(data, columns = column_names)

    # save recipe data into csv
    fname_csv = str(year) + "_" + str(week) + "_menu.csv"
    df_recipes.to_csv(fname_csv, index=False)
    logging.info("recipes exported to csv.")
                 

    # extract top 10 recipes based on RatingsCount and FavoritesCount
    params = {"names": ["RatingsCount","FavoritesCount"],
              "order": [False,False]
              }
    df_top_recipes = get_top_recipes(df_recipes, sort_params=params, count=10)

    # save top 10 recipes into csv
    fname_out = str(year) + "_" + str(week) + "_TOP_10.csv"
    df_top_recipes.to_csv(fname_out, index=False)
    logging.info("top 10 recipes exported to csv.")
    
    
