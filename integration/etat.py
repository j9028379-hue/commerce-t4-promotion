"""Journal partagé T1 : publication CAS sur branche séparée, après contrôles et upload."""

import os, sys, base64, json, subprocess as sp
from pathlib import Path as P

branch = "state/commerce-autoplay"
endpoint = "repos/" + os.environ["GITHUB_REPOSITORY"] + "/contents/autoplay/etat.json"
gh = lambda *args: json.loads(sp.check_output(["gh", "api", *args]))
p = P("work/etat.json")
sig = P("work/etag")
if sys.argv[1] == "lire":
    r = gh(endpoint + "?ref=" + branch)
    p.write_bytes(base64.b64decode(r["content"]))
    sig.write_text(r["sha"])
else:
    new = P("work/suivant.json")
    old = json.loads(p.read_bytes())
    rows = json.loads(new.read_bytes())
    assert rows == old or (rows[:-1] == old and (not old or rows[-1][1] != old[-1][1]))
    r = gh(endpoint + "?ref=" + branch)
    assert (
        r["sha"] == sig.read_text()
    ), "Conflit : journal modifié, refuser la livraison"
    if rows != old:
        gh(
            "-X",
            "PUT",
            endpoint,
            "-f",
            "branch=" + branch,
            "-f",
            "sha=" + r["sha"],
            "-f",
            "message=Confirmer la livraison vérifiée " + os.environ["GITHUB_RUN_ID"],
            "-f",
            "content=" + base64.b64encode(new.read_bytes()).decode(),
        )
