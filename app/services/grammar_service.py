import requests

LANGUAGETOOL_API_URL = "https://api.languagetool.org/v2/check"


def check_grammar(text: str, language: str = "en-US") -> dict:
    try:
        response = requests.post(
            LANGUAGETOOL_API_URL,
            data={
                "text": text,
                "language": language
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        errors = [
            {
                "message": match["message"],
                "offset": match["offset"],
                "length": match["length"],
                "replacements": [r["value"] for r in match.get("replacements", [])[:5]]
            }
            for match in data.get("matches", [])
        ]

        return {
            "text": text,
            "errors": errors,
            "error_count": len(errors)
        }
    except Exception as e:
        return {
            "text": text,
            "errors": [],
            "error_count": 0,
            "warning": f"Grammar check failed: {str(e)}"
        }
