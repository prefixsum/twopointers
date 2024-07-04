import datetime

# LeetCode API endpoint
LEETCODE_API_URL = "https://leetcode.com/graphql"

# Discord channel ID where you want to post the challenge
CHANNEL_IDS = {
    "DAILY_CHALLENGE": 1258047274035183666,
    "WEEKLY_CONTEST": 1220304410698317855,
    "BIWEEKLY_CONTEST": 1220304410698317855,
}

# Local timezone object
LOCAL_TZ = datetime.datetime.now().astimezone().tzinfo
