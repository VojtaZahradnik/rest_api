from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Python exercise")

posts = {"title":["test1","test2"],"body" :["body1","body2"],"author" :["author1","author2"],"date":["date1","date2"]}

class Post(BaseModel):
    title: str
    body: str
    author: str
    date: str


@app.get("/")
async def root():
    return "Welcome"

# Editing blog post by title
@app.put("/update/{title}")
def update_post(title:str,post : Post):
    if (title in posts["title"]):
        index = getIndex("title", title)
        for key in posts:
            posts[key][index] = post.dict()[key]
        return {"message": "Update"}
    else:
        return {"message": "Not found"}

# Deleting blog post by title
@app.delete("/delete/{title}")
def delete_post(title:str):
    if (title in posts["title"]):
        index = getIndex("title",title)
        for key in posts.keys():
            del posts[key][index]
        return {"message": "Deleted"}
    else:
        return {"message": "Not found"}

# List blog post
@app.get("/list")
def list_all():
    return posts["title"]

# View blog post detail
@app.get("/list/{title}")
def list_post(title:str):
    if(title in posts["title"]):
        result = [x[getIndex("title",title)] for x in [*posts.values()]]
    else:
        result = {"message": "Not found"}
    return result

# Creating a new blog post
@app.post("/create")
def create_post(post : Post):
    if(post.title not in posts["title"]):
        for key in posts:
            posts[key].append(post.dict()[key])
        return {"message": "Post created"}
    else:
        return {"message": "Name of the post already exists"}

def getIndex(key,title):
    return posts[key].index(title)
