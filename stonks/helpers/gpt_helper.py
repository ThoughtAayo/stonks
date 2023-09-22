from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def extract_structured_data(content: str):
    """Extract structured info from text via LLM"""
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    template = """
    You are an expert finance analyst who will extract core information from the given content and provide financial analysis. 
    The document consist data for multiple quarter and years. Please make sure to capture this information 
    You'll will first extract the information as it is in JSON capturing the multiple quarter and year data.
    Then you'll analyse the data and then append the insights as in a key called "analysis" at top level of the json file.
    Here's the content.
    {content}
    Return ONLY the JSON doc.
    """

    prompt = PromptTemplate(
        input_variables=["content"],
        template=template,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    results = chain.run(content=content)

    return results

def query(dataset: str, question: str):
    """Extract structured info from text via LLM"""
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    template = """
    You are an expert finance analyst who will generate insights based on given dataset. 
    Please answer questions purely based on the dataset without any outside data. If you don't know the answer, output I don't know.
    Here's the data that you'll use to answer the question.
    {content}
    
    Please answer the following question
    {question}
    """

    prompt = PromptTemplate(
        input_variables=["content", "question"],
        template=template,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    results = chain.run(content=dataset, question=question)

    return results