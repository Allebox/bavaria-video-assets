import argparse, json, pathlib, re

ap=argparse.ArgumentParser()
ap.add_argument("--script",required=True,help="Narration/script text")
ap.add_argument("--output",default="scene-plan.json")
a=ap.parse_args()

m=json.loads(pathlib.Path("asset-manifest.json").read_text(encoding="utf-8"))
approved=[x for x in m.get("assets",[]) if x.get("status")=="approved" and x.get("usage") in ("video","both")]
text=a.script.lower()

rules=[
 ("planning",["plan","planung","heil- und kostenplan","kostenplan","hkp","behandlung"]),
 ("aftercare",["nachsorge","kontrolle","follow-up","betreuung"]),
 ("human",["lächeln","smile","vertrauen","essen","lebensqualität","kontakt"]),
 ("clinical",["implantat","implant","klinik","zahn","behandlung"]),
 ("comparison",["vergleich","zirkon","metallkeramik"])
]
scored=[]
for x in approved:
    score=0
    hay=" ".join([x.get("id",""),x.get("category","")," ".join(x.get("tags",[]))]).lower()
    for cat,words in rules:
        if x.get("category")==cat:
            score+=sum(3 for w in words if w in text)
        score+=sum(1 for w in words if w in text and w in hay)
    scored.append((score,x))
scored.sort(key=lambda z:(-z[0],z[1]["id"]))
chosen=[]
for score,x in scored:
    if x["id"] not in [y["id"] for y in chosen]:
        chosen.append(x)
    if len(chosen)==2: break
if not chosen: raise SystemExit("No approved video assets available")

plan={
 "version":"1.0",
 "policy":{"selectionOrder":["css-ux","approved-library","new-generation"],"newGeneratedImages":0,"maxNewGeneratedImagesPerVideo":2},
 "visualSystem":{"background":["#F3F1EB","#F9F9F9"],"text":"#0D1117","gold":"#B6965E","darkGold":"#4E4028","h1h2":"Playfair Display","body":"Inter","radius":12},
 "scenes":[
   {"id":"scene-01","type":"css-ux+approved-asset","assetId":chosen[0]["id"],"assetPath":chosen[0]["path"],"motion":"slow-push","overlay":"minimal"},
   {"id":"scene-02","type":"css-ux+approved-asset","assetId":chosen[-1]["id"],"assetPath":chosen[-1]["path"],"motion":"slow-pan","overlay":"minimal"}
 ]
}
pathlib.Path(a.output).write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(plan,ensure_ascii=False))
