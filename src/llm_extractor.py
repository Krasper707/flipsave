from pydantic import BaseModel, Field
from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

class ExtractedInfo(BaseModel):
    """A structured representation of information extracted from a financial text."""
    
    transaction_type: str = Field(
        description="The primary type of the message. Must be one of: 'Offer', 'Debit', 'Credit', 'Receipt', 'Info'."
    )
    vendor: Optional[str] = Field(
        description="The merchant, bank, or company name mentioned (e.g., Zomato, HDFC Bank, Amazon)."
    )
    amount: Optional[float] = Field(
        description="The monetary value of the transaction if present."
    )
    offer_details: Optional[str] = Field(
        description="A summary of the promotional offer if one exists (e.g., '50% off up to Rs. 100')."
    )
    coupon_code: Optional[str] = Field(
        description="The specific promotional code to be used (e.g., 'FLIP50')."
    )
    expiry_date: Optional[str] = Field(
        description="The expiration date of an offer or voucher, formatted as YYYY-MM-DD."
    )
    category: str = Field(
        description="A relevant spending category for the transaction or offer. Must be one of: 'Food & Dining', 'Shopping', 'Travel', 'Bills & Utilities', 'Groceries', 'Entertainment', 'Finance', 'Other'."
    )


load_dotenv()

def get_llm():
    """Initializes and returns the shared Gemini LLM model."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        convert_system_message_to_human=True
    )
    return llm

def create_extraction_chain():
    """
    Initializes and returns a Langchain chain configured for financial text extraction using Google Gemini.
    This version includes a retry mechanism for robustness.
    """
    
    llm = get_llm()
    
    parser = PydanticOutputParser(pydantic_object=ExtractedInfo)
    
    prompt_template = """
    You are an expert system designed to extract structured information from unstructured financial text messages.
    Analyze the text provided by the user and extract the relevant details.
    
    Adhere strictly to the following JSON schema for your response:
    {format_instructions}
    
    Here is the text you need to analyze:
    "{text_input}"
    """
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["text_input"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | llm | parser
    
    chain_with_retries = chain.with_retry(stop_after_attempt=2)
    
    return chain_with_retries
if __name__ == '__main__':
    extraction_chain = create_extraction_chain()
    
    test_texts = [
        "Your a/c XXX123 has been debited for Rs. 550.00 on 25-Nov-23 at ZOMATO.",
        "EXCLUSIVE OFFER: Get 40% OFF up to Rs. 120 on your next Myntra order. Use code STYLEUP40. Valid till 30-Nov.",
        "Your Amazon.in order for 'Wireless Mouse' for Rs. 1,299.00 has been shipped."
    ]
    
    print("--- Testing FlipSave Extraction Chain ---")
    for i, text in enumerate(test_texts):
        print(f"\n--- Test Case {i+1} ---")
        print(f"Input Text: {text}")
        
        result = extraction_chain.invoke({"text_input": text})
        
        print("Extracted Info:")
        print(result.model_dump_json(indent=2))
