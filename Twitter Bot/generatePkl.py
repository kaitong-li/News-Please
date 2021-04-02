import joblib

wordsTB = ["'s", ',', 'keywords', 'Twitter', 'account', 'a', 'all', 'anyone', 'are', 'awesome', 'be', 'behavior', 'by', 'bye', 'can', 'chatting', 'check', 'could', 'data', 'day', 'detail', 'do', 'dont', 'find', 'for', 'give', 'good', 'goodbye', 'have', 'hello', 'help', 'helpful', 'helping', 'hey', 'hi', 'history', 'how', 'i', 'id', 'is', 'later', 'list', 'load', 'locate', 'log', 'looking', 'lookup', 'management', 'me', 'module', 'next', 'nice', 'of', 'offered', 'open', 'provide', 'reaction', 'related', 'result', 'search', 'searching', 'see', 'show', 'support', 'task', 'thank', 'thanks', 'that', 'there', 'till', 'time', 'to', 'transfer', 'up', 'want', 'what', 'which', 'with', 'you']
classesTB = ['goodbye', 'greeting', 'options', 'thanks', 'no_response']
joblib.dump(wordsTB, 'wordsTB.pkl')
joblib.dump(classesTB, 'classesTB.pkl')

'''
x = joblib.load('x.pkl')
print(x)
'''