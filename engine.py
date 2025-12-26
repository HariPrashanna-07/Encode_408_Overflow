import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


def get_ai_reasoning(ingredients_text, health_goals):
    # Initialize the model correctly with a string name
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0.2  # Lower temperature is better for factual health analysis
    )

    # Create the prompt
    prompt = ChatPromptTemplate.from_template("""
    You are an AI health co-pilot.
    You think for the user so they don’t have to.

    Context:
    - User health goal: {goals}
    - Product ingredients (raw, messy, incomplete): {ingredients}

    Rules:
    - Do NOT list ingredients mechanically.
    - Do NOT use tables.
    - Do NOT sound like a report or nutrition textbook.
    - Assume the user is deciding whether to consume this RIGHT NOW.
    - **Smart Efficiency**: If you find a hard conflict (e.g., "Milk" in "Vegan"), STOP analyzing deeper. Mention this short-circuit.
    - **Anti-Repetition**: Never say the same reason twice. Group related issues.
    - **Zero Uncertainty**: If it's a hard conflict (e.g. allergen/dietary rule), Uncertainty is "None".

    Task:
    1. Infer what likely matters to the user.
    2. Give a nuanced verdict.
    3. **Analysis Note**: Mention if you stopped early (e.g., "Stopped analysis at 'Milk'").
    4. Explain WHY (max 3 short bullets). No repetition.
    5. Mention uncertainty (or "None" if hard conflict).
    6. **Assistive Nudge**: Suggest a helpful next step (e.g., "Want a vegan alternative?", "Check the sodium?").

    Tone:
    - Smart, efficient, helpful.

    Output format EXACTLY:

    Verdict: <Your nuanced verdict>

    Analysis Note:
    <One line explaining short-circuit or focus>

    Why it matters:
    - <reason>
    - <reason>

    Uncertainty:
    - <Specific condition OR "None - clear conflict">

    Nudge:
    <One helpful question or suggestion>
    """)


    # Create the chain
    chain = prompt | llm

    # Run the chain
    response = chain.invoke({
        "goals": health_goals,
        "ingredients": ingredients_text
    })

    content = response.content

    # Check if content is a list (structured output) and extract text
    if isinstance(content, list):
        # Join all 'text' fields from the list items
        full_text = []
        for item in content:
            if isinstance(item, dict) and 'text' in item:
                full_text.append(item['text'])
            elif isinstance(item, str):
                full_text.append(item)
        return "\n\n".join(full_text)
    
    return str(content)