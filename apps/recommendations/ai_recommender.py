from apps.products.models import Product
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_ai_recommendations(product_id):
    products= Product.objects.all()

    if not products.exists():
        return []
    
    product_data= []
    product_ids= []

    for product in products:
        text= f"{product.name} {product.description} {product.category.name}"

        product_data.append(text)
        product_ids.append(product.id)
    
    vectorizer= TfidfVectorizer(stop_words= 'english')
    tfidf_matrix= vectorizer.fit_transform(product_data)
    similarity_matrix= cosine_similarity(tfidf_matrix)

    try:
        target_index= product_ids.index(product_id)
    except ValueError:
        return []
    
    similarity_scores= list(enumerate(similarity_matrix[target_index]))

    sorted_products= sorted(similarity_scores, key= lambda x: x[1], reverse= True)

    recommended_ids= []

    for index, score in sorted_products[1:6]:
        recommended_ids.append(product_ids[index])
    recommended_products= Product.objects.filter(id__in= recommended_ids)
    return recommended_products