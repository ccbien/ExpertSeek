import streamlit as st
from request import *

if "authors" not in st.session_state:
    st.session_state.authors = []
if "author" not in st.session_state:
    st.session_state.author = None

st.sidebar.title("Search Panel")

    

name_query = st.sidebar.text_input("Enter name:")
org_query = st.sidebar.text_input("Enter organization:")

def click_search():
    st.session_state.authors = search_authors(name_query, org_query)
    
search_button = st.sidebar.button(
    "Search",
    on_click=click_search,
    type="primary",
)


text_query = st.sidebar.text_input("Enter keywords, topics, etc.")

def click_search_kw():
    st.session_state.authors = search_authors_kw(text_query)
    
search_kw_button = st.sidebar.button(
    "Search with keywords",
    on_click=click_search_kw,
    type="primary",
)

if st.session_state.authors:
    st.sidebar.subheader("Results")
    st.session_state.author = None

    for author in st.session_state.authors:
        if st.sidebar.button(
            author["name"],
            key="side_" + author["author_id"],
            use_container_width=True,
        ):
            st.session_state.author = author

if st.session_state.author is not None:
    st.title(st.session_state.author["name"])
    st.header("Top co-authors")
    coauthors = get_top_coauthor(st.session_state.author["author_id"])
    for author in coauthors:
        st.markdown(f"{author['name']}, *{author['org']}*")
    
    papers = get_all_paper(st.session_state.author["author_id"])
    papers.sort(key=lambda item: -item["year"])
    st.header(f"Publications ({len(papers)})")
    for paper in papers:
        st.markdown(f"**[{paper['year']}]** {paper['title']}")
        st.markdown(f"**DOI:** [{paper['doi']}](https://doi.org/{paper['doi']})")
        st.markdown("---------------------------------------------------")