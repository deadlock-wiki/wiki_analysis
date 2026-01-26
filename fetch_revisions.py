def fetch_recent_revisions(days=30, limit=500):
    since = (datetime.now(UTC) - timedelta(days=days)).isoformat()
    all_records = []
    rccontinue = None

    while True:
        params = {
            "action": "query",
            "format": "json",
            "list": "recentchanges",
            "rcprop": "title|timestamp|user|type",
            "rclimit": limit,
            "rcstart": since,
            "rcdir": "newer",
        }

        if rccontinue:
            params["rccontinue"] = rccontinue

        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        for rc in data["query"]["recentchanges"]:
            all_records.append({
                "page": rc["title"],
                "timestamp": rc["timestamp"],
                "user": rc.get("user"),
                "type": rc.get("type"),
            })

        if "continue" not in data:
            break

        rccontinue = data["continue"]["rccontinue"]

    return pd.DataFrame(all_records)
