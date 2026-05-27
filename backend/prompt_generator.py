def generate_safe_query(sanitized_text: str, user_goal: str = "") -> str:
    goal = user_goal.strip() or "Help me understand and fix this issue."

    return f"""I need help with the following technical issue.

Goal:
{goal}

Sanitized context:
{sanitized_text}

Please analyze the issue and provide:
1. Likely root cause
2. Step-by-step troubleshooting
3. Commands I can safely run locally
4. What information is still missing, without asking for real secrets
5. How to prevent this issue in future

Important:
- Sensitive values have been replaced with placeholders like <TOKEN>, <EMAIL>, <PRIVATE_IP>, <LOCAL_PATH>, <DATABASE_URL>, or <SECRET_ASSIGNMENT>.
- Do not ask me to share real secrets, tokens, passwords, private keys, cookies, internal hostnames, or production details.
- If more information is needed, ask only for sanitized logs or masked configuration.
"""