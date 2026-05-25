from apps.products.ai_search import semantic_search

def chatbot_response(message):
    products= semantic_search(message)
    if not products:
        return {
            "message": "No matching products found",
            "products": []
        }
    product_data= []
    for product in products:
        product_data.append({
            "id":product.id,
            "name": product.name,
            "price": str(product.price),
            "category": product.category.name
        })
    return {
        "message": "Recommended products",
        "products": product_data
    }
