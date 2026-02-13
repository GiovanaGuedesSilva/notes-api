import markdown


def render_markdown_to_html(content: str) -> str:
    return markdown.markdown(
        content,
        extensions=["fenced_code", "tables", "toc"]
    )
