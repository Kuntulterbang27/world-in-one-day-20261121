"""Final copy desk: preserve facts while fitting one readable context line."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTEXT = {
"asia-01": "Leh and Kargil hold first local polls since UT status.",
"asia-02": "India's PM urges nation-building at IIT Kharagpur.",
"asia-03": "Delhi counsel dispute claims about earlier bail notice.",
"asia-04": "British rider claims fifth Macau motorcycle GP win.",
"asia-05": "Anutin outlines farm quotas for proposed US trade deal.",
"asia-06": "PM seeks China-Myanmar help for northern Thai rivers.",
"asia-07": "Hanoi approves priority-project law for July 2027.",
"asia-08": "Officials raid Planet BKK pub in Chom Thong.",
"asia-09": "Coalition says three Houthi missiles aimed at Riyadh.",
"asia-11": "Gaza City: hospital says 3 dead; Israel cites militants.",
"asia-12": "State TV shows Guard device at undisclosed Iran site.",
"asia-13": "Tehran's deputy FM says Qatar mediation continues.",
"SUP02": "Antalya talks run into Saturday; no final deal reported.",
"EA01": "Russian ship near Gogland drifts into Finnish waters.",
"EA02": "Paris: Yellow Vests and students protest costs, policing.",
"EA03": "Von der Leyen backs Denmark after Friday's disclosure.",
"EA04": "Sanchez proposes 2027 housing levy; approval still due.",
"EA05": "Ex-police chief faced Mafia inquiry; denied wrongdoing.",
"EA06": "Ukraine's leader voices doubts at Saturday Kyiv talks.",
"EA11": "LA-Long Beach security union deal awaits ratification.",
"EA12": "McGuinty says forces still work closely, in Halifax.",
"EA13": "Saturday pledge follows cartel boss's Friday arrest.",
"SUP03": "Saturday Junin report follows Friday quake; new tremors.",
"who-polio": "Arba Minch launch targets 11.3 million children.",
"kenya-ruto": "Kenya's president rejects IEBC criticism in Sirisia.",
"nigeria-police": "Akume delivers president's warning to Wudil cadets.",
"chad-dengue": "PM starts sanitation drive at N'Djamena market.",
"aswan-aa": "Ministers discuss African security and recovery.",
"cummins": "Saturday board statement backs captain in Sydney.",
"victoria-school": "Labor's $15m Melbourne pledge depends on election win.",
"nz-cricket": "Rahul hits 136; India 488/4 at Saturday stumps in NZ.",
"sydney-charges": "Saturday charges follow Friday's Castle Hill stabbing.",
"EA07": "Brussels: Costa proposes 3% levy; no deal adopted.",
"EA08": "Brussels signing after ten years; approvals still needed.",
"EA09": "Russia: Kulikov named; Kim keeps strategic role.",
"EA10": "Geneva agrees early Saturday to two more years of talks.",
"SUP01": "Reuters reveals red-chip curbs; Beijing has not replied.",
}


def main():
    path = ROOT / "stories.json"
    stories = json.loads(path.read_text(encoding="utf-8"))
    for story in stories:
        if story["id"] in CONTEXT:
            story["image_context"] = CONTEXT[story["id"]]
    # Renderer data deliberately excludes verbose provenance. SOURCES retains it.
    fields = ("id", "number", "section", "image_headline", "image_context", "hero", "lon", "lat")
    slim = [{key: story[key] for key in fields} for story in stories]
    path.write_text("[\n" + ",\n".join(json.dumps(story, ensure_ascii=False) for story in slim) + "\n]\n", encoding="utf-8")
    print("Copy-edited", len(CONTEXT), "briefs; hero preserved")


if __name__ == "__main__":
    main()
