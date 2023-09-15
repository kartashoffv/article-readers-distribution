from transformers import pipeline
import codecs

from info import *

def get_cats_from_texts(text_lst : list):
    pipe = pipeline("text-classification", model="kartashoffv/news_topic_classification")
    output_cats = []
    max_length = 510
    
    for text in text_lst:
        if len(text) > max_length:
            text = text[:max_length]
        output_cats.append(text)
    
    result = [pipe(txt)[0]['label'] for txt in output_cats]
    
    return result


def calculate_distribution(total_users, cat_distribution):
    categories = cat_distribution.keys()
    users = {}
    
    for category, percentage in cat_distribution.items():
        users[category] = int(total_users * (percentage / 100))
    
    return users


total_men = vedomosti_info["monthly_unique_visitors"] * vedomosti_info['gender_distribution']["Male"] / 100 
total_women = vedomosti_info["monthly_unique_visitors"] * vedomosti_info['gender_distribution']["Female"] / 100 

income_distribution = vedomosti_info['age_distribution']
total_users_age_distribution = calculate_distribution(total_men + total_women, income_distribution)


age_dist = {}
total_views = []

def get_distribution(topic):
    topic = topics_info[topic]
    
    age = {}
    sex = {}
    money = {}
    education = {}
    views = 0
    
    for k, v in topic["age_distribution"].items():
        age_dist[k] = int(total_users_age_distribution[k] * (v / 100))
        age[k] = age_dist[k] 
        total = sum(age.values())
        normalized_age = {key: round(value / total, 5) for key, value in age.items()}
        views+=int(total_users_age_distribution[k] * (v / 100)) 
    for k, v in topic["gender_distribution"].items():
        sex[k] = dict(map(lambda x: (x[0], int(x[1] * (v / 100))), age_dist.items()))
        normalized_sex = {gender: {key: round(value / total, 5) for key, value in values.items()} for gender, values in sex.items()}
    for k, v in topic["income_level_distribution"].items():
        money[k] = dict(map(lambda x: (x[0], int(x[1] * (v / 100))), age_dist.items()))
        normalized_income_level = {income: {key: round(value / total, 5) for key, value in values.items()} for income, values in money.items()}
    for k, v in topic["education_level"].items():
        education[k] = dict(map(lambda x: (x[0], int(x[1] * (v / 100))), age_dist.items()))
        normalized_education_level = {education: {key: round(value / total, 5) for key, value in values.items()} for education, values in education.items()}
    
    return normalized_age, normalized_sex, normalized_income_level, normalized_education_level, views

def get_output_distributions(texts):
    texts = [codecs.decode(text, 'unicode-escape').encode('utf-8').decode('utf-8') for text in texts]
    distributions = []
    cats = get_cats_from_texts(texts)
    
    for cat in cats:
        age, sex, income_level, normalized_education_level, views = get_distribution(cat)
        
        distributions.append({cat : {
                "age" : age,
                "sex" : sex,
                "income_level" : income_level,
                "education_level" : normalized_education_level,
                "views" : views
            }})
        
    return distributions



