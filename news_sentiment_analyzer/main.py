from newsapi import NewsApiClient
from textblob import TextBlob

def main():
    print("[ News Sentiment Analyzer ]\n")

    #1 Input API_KEY
    API_KEY = input("Input Your NewsAPI Key: ").strip()
    if not API_KEY:
        print("Invalid API_KEY input...")
        return

    #2 NewsAPI
    newsapi = NewsApiClient(api_key=API_KEY)

    #3 Category
    print("Enter the categories you want to search for, such as corporations, themes, etc.. \n")
    
    #3.1 Keywords
    keyword = input("Input Keyword: ").strip()
    if not keyword:
        print("Invalid Keyword input...")
        return
    
    #3.2 Date Range(Optional)
    from_date = input("start date(YYYY-MM-DD, Omitted when you input Enter): ").strip()
    to_date = input("end date(YYYY-MM-DD, Omitted when you input Enter): ").strip()

    #3.3 sort
    print("\nSelect the sort method:")
    print("1. publishedAt(최신순)")
    print("2. relevancy(관련도순)")
    print("3. popularity(인기순)")

    sort_choice = input("input number(no input=default=1): ").strip()

    sort_map = {
        "1": "publishedAt",
        "2": "relevancy",
        "3": "popularity"
    }

    sort_by = sort_map.get(sort_choice, "publishedAt")

    print(f"\n Search results for news related to '{keyword}'\n")

    try:
        #4. parameter
        params = {
            "q": keyword,
            "language": "en",
            "sort_by": sort_by,
            "page_size": 5
        }

        if from_date:
            params["from_param"] = from_date
        if to_date:
            params["to"] = to_date
    
        #5. Request News
        result = newsapi.get_everything(**params)

        articles = result.get("articles", [])

        if not articles:
            print("No Result...")
            return
    
        positive_count = 0  #긍정
        neutral_count = 0   #중립
        negative_count = 0  #부정
        polarity_sum = 0    #평균(시장 분위기 파악 목적)

        for i, article in enumerate(articles, start=1):
            title = article.get("title", "제목 없음")
            source = article.get("source", {}).get("name", "출처 없음")
            published = article.get("publishedAt", "")[:10]

            # Sentiment Analize
            blob = TextBlob(title)
            polarity = blob.sentiment.polarity

            if polarity > 0:
                sentiment = "positive"
                positive_count += 1
            elif polarity < 0:
                sentiment = "negative"
                negative_count += 1
            else:
                sentiment = "neutral"
                neutral_count += 1

            polarity_sum += polarity

            print(f"{i}. {title}")
            print(f"    - 출처: {source}")
            print(f"    - 날짜: {published}")
            print(f"    - 감정 분석 결과: {sentiment} (점수: {polarity:.2f})\n")

        total_articles = positive_count + neutral_count + negative_count

        if total_articles > 0:
            avg_polarity = polarity_sum / total_articles
        else:
            avg_polarity = 0

        print("=" * 40)
        print("[ Sentiment Summary ]")
        print(f"Positive : {positive_count}")
        print(f"Neutral : {neutral_count}")
        print(f"Negative : {negative_count}")
        print(f"Average Polarity : {avg_polarity:.2f}")
        print("=" * 40)

    except Exception as e:
        print("뉴스를 불러오는 중 오류가 발생했습니다.")
        print("오류 내용:", e)
    
if __name__ == "__main__":
    main()