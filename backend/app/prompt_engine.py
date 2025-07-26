from llama_cpp import Llama
import os

# Get the absolute path to the model
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "models", "mistral-7b-instruct-v0.1.Q4_K_M.gguf")

# Load the model once when the file is imported
try:
    llm = Llama(
        model_path=model_path,
        n_ctx=2048,  # Context window
        n_threads=4,  # Number of threads
        verbose=False  # Reduce logging
    )
    print(f"Model loaded successfully from: {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    llm = None

def generate_questions(learner_profile: str, mentor_profile: str) -> str:
    if llm is None:
        return "Error: Model not loaded properly"
    
    # Truncate profiles if too long to fit in context
    max_profile_length = 800
    if len(learner_profile) > max_profile_length:
        learner_profile = learner_profile[:max_profile_length] + "..."
    if len(mentor_profile) > max_profile_length:
        mentor_profile = mentor_profile[:max_profile_length] + "..."
    
    prompt = f"""<s>[INST] You're helping a student prepare for a coffee chat with an industry professional.

Their LinkedIn profiles are below.

Learner Profile:
{learner_profile}

Mentor Profile:
{mentor_profile}

Based on this, suggest 3 thoughtful, specific questions the learner can ask during the chat.
Questions should reflect the mentor's experience and how it can help the learner.
Format as a numbered list. [/INST]"""

    try:
        response = llm(
            prompt, 
            max_tokens=300,
            temperature=0.7,
            top_p=0.9,
            stop=["</s>", "[INST]"]
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        return f"Error generating questions: {str(e)}"