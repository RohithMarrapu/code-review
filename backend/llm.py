from transformers import pipeline


_reviewer = None


def get_reviewer():
    global _reviewer
    if _reviewer is None:
        # Using a lightweight instruction model suitable for CPU
        # You can swap to other seq2seq/causal models if desired
        _reviewer = pipeline(
            task="text2text-generation",
            model="google/flan-t5-base",
            framework="pt",
        )
    return _reviewer


SYSTEM_PROMPT = (
    "You are a senior software engineer performing a code review. "
    "Analyze the provided code for readability, modularity, maintainability, and potential bugs. "
    "Return a concise Markdown report using EXACTLY these sections and headings: \n"
    "### Overview\n"
    "### Strengths\n"
    "### Issues (with severity)\n"
    "### Actionable Suggestions\n"
    "List issues and suggestions as bullet points with short, actionable wording."
)


def build_prompt(filename: str, language: str | None, content: str) -> str:
    language_part = f"Language: {language}\n" if language else ""
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"File: {filename}\n"
        f"{language_part}"
        "Code:\n"
        f"{content}\n\n"
        "Review the code for readability, modularity, best practices, and potential bugs. "
        "Provide prioritized, actionable suggestions."
    )


def review_code(filename: str, language: str | None, content: str) -> str:
    prompt = build_prompt(filename, language, content)
    reviewer = get_reviewer()
    out = reviewer(prompt, max_new_tokens=512)
    text = out[0]["generated_text"] if isinstance(out, list) else str(out)
    text = text.strip()
    return _ensure_markdown_sections(text)


def _ensure_markdown_sections(text: str) -> str:
    """Ensure the report includes all required Markdown sections.

    If the model response is empty or missing sections, synthesize a minimal
    structured report and place the raw model output under Overview.
    """
    required = [
        "### Overview",
        "### Strengths",
        "### Issues (with severity)",
        "### Actionable Suggestions",
    ]

    if not text or all(h not in text for h in required):
        safe_overview = text or "Automated review generated."
        return (
            "### Overview\n"
            f"{safe_overview}\n\n"
            "### Strengths\n"
            "- Clear areas or patterns will be highlighted here.\n\n"
            "### Issues (with severity)\n"
            "- No specific issues extracted. Consider validating naming, error handling, and tests.\n\n"
            "### Actionable Suggestions\n"
            "- Add docstrings and comments where logic is non-obvious.\n"
            "- Split large functions into smaller, focused units.\n"
            "- Add tests for edge cases and error paths.\n"
        )

    # If some sections are present but not all, append the missing ones
    result = text
    for h in required:
        if h not in result:
            result += f"\n\n{h}\n- (No items)"
    return result


