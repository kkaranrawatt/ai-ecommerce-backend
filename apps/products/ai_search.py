from apps.products.models import Product
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore

def semantic_search(query):
    products= Product.objects.all()
    if not products.exists():
        return []
    
    product_texts= []
    product_ids= []
    for product in products:
        text= f"""
        {product.name}
        {product.description}
        {product.category.name}
        """
        product_texts.append(text)
        product_ids.append(product.id)
    
    vectorizer= TfidfVectorizer(stop_words= 'english')
    tfidf_matrix= vectorizer.fit_transform(product_texts)
    query_vector= vectorizer.transform([query])
    similarity_scores= cosine_similarity(query_vector, tfidf_matrix)
    scores= list(enumerate(similarity_scores[0]))
    sorted_scores= sorted(scores, key= lambda x: x[1], reverse= True)

    recommended_ids=[]

    for index, score in sorted_scores[:5]:
        if score > 0:
            recommended_ids.append(product_ids[index])
    return Product.objects.filter(id__in= recommended_ids)
