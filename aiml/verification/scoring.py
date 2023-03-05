from datetime import datetime
def score_profile(profile):
    # baseline score of 800
    # max score of 3000
    profile['interest_len'] = len(profile['interest'])
    profile['profile_age'] = ((profile['created_at'] - datetime.now()).total_seconds())/(60*60)
    score=0
    if profile['is_verified']:
        score+=0.3
    if profile['profile_age']<24:
        score+=0.4
    elif profile['profile_age']>24:
        score+=0.1
    if profile['is_subscribed']:
        score+=0.5
    if profile['face_detection_probs']>90:
        score+=0.25
    score += profile['interest_len']*0.1
    return score

def get_score(user):
    profile={
        'is_verified':user.id_is_verified,
        'status':user.status,
        'is_subscribed':user.premium,
        'face_detection_probs':user.face_detection_probablity,
        'interest':user.interests.all(),
        'created_at':user.date_joined
    }
    return score_profile(profile)