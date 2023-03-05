import numpy as np
from datetime import date
 
def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

class EloRecommendationSystem:
    def __init__(self, user_features, profiles, k=32): # need to know how to determine k
        self.user_features = user_features
        self.profiles = profiles
        self.k = k

    def predict_scores(self):
        scores = np.full(len(self.profiles), 800) # initializing to 800
        for i, profile in enumerate(self.profiles):
            expected_score = self.calculate_expected_score(self.user_features, profile)
            # calculating expected score for the profile in consideration
            result = self.get_match_result(profile)
            scores[i]+=self.k*(result-expected_score)
        return scores
    
    def get_top_profiles(self, n=10):
        scores = self.predict_scores()
        print('predicted score', scores)
        top_indices = np.argsort(scores)[:n]
        # sort descending order and get top n 
        print('top indices', top_indices,self.profiles)
        return [self.profiles[i]["_id"] for i in top_indices]
    
    def jaccard_similarity(self, list1, list2):
        set1 = set(list1)
        set2 = set(list2)
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)
    
    def calculate_expected_score(self, user_features, profile):
        interest_similarity = self.jaccard_similarity(user_features['interests'], profile['interests'])
        print(interest_similarity)
        expectation = 1 / (1 + np.power(10, (profile['score'] - user_features['score']) / 400))
        print("*"*10)
        print(expectation+interest_similarity*200)
        return expectation+ interest_similarity*200
    
    def get_match_result(self, profile):
        # will get from user

        return 1 if np.random.choice([True, False], p=[0.7,0.3]) else -1
    


def get_close_profiles(user,profiles):
    selfuser = {'id1':user.id,
                 'interests':[i.name for i in user.interests.all()],
                 'gender':user.gender,
                 'who_to_date':user.who_to_date,
                 'is_subscribed': user.premium,
                 'is_habit_drink': user.is_habit_drink,
                 'is_habit_smoke': user.is_habit_smoke,
                'score': user.user_score}
    list_profiles = [ {"_id": i.id, "name": i.name, "age": age(i.dob) , "gender": i.gender, "location": i.country, "interests": [j.name for j in i.interests.all() ], "score": i.user_score} for i in profiles]
    elo_rs = EloRecommendationSystem(selfuser,list_profiles)
    return elo_rs.get_top_profiles()