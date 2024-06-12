from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.cf_bypass import CloudflareBypass
import os

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")


@app.get("/api/healthchecker")
def healthchecker():
    return {"status": "success", "message": "Integrate FastAPI Framework with Next.js"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: Union[str, None] = None
    completed: Union[bool, None] = None


class TodoItem(BaseModel):
    id: int
    title: str
    completed: bool


# Define the TodoItem model
class TodoItem(BaseModel):
    id: int
    title: str
    completed: bool


# In-memory storage for todo items
todos = []

# Route to create a new todo item


@app.post("/api/todos")
def create_todo_item(todo: TodoCreate):
    new_todo = TodoItem(id=len(todos) + 1, title=todo.title, completed=False)
    todos.append(new_todo)
    return new_todo


# Route to get all todo items


@app.get("/api/todos")
def get_all_todo_items():
    return todos


# Route to get a specific todo item by ID


@app.get("/api/todos/{todo_id}")
def get_todo_item(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return {"error": "Todo item not found"}


# Route to update a specific todo item by ID


@app.patch("/api/todos/{todo_id}")
def update_todo_item(todo_id: int, todo: TodoUpdate):
    for todo_item in todos:
        if todo_item.id == todo_id:
            todo_item.title = todo.title if todo.title is not None else todo_item.title
            todo_item.completed = (
                todo.completed if todo.completed is not None else todo_item.completed
            )
            return todo_item
    return {"error": "Todo item not found"}


# Route to delete a specific todo item by ID


@app.delete("/api/todos/{todo_id}")
def delete_todo_item(todo_id: int):
    for i, todo_item in enumerate(todos):
        if todo_item.id == todo_id:
            del todos[i]
            return {"message": "Todo item deleted"}
    return {"error": "Todo item not found"}


@app.get("/ahref/kd/{keyword}")
async def getAhrefKD(keyword: str):
    path = "/tmp/chromium"
    cloudflare_bypass = None
    # Try each path in sequence until a valid one is found

    # Check if the path exists
    if os.path.exists(path):
        print("tmp is found")
        # List all files and directories in the path
        files_and_dirs = os.listdir(path)

        # Filter out directories and only list files
        files = [f for f in files_and_dirs if os.path.isfile(os.path.join(path, f))]

        # Print all files
        for file in files:
            print(file)
        cloudflare_bypass = CloudflareBypass(browser_path=path)

    else:
        print("The path does not exist")
        cloudflare_bypass = CloudflareBypass(browser_path=None)

    # co = ChromiumOptions().set_browser_path(path).auto_port()
    # page1 = ChromiumPage(co)
    page1 = cloudflare_bypass.driver
    url = "https://ahrefs.com/keyword-difficulty/"

    page1.get(url)
    # keyword = "remini.ai"
    page1.ele("@placeholder=Enter keyword").input(keyword)

    # 点击登录按钮
    page1.ele("text=Check keyword").click()
    cookies = cloudflare_bypass.bypass(url)

    kd = page1.ele(".css-16bvajg-chartValue").text

    kds = page1.ele(".css-1wi5h2-row css-1crciv5 css-6rbp9c").text
    #     print(kd)
    #     print(kds)

    return {"keyword": keyword, "kd": kd, "des": kds}
