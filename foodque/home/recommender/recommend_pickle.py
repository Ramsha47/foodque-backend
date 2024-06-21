import pandas as pd
import numpy as np
import heapq
from collections import defaultdict
from operator import itemgetter
from surprise import Dataset, Reader
from surprise.prediction_algorithms import SVD
import mysql.connector
import pickle

def recommender(userid, user_info, calorie_range=None):
    # Define the functions used inside the recommender function
    def check_user_exists(user_id, review_df, user_df):
        if user_id not in user_df['UserId'].values:
            return "User doesn't exist"
        user_reviews = review_df[review_df['AuthorId'] == user_id]
        if len(user_reviews) < 15:
            return 'Not enough User data' 
        else:
            return 'exist'
            
    def coldstart(reviews, nof_popular=70, nof_random=50):
        popular_recipes = reviews['RecipeId'].value_counts().reset_index()
        popular_recipes.columns = ['RecipeId', 'Rating']
        popular_recipes = popular_recipes.sort_values(by='Rating', ascending=False)
        top_popular_recipes = popular_recipes.head(nof_popular)
        popular_recipe_ids = set(top_popular_recipes['RecipeId'])
        random_recipe_ids = set(reviews['RecipeId'].sample(n=nof_random, random_state=42))
        random_recipe_ids = random_recipe_ids - popular_recipe_ids
        combined_recipe_ids = list(popular_recipe_ids) + list(random_recipe_ids)
        np.random.shuffle(combined_recipe_ids)
        random_recipes_df = pd.DataFrame({'RecipeId': combined_recipe_ids})
        random_recipes_df['Rating'] = 0
        random_recipes_df.loc[random_recipes_df['RecipeId'].isin(popular_recipe_ids), 'Rating'] = top_popular_recipes['Rating']
        return random_recipes_df

    def filter_recipes(recipes, calorie_range):
        filtered_recipes = recipes.copy()
        if calorie_range is not None:
            filtered_dfs = []
            for i in calorie_range:
                filtered_dfs.append(filtered_recipes[filtered_recipes['Calorie_Range'] == i])
            filtered_recipes = pd.concat(filtered_dfs)
        return filtered_recipes

    def get_Calorie_Range(goal):
        templist = []
        if goal:
            if goal == 'lose':
                templist.append('Low')
            elif goal == 'maintain':
                templist.extend(['Low', 'Medium'])
            elif goal == 'gain':
                templist.extend(['Low', 'Medium', 'High'])
            return templist
        else:
            raise ValueError("Goal cannot be empty.")

    def load_data_from_database(table_name, columns=None):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="food"
        )
        cursor = conn.cursor()
        if columns is None:
            query = f"SELECT * FROM {table_name}"
        else:
            columns_str = ', '.join(columns)
            query = f"SELECT {columns_str} FROM {table_name}"
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        conn.commit()
        cursor.close()
        conn.close()
        return df

    def get_topn(trainset, algo, userid, k=10, nof_simusers=10):
        algo.fit(trainset)
        topN = defaultdict(list)
        simsMatrix = algo.compute_similarities()
        uiid = trainset.to_inner_uid(userid)
        similarityRow = simsMatrix[uiid]
        similarUsers = [(innerID, score) for innerID, score in enumerate(similarityRow) if innerID != uiid]

        if len(similarUsers) >= nof_simusers:
            kNeighbors = heapq.nlargest(k, similarUsers, key=lambda t: t[1])
            candidates = defaultdict(float)
            for innerID, userSimilarityScore in kNeighbors:
                for rating in trainset.ur[innerID]:
                    candidates[rating[0]] += (rating[1] / 5.0) * userSimilarityScore
                
            watched = {itemID: 1 for itemID, rating in trainset.ur[uiid]}
            pos = 0
            for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
                if itemID not in watched:
                    movieID = trainset.to_raw_iid(itemID)
                    topN[int(trainset.to_raw_uid(uiid))].append((int(movieID), ratingSum))
                    pos += 1
                    if pos >= k:
                        break

        return topN if topN else False

    def get_toprec(candidates):
        all_items = {}
        for result in candidates:
            for user_id, items in result.items():
                for item_id, score in items:
                    all_items.setdefault(item_id, []).append(score)
        
        average_items = {}
        for item_id, scores in all_items.items():
            average_score = sum(scores) / len(scores)
            average_items[item_id] = average_score
        
        sorted_items = sorted(average_items.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_items

    def generate_recommendations(userid, review_df, df200k, user_df):
        topN = []
        recommend = []
        coldstart_flag = check_user_exists(userid, review_df, user_df)
        if coldstart_flag == 'exist':
            for name in df200k:
                columns_to_fetch = ['AuthorId', 'RecipeId', 'Rating']
                df = load_data_from_database(name, columns_to_fetch)
                if not (df['AuthorId'] == userid).any():
                    user_data = review_df[review_df['AuthorId'] == userid][['AuthorId', 'RecipeId', 'Rating']]
                    df = pd.concat([df, user_data], ignore_index=True)

                reader = Reader(rating_scale=(0, 5))
                data = Dataset.load_from_df(df, reader)
                trainSet = data.build_full_trainset()

                algo = SVD(n_factors=50, reg_all=0.1, lr_all=0.005, n_epochs=100)
                algo.fit(trainSet)

                topN.append(get_topn(trainSet, algo, userid, k=30, nof_simusers=10))
                recommend.extend(get_toprec(topN))

        else:
            nof_popular = 70
            nof_random = 50
            recommend = coldstart(review_df, nof_popular, nof_random)

        return recommend, coldstart_flag

    def filtered_recommendations(userid, user_info, calorie_range):
        columns_to_fetch = ['AuthorId', 'RecipeId', 'Rating']
        review_df = load_data_from_database('reviews', columns_to_fetch)
        columns_to_fetch = ['UserId']
        user_df = load_data_from_database('users', columns_to_fetch)
        df200k = ['batch_1', 'batch_2', 'batch_3', 'batch_4', 'batch_5']
        recommendations, coldstart_flag = generate_recommendations(userid, review_df, df200k, user_df)
        
        df = load_data_from_database('recipes', None)
        if coldstart_flag == 'exist':
            recommendations = pd.DataFrame(recommendations, columns=['RecipeId', 'Rating'])
            
        filtered_df = pd.merge(df, recommendations, on='RecipeId')
    
        calorie_range = get_Calorie_Range(user_info['user_weight_goal'])
        filtered_recipes = filter_recipes(filtered_df, calorie_range)

        if coldstart_flag == "User doesn't exist":
            return False, False, coldstart_flag
            
        return user_info, filtered_recipes, coldstart_flag

    user_info, filtered_recipes, coldstart_flag = filtered_recommendations(userid, user_info, calorie_range)
    return user_info, filtered_recipes, coldstart_flag

functions = {'recommender': recommender}

# Specify the file path for saving the serialized functions
dump_file_path = 'recommender_function.pkl'

# Serialize and save the functions to the file
with open(dump_file_path, 'wb') as f:
    pickle.dump(functions, f)
