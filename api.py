import requests
from config import LEETCODE_API_URL


def get_daily_challenge():
    query = """
    query questionOfToday {
      activeDailyCodingChallengeQuestion {
        date
        userStatus
        link
        question {
          acRate
          difficulty
          freqBar
          frontendQuestionId: questionFrontendId
          isFavor
          paidOnly: isPaidOnly
          status
          title
          titleSlug
          hasVideoSolution
          hasSolution
          topicTags {
            name
            id
            slug
          }
        }
      }
    }
    """
    response = requests.post(LEETCODE_API_URL, json={"query": query})
    data = response.json()
    daily_challenge = data["data"]["activeDailyCodingChallengeQuestion"]
    return daily_challenge


def get_upcoming_contests():
    query = """
    query upcomingContests {
      upcomingContests {
        title
        titleSlug
        startTime
        duration
        __typename
      }
    }
    """
    response = requests.post(LEETCODE_API_URL, json={"query": query})
    data = response.json()
    upcoming_contests = data["data"]["upcomingContests"]
    return upcoming_contests
