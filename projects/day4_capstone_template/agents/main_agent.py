import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st

# Load Environment
load_dotenv()

class AIAgent:
    """
    Main AI Agent class for the Capstone project.
    
    This agent can be customized with different personalities and behaviors.
    """
    
    def __init__(self, system_prompt: str = None):
        """
        Initialize the AI Agent.
        
        Args:
            system_prompt: Custom system prompt defining agent behavior
        """
        self.system_prompt = system_prompt or "You are a helpful AI assistant."
        self.api_key = self._get_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-flash-lite-latest")
        else:
            self.model = None

    def _get_api_key(self):
        """Get API key from .env or Streamlit secrets."""
        key = os.getenv("GOOGLE_API_KEY")
        if not key:
            try:
                key = st.secrets["GOOGLE_API_KEY"]
            except:
                pass
        return key

    def generate_response(self, user_message: str, context: str = None) -> str:
        """
        Generate a response from the agent.
        
        Args:
            user_message: The user's message
            context: Optional conversation context/history
        
        Returns:
            Agent's response as string
        """
        if not self.model:
            return "Error: API Key not found. Please check your .env file."
        
        # Build prompt with context if provided
        if context:
            full_prompt = f"""
SYSTEM RULES:
{self.system_prompt}

CONTEXT (Previous Conversation):
{context}

USER MESSAGE:
{user_message}

YOUR RESPONSE:
"""
        else:
            full_prompt = f"""
SYSTEM RULES:
{self.system_prompt}

USER MESSAGE:
{user_message}

YOUR RESPONSE:
"""
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}. Please check your API key and internet connection."

    def update_personality(self, new_prompt: str):
        """Update the agent's system prompt/personality."""
        self.system_prompt = new_prompt
