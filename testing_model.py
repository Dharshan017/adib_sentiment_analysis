import pandas as pd
import re
import nltk
import spacy
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from autocorrect import Speller
# nltk.download("wordnet")
# nltk.download("punkt")
# nltk.download('averaged_perceptron_tagger')
# nltk.download('vader_lexicon')
# nltk.download('stopwords')
sp = spacy.load('en_core_web_sm')

from pyabsa import ATEPCCheckpointManager
aspect_extractor = ATEPCCheckpointManager.get_aspect_extractor(checkpoint='english',auto_device=False)

# trust_pilot_rev = pd.read_excel(r"D:\adib_sentiment_analysis\trust_pilot_rev.xlsx")

def get_aspect_sentiment_old(review):
    lmtzr = WordNetLemmatizer()
    review = review.replace('mr.', 'mr ')
    loan = ["loan", "mortgage", "finance", "loans", "mortgages", "murahaba"]
    card = ["card", "credit card", "cards"]
    customer_service = ['customer service','tellers', 'manager','rep', 'representative', 'customer_care',"service", "employees", "employee","call","calls", "staff", "call centre", "executive", "services", "executive" ]
    
    products = [loan, card, customer_service]
    
    split_rev = re.split("\\.|\n| but ", review)
    split_rev =  list(filter(None, split_rev))

    inference_source = split_rev
    atepc_result = aspect_extractor.extract_aspect(inference_source=inference_source, pred_sentiment=True)
    
    review_aspect = []


    for index, prd in enumerate(products):
            res = any(ele in review for ele in prd)
            if res:
                review_aspect.append(prd[0])
                

    for index in range(len(atepc_result)):
        review_aspect.extend(atepc_result[index]["aspect"])        
        review_aspect = [lmtzr.lemmatize(word) for word in review_aspect] 
        review_aspect = list(set(review_aspect))
        review_aspect = ["customer service" if x=="service" or x == "customer" else x for x in review_aspect]
        pos_tagged_tokens = nltk.pos_tag(review_aspect)
        for i in range(len(pos_tagged_tokens)):
            if pos_tagged_tokens[i][1].startswith('PRP'):
              review_aspect.remove(pos_tagged_tokens[i][0])  
    print(review_aspect,"*"*100)
    return str(review_aspect)

    
lmtzr = WordNetLemmatizer()
def get_aspect_sentiment(review):
    review = review.lower()
    review = review.replace('mr.', 'mr ')
    loan = ["loan", "mortgage", "finance", "loans", "mortgages", "murahaba"]
    card = ["card", "credit card", "cards"]
    customer_service = ['customer service','tellers', 'manager','rep', 'representative', 'customer_care',"service", "employees", "employee","call","calls", "staff", "call centre", "executive", "services", "executive" ]
    products = [loan, card, customer_service]
    split_rev = re.split("\\.|\n| but ", review)
    split_rev =  list(filter(None, split_rev))
    inference_source = split_rev
    atepc_result = aspect_extractor.extract_aspect(inference_source=inference_source, pred_sentiment=True, save_result=False,
                                               print_result=False )
    review_aspect = []
    for index, prd in enumerate(products):
            res = any(ele in review for ele in prd)
            if res:
                review_aspect.append(prd[0])
    for index in range(len(atepc_result)):
        review_aspect.extend(atepc_result[index]["aspect"])   
    review_aspect = [lmtzr.lemmatize(word) for word in review_aspect] 
    review_aspect = ["customer service" if x=="service" or x == "customer" else x for x in review_aspect]
    pos_tagged_tokens = nltk.pos_tag(review_aspect)
    for i in range(len(pos_tagged_tokens)):
        if pos_tagged_tokens[i][1].startswith('PRP'):
          review_aspect.remove(pos_tagged_tokens[i][0])  
    review_aspect = list(set(review_aspect))
    return str(review_aspect)
# trust_pilot_rev['review_aspect'] = trust_pilot_rev.apply(lambda x: get_aspect_sentiment(x['Review']),axis=1)

# topic = get_aspect_sentiment("""service is horrible""")
# print(topic)

analyzer = SentimentIntensityAnalyzer()
analyzer.constants.NEGATE.add("no")
new_words = {'please': 0,'blocked':-4,'block':-4,'dishonesty':-2,'shocking':-3,'waiting' :-4,'debit': -3,'credit':0,'deduct':-3,'deductions':-3,'deducted':-3,'outdated':-3,'crowded':-2,'slow':-4,'slowest':-4,'joke':0,'issue':-3,'hacked':-3,'understand':1, 'want':0, 'convince':0, 'fee':-1, 'fees':-1, "breaking":-3, "acknowledged": 1,  'acknowledge':1, 'zero':-4}
analyzer.lexicon.update(new_words)
# analyzer.lexicon.pop('no')

spell1 = Speller()
spell1.nlp_data.update({"ADIB":10000, "Abu Dhabi": 10000, "ADIB": 10000, "adib":10000})



def clean_txt_for_sentiment(review):
    review = review.lower().strip()
    review = re.sub(r'[^\x00-\x7F]+', '', review)
    review_corrected = re.sub(r'(.)\1{2,}', r'\1\1', review)
    review_corrected = re.sub('mr.','mr', review_corrected)
    review_corrected = re.sub('customer care', 'customer_care', review_corrected)
    review_corrected = re.sub('credit card', 'credit_card', review_corrected)
    review_corrected = re.sub('debit card', 'debit_card', review_corrected)
    return review_corrected

def get_sentiment(review):
    review = clean_txt_for_sentiment(review)
    sentiment = analyzer.polarity_scores(review)
    compound_score = sentiment['compound']
    positive_score = sentiment['pos']
    negative_score = sentiment['neg']
    neutral_score = sentiment['neu']
    if compound_score <0:
        sentiment = "Negative"
    elif compound_score ==0:
        sentiment = "Neutral"
    elif compound_score >0:
        sentiment = "Positive"
    return [compound_score,positive_score, negative_score, neutral_score, sentiment]

# trust_pilot_rev[['overall_sentiment_score', 'positive_score', 'negative_score', 'neutral_score', 'sentiment']] = trust_pilot_rev.apply(lambda x: get_sentiment(x['Review']),axis=1,result_type='expand')

# get_sentiment("Service is goooooood by mr. Mohmd for credit card dept in ABID")



def remove_stopwords(x):
    cachedStopWords = sp.Defaults.stop_words
    cachedStopWords = [x.lower() for x in cachedStopWords]
    cachedStopWords.append("bank")
    cachedStopWords.append("adib")
    cachedStopWords.extend(list(stopwords.words('english')))
    cachedStopWords = list(set(cachedStopWords))
    meaningful_words = []
    my_list = x
    tokenized_my_list = word_tokenize(my_list) 
    meaningful_words = [w for w in tokenized_my_list if not w in cachedStopWords]
    return " ".join(meaningful_words)

def get_ngrams(text, n=2):
    text = str(text)
    n_grams = ngrams(text.split(), n)
    returnVal = []
    try:
        for grams in n_grams:
            returnVal.append('_'.join(grams))
    except(RuntimeError):
        pass
    return ' '.join(returnVal).strip()

def word_count(df):
    df['Review_word_cloud'] = df['Review'].str.lower()
    df['Review_word_cloud'] = df['Review_word_cloud'].apply(remove_stopwords)
    df['Review_word_cloud'] = df['Review_word_cloud'].str.replace('[^\w\s]','')
    df["unigram_text"] = df["Review_word_cloud"].apply(get_ngrams, n=1)
    word_cloud = df["unigram_text"].str.replace('\d+', '').str.split(expand=True).stack().value_counts().reset_index()
    word_cloud.columns = ['Word', 'Frequency'] 
    word_cloud['Sentiment'] = word_cloud['Word'].apply(lambda review: get_sentiment(review)[0])
    sentiment_df = word_cloud[word_cloud['Sentiment']!=0]
    topic_df = word_cloud[word_cloud['Sentiment']==0]
    return sentiment_df, topic_df

# a,b =  word_count(trust_pilot_rev)


def process_file(review_df):
    review_df['review_aspect'] = review_df.apply(lambda x: get_aspect_sentiment(x['Review']),axis=1)
    review_df[['overall_sentiment_score', 'positive_score', 'negative_score', 'neutral_score', 'sentiment']] = review_df.apply(lambda x: get_sentiment(x['Review']),axis=1,result_type='expand')
    a,b =  word_count(review_df)
    return review_df,a,b