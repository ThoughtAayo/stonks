from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def extract_structured_data(content: str):
    """Extract structured info from text via LLM"""
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    template = """
    You are an expert finance analyst who will extract core information from the given content and provide financial analysis. 
    Please be specific to the given data. Group analysis to titles and return in the format of json where the key is the topic of analysis and key is the analysis itself.
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