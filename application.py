import streamlit as st
from src.scrapper import FlipkartReviewsScrapping, AmazonReviewsScrapping


# User interface
st.header("Product reviews from Ecommerce websites!")

# User inputs
st.sidebar.subheader('User Inputs:')
ecom_website = st.sidebar.selectbox(label="Which platform are you looking for?", options=('Flipkart', 'Amazon'))
search_item = st.sidebar.text_input('Which product are you looking for?')

# Results
if ecom_website == 'Flipkart':
    scrapper = FlipkartReviewsScrapping()
    results = scrapper.get_reviews(search_item=search_item)

    product_name, link = results[0]['product_name'], results[0]['product_page']
    st.write(f'The product is: {product_name}')

    st.write('Reviews:')
    for item in results[1:]:
        st.table(item)

