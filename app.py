








import streamlit as st
import pickle
import pandas as pd
import requests

# --- Function to fetch poster from TMDb by movie title ---
def fetch_poster_by_title(title):
    api_key = "976b276ecf310bf8db66270ad372aecb"
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
    response = requests.get(search_url).json()
    results = response.get("results")
    if results:
        poster_path = results[0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# --- Load movie data ---
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# --- Recommendation function ---
def recommend(movie, num_recommend):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_recommend+1]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        
        recommended_movies_posters.append(fetch_poster_by_title(title))  # Fetch poster by title
    return recommended_movies, recommended_movies_posters

# --- Streamlit form ---
with st.form(key="movie_form"):
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        selected_movie = st.selectbox(
            "Search a movie",
            movies['title'].values,
            help="Type movie name or select from dropdown"
        )
    with col2:
        num_recommend = st.number_input(
            "Number",
            min_value=1,
            max_value=20,
            value=3
        )
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.form_submit_button("Recommend")

# # --- Show recommendations ---
# if submit_button:
#     names, posters = recommend(selected_movie, num_recommend)
#     for name, poster in zip(names, posters):
#         st.write(name)
#         if poster:
#             st.image(poster, width=150)

# # --- Optional tabs ---
# tab1, tab2 = st.tabs(["Top Picks", "Trending"])
# with tab1:
#     st.write("")
# with tab2:
#     st.write("")




# --- Display recommendations in a responsive grid ---
if submit_button:
    titles, posters = recommend(selected_movie, num_recommend)
    st.write(f"Recommendations for **{selected_movie}**")

    # Determine number of columns dynamically
    num_cols = 5  # Adjust number of items per row
    rows = (len(titles) + num_cols - 1) // num_cols  # Ceiling division

    for r in range(rows):
        row_titles = titles[r*num_cols:(r+1)*num_cols]
        row_posters = posters[r*num_cols:(r+1)*num_cols]
        cols = st.columns(len(row_titles))
        for idx, (title, poster) in enumerate(zip(row_titles, row_posters)):
            with cols[idx]:
                if poster:
                    st.image(poster, use_container_width=True)
                st.caption(f"**{title}**")  # Nice title below poster

# Optional tabs for extra content
tab1, tab2 = st.tabs(["Top Picks", "Trending"])
with tab1:
    st.write("")
with tab2:
    st.write("")





















# import streamlit as st 
# import pickle
# import pandas as pd 
# import requests


# def fetch_poster(movie_id):
#     api_key = "976b276ecf310bf8db66270ad372aecb"
#     movie_id = [0]
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
#     response = requests.get(url).json()
#     results = response.get("results")
#     if results:
#         poster_path = results[0].get("poster_path")
#         if poster_path:
#             return f"https://image.tmdb.org/t/p/w500{poster_path}"
#     else:
#         return None

# # laod 2 files
# movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)

# # selected_movie = st.multiselect(
# #     "Pick multiple movies you like",
# #     movies['title'].values,
# #     help="Select one or more movies to improve recommendation"
# # )

# # defining recommend function
# def recommend(movie, num_recommend):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)),reverse=True, key = lambda x:x[1])[1:num_recommend+1] # we can remove [0] as we did it n `distance`

#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]]["id"]))
#     return recommended_movies, recommended_movies_posters

# # Form for input
# with st.form(key="movie_form"):
#     col1, col2, col3 = st.columns([3, 1, 1])

#     with col1:
#         selected_movie = st.selectbox(
#             "Search a movie",
#             movies['title'].values,
#             help="Type movie name or select from dropdown"
#         )
#     with col2:
#         num_recommend = st.number_input(
#             "Number",
#             min_value=1,
#             max_value=20,
#             value=5
#         )
#     with col3:
#         # Add some top padding to push the button down
#         st.markdown("<br>", unsafe_allow_html=True)
#         submit_button = st.form_submit_button("Recommend")

# if submit_button:
#     names, posters = recommend(selected_movie, num_recommend)
#     for name, poster in zip(names, posters):
#         st.write(name)
#         if poster:
#             st.image(poster, width=150)
# ### layout your app



# tab1, tab2 = st.tabs(["Top Picks", "Trending"])
# with tab1:
#     st.write("")
# with tab2:
#     st.write("")
