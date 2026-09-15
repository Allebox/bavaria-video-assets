import argparse, base64, json, os, pathlib, urllib.request
from PIL import Image, ImageOps

ap=argparse.ArgumentParser()
ap.add_argument("--asset-id",required=True); ap.add_argument("--category",required=True)
ap.add_argument("--prompt",required=True); ap.add_argument("--tags",default=""); ap.add_argument("--usage",default="video")
a=ap.parse_args()
allowed={"planning","clinical","human","aftercare","location","editorial","brand","comparison"}
if a.category not in allowed: raise SystemExit("invalid category")
if not __import__("re").match(r"^[a-z0-9][a-z0-9-]{2,79}$",a.asset_id): raise SystemExit("invalid asset id")
key=os.environ.get("OPENAI_API_KEY")
if not key: raise SystemExit("OPENAI_API_KEY is missing")
manifest=pathlib.Path("asset-manifest.json")
data=json.loads(manifest.read_text(encoding="utf-8"))
# Test/production guardrail: this worker generates exactly one image per invocation.
payload=json.dumps({"model":"gpt-image-1-mini","prompt":a.prompt,"size":"1536x1024","quality":"low","n":1}).encode()
req=urllib.request.Request("https://api.openai.com/v1/images/generations",data=payload,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
with urllib.request.urlopen(req,timeout=300) as r: result=json.load(r)
raw=base64.b64decode(result["data"][0]["b64_json"])
tmp=pathlib.Path("/tmp/generated.png"); tmp.write_bytes(raw)
dst=pathlib.Path(f"assets/approved/{a.category}/{a.asset_id}.webp"); dst.parent.mkdir(parents=True,exist_ok=True)
im=ImageOps.exif_transpose(Image.open(tmp)).convert("RGB"); im.save(dst,"WEBP",quality=88,method=6)
item={"id":a.asset_id,"category":a.category,"path":str(dst).replace("\\","/"),"tags":[x.strip() for x in a.tags.split(",") if x.strip()],"usage":a.usage,"status":"approved","source":"generated","model":"gpt-image-1-mini"}
assets=[x for x in data.get("assets",[]) if x.get("id")!=a.asset_id]; assets.append(item); assets.sort(key=lambda x:x["id"])
data["assets"]=assets; manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(dst)
