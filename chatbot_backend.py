#Steps
#1 import the ConversationSummaryBufferMemory, ConversationChain, ChatBedrock (BedrockChat) Langchain Modules
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_aws import ChatBedrock

store = {}  # memory is maintained outside the chain


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
                if session_id not in store:
                    store[session_id] = InMemoryChatMessageHistory()
                    return store[session_id]

                memory = ConversationBufferWindowMemory(
                    chat_memory=store[session_id],
                    k=3,
                    return_messages=True,
                )
                assert len(memory.memory_variables) == 1
                key = memory.memory_variables[0]
                messages = memory.load_memory_variables({})[key]
                store[session_id] = InMemoryChatMessageHistory(messages=messages)
                return store[session_id]

#2a Write a function for invoking model- client connection with Bedrock with profile, model_id & Inference params- model_kwargs
def demo_chatbot():
    demo_llm=ChatBedrock(
       credentials_profile_name='default',
       model_id='anthropic.claude-3-haiku-20240307-v1:0',
       model_kwargs= {
           "max_tokens": 300,
           "temperature": 0.1,
           "top_p": 0.9,
           "stop_sequences": ["\n\nHuman:"]} )
    return demo_llm


#4 Create a Function for Conversation Chain - Input text + Memory
def demo_conversation(input_text):
    llm_chain_data=demo_chatbot()
    # Create a RunnableWithMessageHistory with correct get_session_history function
    llm_conversation = RunnableWithMessageHistory(
        runnable=llm_chain_data, 
        get_session_history=get_session_history  # Pass the function reference here correctly
    )

#5 Chat response using invoke (Prompt template)
    chat_reply=llm_conversation.invoke(
                input_text,
                config={"configurable": {"session_id": "1"}},
            )
    
    # Adjust this depending on the actual structure of chat_reply
    if hasattr(chat_reply, 'content'):
        return chat_reply.content
    else:
        return "No response"  # Default or error message    

