PROFILE_NAME = "sds"
PROJ_KEY = "628052f6ea6d4f03c8e4f6adc50a8bf98dcc53e6"  # This is the PROJ_KEY for the BCX Hackathon project
INDEX_KEY = "5d0f026fdd28f9d1cf5f0107259214039e8ec287"

RETR_K = 10  # the number of search results to retrieve
TEXT_WEIGHT = 0.1  # the weight of lexical search (0.0: semantic-only, 1.0: lexical-only, anything in between: hybrid search)
RERANK = False
import pandas as pd
import streamlit as st
from deepsearch.cps.client.api import CpsApi
from deepsearch.cps.client.components.elastic import ElasticProjectDataCollectionSource
from deepsearch.cps.queries import DataQuery, CorpusRAGQuery, CorpusSemanticQuery
from deepsearch.cps.queries.results import RAGResult, SearchResult, SearchResultItem
from deepsearch.cps.client.components.documents import SemIngestPrivateDataCollectionSource

api = CpsApi.from_env(profile_name=PROFILE_NAME)

def render_provenance_url(api: CpsApi, coords: ElasticProjectDataCollectionSource, retr_item: SearchResultItem):
    item_index = int(retr_item.path_in_doc[retr_item.path_in_doc.rfind(".") + 1:])
    doc_url = api.documents.generate_url(document_hash=retr_item.doc_hash, data_source=coords, item_index=item_index)
    return doc_url

coll_coords = ElasticProjectDataCollectionSource(proj_key=PROJ_KEY, index_key=INDEX_KEY)

# Streamlit UI
st.title("DeepSearch Query Interface")

question = st.text_input("Enter your question:", "How to fix?")

if st.button("Submit"):
    question_query = CorpusRAGQuery(question=question, project=PROJ_KEY, index_key=INDEX_KEY)
    api_output = api.queries.run(question_query)
    rag_result = RAGResult.from_api_output(api_output)

    if rag_result.answers:
        st.write("Answer:", rag_result.answers[0].answer)
        st.write("Context:", rag_result.answers[0].grounding.items[0].passage)
        # Optionally, display the provenance URL if needed
        provenance_url = render_provenance_url(api, coll_coords, rag_result.answers[0].grounding.items[0])
        st.write("Provenance URL:", provenance_url)
    else:
        st.write("No answer found.")