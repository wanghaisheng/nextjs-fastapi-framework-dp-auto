import secure
import uvicorn
from api.config import settings
from api.dependencies import validate_token
from fastapi import Depends, FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv
import os
from .cf_bypass import CloudflareBypass
import os

# load_dotenv()

app = FastAPI()

csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
referrer = secure.ReferrerPolicy().no_referrer()
cache_value = secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate()
x_frame_options = secure.XFrameOptions().deny()

secure_headers = secure.Secure(
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    cache=cache_value,
    xfo=x_frame_options,
)


@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response


origins = [
    "*",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://nextjs-fastapi-framework-dp-auto.vercel.app/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=86400,
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    message = str(exc.detail)

    return JSONResponse({"message": message}, status_code=exc.status_code)


@app.get("/api/messages/public")
def public():
    return {"text": "This is a public message."}


@app.get("/api/messages/protected", dependencies=[Depends(validate_token)])
def protected():
    return {"text": "This is a protected message."}


@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}


@app.get("/api/auth/me")
def auth_me():
    # print("><>>>>>>")
    # print(value)
    return None


# Your route now expects JSON body with 'keywords' field
@app.post("/api/ahref/kd/")
async def getAhrefKD(keyword: str = Body(...)):  # Use Body to get the
    if keyword:
        path = "/tmp/chromium"
        path = "/vercel/.cache/puppeteer/chrome/linux-123.0.6312.86"

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
        if "," in keyword:
            keywords = keyword.split(",")
        else:
            keywords = [keyword]
        datas = []
        if keyword in keywords:
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
            data = {"keyword": keyword, "kd": kd, "des": kds}
            datas.append(data)

            return data
    else:
        return []
