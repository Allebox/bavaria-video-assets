import argparse, json, pathlib, shutil

ap=argparse.ArgumentParser()
ap.add_argument("--asset-id",required=True)
ap.add_argument("--output",default="selected-asset.webp")
a=ap.parse_args()

manifest=json.loads(pathlib.Path("asset-manifest.json").read_text(encoding="utf-8"))
matches=[x for x in manifest.get("assets",[]) if x.get("id")==a.asset_id]
if not matches:
    raise SystemExit(f"Asset not found in manifest: {a.asset_id}")
item=matches[0]
if item.get("status")!="approved":
    raise SystemExit(f"Asset is not approved: {a.asset_id} ({item.get('status')})")
src=pathlib.Path(item["path"])
if not src.is_file():
    raise SystemExit(f"Manifest path missing: {src}")
out=pathlib.Path(a.output)
out.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(src,out)
result={"id":item["id"],"category":item["category"],"source":str(src),"output":str(out),"usage":item.get("usage"),"tags":item.get("tags",[]),"status":"PASS"}
pathlib.Path("selected-asset.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,ensure_ascii=False))
