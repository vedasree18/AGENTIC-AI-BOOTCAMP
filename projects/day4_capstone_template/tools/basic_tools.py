"""
Basic Tools for the Capstone Agent

Add your custom tools here!
"""

import re
import ast
import operator

def calculator(expression: str):
    """
    Safely evaluates mathematical expressions.
    
    Args:
        expression: Math expression as string (e.g., "5 + 3 * 2")
    
    Returns:
        Result as string
    """
    # Clean input - remove non-math characters
    clean_expr = re.sub(r'[^0-9+\-*/(). ]', '', expression)
    
    if not clean_expr.strip():
        return "Error: Invalid expression"
    
    # Safe operators
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
    }
    
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](_eval(node.operand))
        else:
            raise TypeError(node)
    
    try:
        tree = ast.parse(clean_expr, mode='eval')
        result = _eval(tree.body)
        if isinstance(result, float):
            result = round(result, 4)
        return f"{result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except Exception:
        return f"Error: Could not calculate '{expression}'"

def search_web(query: str):
    """
    Placeholder for web search tool.
    
    TODO: Implement using:
    - DuckDuckGo: from duckduckgo_search import DDGS
    - Wikipedia: requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}")
    - Serper API: https://serper.dev
    
    Args:
        query: Search query string
    
    Returns:
        Search results as string
    """
    return f"🔍 Web search for '{query}' - Implement this tool using DuckDuckGo or Wikipedia API!"

def text_summarizer(text: str, max_sentences: int = 3) -> str:
    """
    Summarizes long text.
    
    TODO: Implement using LLM or summarization library
    
    Args:
        text: Text to summarize
        max_sentences: Maximum sentences in summary
    
    Returns:
        Summary as string
    """
    # Placeholder - implement with LLM call
    return f"📝 Summary (placeholder): {text[:100]}..."

def translator(text: str, target_language: str = "hindi") -> str:
    """
    Translates text to target language.
    
    TODO: Implement using translation API or LLM
    
    Args:
        text: Text to translate
        target_language: Target language
    
    Returns:
        Translated text
    """
    return f"🌍 Translation to {target_language} (placeholder): {text}"

# Add more tools here!
# Example:
# def weather_checker(location: str) -> str:
#     """Check weather for a location"""
#     # Implement using OpenWeatherMap API
#     pass
