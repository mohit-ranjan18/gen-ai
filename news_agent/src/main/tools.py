#https://news-hub-be-dev.up.railway.app/v1/preference
import requests


def fetch_preferences() -> dict:
    """
    Fetch user preferences from the news hub API.

    This method does not take any input.

    Returns:
        dict: Contains:
            - 'status': str
            - 'preferences': List[dict] with keys: 'name', 'description', 'datetime', 'status'

    Raises:
        requests.exceptions.RequestException: For network-related errors.
        ValueError: If the response status is not 'success' or JSON can't be parsed.
    """
    url = "https://news-hub-be-dev.up.railway.app/v1/preference"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        status = data.get("status", "unknown")
        if status != "success":
            error_msg = data.get("message", "Unknown error from API")
            raise ValueError(f"API Error: {error_msg}")

        preferences_data = data.get("data", {}).get("preferences", [])

        preferences = [
            {
                "name": pref.get("name"),
                "description": pref.get("description"),
                "datetime": pref.get("datetime"),
                "status": pref.get("status")
            }
            for pref in preferences_data[:3]
        ]

        return {
            "status": status,
            "preferences": preferences
        }

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise
    except (ValueError, KeyError, TypeError) as e:
        print(f"Error parsing response: {e}")
        raise

# Example usage
# if __name__ == "__main__":
#     try:
#         result = fetch_preferences()
#         print(result)
#         print("Status:", result["status"])
#         print("Preferences:")
#         # for p in result["preferences"]:
#         #     print(p)
#     except Exception as e:
#         print("Error:", e)
