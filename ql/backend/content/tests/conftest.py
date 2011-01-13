import pymongo
from quantumlounge.content.base import ContentManager
from quantumlounge.content.tweet import TweetManager, TweetType

def pytest_funcarg__cstore(request):
    """initialize a content store and return it"""
    db = pymongo.Connection().ql_test
    db.drop_collection("contents")
    return ContentManager(db, "contents")

def pytest_funcarg__db(request):
    db = pymongo.Connection().ql_test
    db.drop_collection("contents")
    return db

def pytest_funcarg__tweettype(request):
    db = request.getfuncargvalue("db")
    return TweetType(db,"content")

