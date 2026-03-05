import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from collections import Counter



print("Project Started...\n")
def extract_keywords(text):
    pass
def improvement_suggestion(text):
    pass

# Load data
data = pd.read_csv("feedback.csv")

# MAIN LOOP (add here)
for i, row in data.iterrows():
    text = row['feedback']
    keywords = extract_keywords(text)
    suggestion = improvement_suggestion(text)

    print("\nFeedback", i+1)
    print("Text:", text)
    print("Keywords:", keywords)
    print("Suggestion:", suggestion)

# Sentiment function
def get_sentiment(text):
    analysis = TextBlob(str(text))
    polarity = analysis.sentiment.polarity
    
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"
    
    # Complaint Category Detection
def detect_complaint_category(text):
    text = str(text).lower()
    
    # Delivery problems
    if "late" in text or "delay" in text or "delivery" in text:
        return "Delivery Issue"
    
    # Service problems
    elif "bad" in text or "worst" in text or "slow" in text or "rude" in text:
        return "Service Issue"
    
    # Product problems
    elif "quality" in text or "product" in text or "damaged" in text:
        return "Product Issue"
    
    # Price problems
    elif "price" in text or "cost" in text or "expensive" in text:
        return "Pricing Issue"
    
    else:
        return "General"
    
# Prepare stopwords
stop_words = set(stopwords.words('english'))

# Keyword extraction function
def extract_keywords(text):
    # Convert text to lowercase
    text = str(text).lower()
    
    # Break sentence into words
    words = word_tokenize(text)
    
    # Remove stopwords and special characters
    keywords = []
    for word in words:
        if word.isalnum() and word not in stop_words:
            keywords.append(word)
    
    # Return top 5 keywords
    return ", ".join(keywords[:5])

# Issue detection
def detect_issue(text):
    text = str(text).lower()
    
    if "late" in text or "delay" in text:
        return "Delivery Issue"
    elif "bad" in text or "worst" in text or "slow" in text:
        return "Service Issue"
    elif "quality" in text or "product" in text:
        return "Product Issue"
    else:
        return "General"

# Apply analysis
data["Sentiment"] = data["feedback"].apply(get_sentiment)
data["Complaint Category"] = data["feedback"].apply(detect_complaint_category)
data["Issue Category"] = data["feedback"].apply(detect_issue)
data["Keywords"] = data["feedback"].apply(extract_keywords)

print(data)

# Sentiment Dashboard
plt.figure(figsize=(6,4))
data["Sentiment"].value_counts().plot(kind="bar")
plt.title("Sentiment Analysis")
plt.xlabel("Sentiment")
plt.ylabel("Number of Feedbacks")
plt.show()
# Complaint Category Dashboard
plt.figure(figsize=(6,4))
data["Complaint Category"].value_counts().plot(kind="bar")
plt.title("Complaint Category Analysis")
plt.xlabel("Category")
plt.ylabel("Count")
plt.show()
# Combine all keywords
all_keywords = " ".join(data["Keywords"])
word_list = all_keywords.split(", ")

# Count frequency
keyword_counts = Counter(word_list)
top_keywords = keyword_counts.most_common(10)

# Convert to DataFrame
kw_df = pd.DataFrame(top_keywords, columns=["Keyword", "Count"])

# Plot
plt.figure(figsize=(6,4))
plt.bar(kw_df["Keyword"], kw_df["Count"])
plt.title("Top Keywords")
plt.xlabel("Keywords")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.show()

# Plot graph
data["Sentiment"].value_counts().plot(kind="bar")
plt.title("Customer Feedback Sentiment Analysis")
plt.show()

print("\nProject Completed!")
print("\nAnalysis Result:\n")
print(data)
print("\nAnalysis Result:\n")
print(data)
# ===== Summary Report Generation =====

report_file = open("report.txt", "w")

report_file.write("Customer Feedback Analysis Report\n")
report_file.write("---------------------------------\n\n")

# Total feedback
total_feedback = len(data)
report_file.write(f"Total Feedback: {total_feedback}\n\n")

# Sentiment Summary
report_file.write("Sentiment Summary:\n")
sentiment_counts = data["Sentiment"].value_counts()
for sentiment, count in sentiment_counts.items():
    report_file.write(f"{sentiment}: {count}\n")

report_file.write("\n")

# Complaint Category Summary
report_file.write("Complaint Category Summary:\n")
category_counts = data["Complaint Category"].value_counts()
for category, count in category_counts.items():
    report_file.write(f"{category}: {count}\n")

report_file.write("\n")

# Top Keywords
all_keywords = " ".join(data["Keywords"])
word_list = all_keywords.split(", ")
keyword_counts = Counter(word_list)
top_keywords = keyword_counts.most_common(5)

report_file.write("Top Keywords:\n")
for word, count in top_keywords:
    report_file.write(f"{word}: {count}\n")

report_file.close()

print("\nSummary report generated: report.txt")

# Combine all keywords
all_keywords = " ".join(data["Keywords"])
word_list = all_keywords.split(", ")

# Count frequency
common_words = Counter(word_list).most_common(10)

print("\nTop Keywords:")
for word, count in common_words:
    print(word, ":", count)

    print("\nComplaint Category Summary:")
print(data["Complaint Category"].value_counts())

data["Complaint Category"].value_counts().plot(kind="bar")
plt.title("Complaint Category Analysis")
plt.xlabel("Category")
plt.ylabel("Count")
plt.show()

# ===== Auto Suggestion for Improvement =====

print("\nImprovement Suggestions:")

category_counts = data["Complaint Category"].value_counts()

suggestions = []

for category, count in category_counts.items():
    if category == "Delivery Issue":
        suggestions.append(f"- Improve delivery process (Issues reported: {count})")
    
    elif category == "Service Issue":
        suggestions.append(f"- Provide customer service training (Issues reported: {count})")
    
    elif category == "Product Issue":
        suggestions.append(f"- Improve product quality control (Issues reported: {count})")
    
    elif category == "Pricing Issue":
        suggestions.append(f"- Review pricing strategy (Issues reported: {count})")

# Print suggestions
for s in suggestions:
    print(s)