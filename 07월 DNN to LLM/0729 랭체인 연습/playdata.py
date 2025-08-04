from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import bs4
from langchain_community.document_loaders import WebBaseLoader
from urllib.parse import urlparse, parse_qs, urlencode
import requests
import re
from typing import Literal
import json
from tqdm import tqdm

class SentimentArticle(BaseModel):
    sentiment: Literal['긍정', '부정', '중립'] = Field(description="감성분석 분류")
    score: str = Field(description='기사 내용 요약')


import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(dotenv_path="../../.env")
api_key = os.getenv("API_KEY")

model = ChatOpenAI(
    model='gpt-4.1',
    temperature=0,
    api_key=api_key
)

parser = PydanticOutputParser(pydantic_object=SentimentArticle)


prompt_template = """
당신은 뉴스 기사의 감성을 분석하는 AI입니다.
아래 뉴스를 읽고 감성을 '긍정', '부정', '중립' 중 하나로 분류하고, 기사 내용 요약을 json 형식으로 출력하세요.


{format_instructions}


뉴스 기사:
{news_article}
"""
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=['news_article'],
    partial_variables={"format_instructions" : parser.get_format_instructions()}


)
chain = prompt | model | parser


def get_news_sentiment(keyword, ds, de):
    p = re.compile("https://[mn]\.[a-z]+\.naver.com/.+")
    base_url = "https://s.search.naver.com/p/newssearch/3/api/tab/more?cluster_rank=98&de=2025.07.29&ds=2025.07.22&eid=&field=0&force_original=&is_dts=0&is_sug_officeid=0&mynews=0&news_office_checked=&nlu_query=&nqx_theme=%7B%22theme%22%3A%7B%22main%22%3A%7B%22name%22%3A%22people_sports%22%2C%22os%22%3A%22175558%22%2C%22source%22%3A%22NLU%22%2C%22pkid%22%3A%221%22%7D%7D%7D&nscs=0&nso=so%3Ar%2Cp%3A1w%2Ca%3Aall&nx_and_query=&nx_search_hlquery=&nx_search_query=&nx_sub_query=&office_category=0&office_section_code=0&office_type=0&pd=1&photo=0&query=%EC%86%90%ED%9D%A5%EB%AF%BC&query_original=&rev=0&service_area=0&sm=tab_smr&sort=0&spq=3&ssc=tab.news.all&start=61"
    query_dict = parse_qs(urlparse(base_url).query)
    query_dict['query'] = [keyword]
    query_dict['start'] = ['1']
    query_dict['de'] = [de]
    query_dict['ds'] = [ds]
    search_host = "https://s.search.naver.com/p/newssearch/3/api/tab/more?"
    after_url = search_host + urlencode(query_dict, doseq=True)
    requests_json =  requests.get(after_url).json()
    urls = [x['href'] for x in bs4.BeautifulSoup(requests_json['collection'][0]['html']).find_all("a", {'href' : p})]
    loader = WebBaseLoader(web_path=(urls),
                    bs_kwargs=dict(parse_only=bs4.SoupStrainer(
                        'div', attrs={'id' : ['newsct_article']}
                    ))   )
    rt = loader.load()


    total = []
    for news in tqdm(rt):
        response = chain.invoke({'news_article' : news.page_content})
        tmp = json.loads(response.model_dump_json())
        tmp['source'] = news.metadata['source']
        total.append(tmp)


    return total