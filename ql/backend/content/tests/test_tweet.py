import datetime

def test_basics(tweettype):
    tweet = tweettype.cls(content="Super duper cooper")
    i = tweettype.mgr.put(tweet)

    t = tweettype.mgr[i]

    assert t.content == "Super duper cooper"
    assert t.date < datetime.datetime.now()


