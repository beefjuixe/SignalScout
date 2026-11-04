from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI(title="Fabrikam SignalScout")
templates = Jinja2Templates(directory="templates")


def _trace(ts: str, step: str, tool: str, params: dict, result: str) -> dict:
    return {
        "timestamp": ts,
        "step": step,
        "tool": tool,
        "params": params,
        "result": result,
    }


ACCOUNTS = {
    "rayquaza_cloud": {
        "id": "rayquaza_cloud",
        "name": "Rayquaza Cloud",
        "industry": "Cloud Infrastructure",
        "size": "2,400 employees · Series D",
        "badges": ["🔥 CISO Transition", "+24% SecOps Growth"],
        "target_lead": {
            "name": "Scarlett Johansson",
            "title": "CISO",
            "tenure": "87 days in seat",
            "previous_role": "VP, Security Architecture at Arceus Data",
            "focus_areas": ["Zero Trust", "Cloud SIEM consolidation", "Vendor rationalization"],
        },
        "warm_path": {
            "internal_contact": "Alex Rivera",
            "internal_title": "VP of Eng",
            "relationship_overlap": "Alex and Scarlett co-authored the 2023 Cloud Trust Alliance playbook and overlapped 18 months at Arceus Data. Alex can forward a technical intro without a cold AE motion.",
            "score_label": "VERY HIGH",
            "score": 0.95,
        },
        "outreach": {
            "intro_request": """Alex — quick ask.

Scarlett Johansson just landed as CISO at Rayquaza Cloud (87 days in seat). Their SecOps spend is up 24% QoQ and they're consolidating cloud SIEM.

You two overlapped at Arceus and co-authored the Cloud Trust Alliance playbook — relationship score is 0.95.

Would you be open to forwarding a short intro? Draft below you can send as-is:

---
Scarlett — congrats on the CISO seat. Given you're compressing the SIEM stack, I wanted to connect you with our AE who covers the Fabrikam Sentinel + Defender overlay we used at Arceus. No pitch, just a 20-min architecture compare if useful.

Alex Rivera
VP of Engineering, Fabrikam
---""",
            "direct_technical": """Scarlett — congratulations on the CISO role at Rayquaza.

Signal we're seeing: SecOps headcount + tooling up 24% while three overlapping SIEM contracts come up in Q1. Fabrikam's Sentinel workspace + Defender XDR overlay is the pattern we ran at Arceus when you were collapsing similar sprawl.

If useful, I can send a 2-page architecture delta (ingest cost, SOAR playbooks, identity signal join) before any commercial conversation.

Happy to keep this purely technical.
— Fabrikam Commercial AE, West""",
        },
        "mcp_trace": [
            _trace("14:02:11.203", "territory_scan", "crm.list_accounts", {"segment": "commercial_ae", "limit": 150}, "OK — 150 monitored accounts ranked"),
            _trace("14:02:11.418", "priority_filter", "signals.rank_week", {"week": "2026-W45", "top_n": 5}, "OK — Rayquaza Cloud #1 (CISO transition + spend spike)"),
            _trace("14:02:11.640", "lead_enrichment", "graph.get_executive", {"account_id": "rayquaza_cloud", "role": "CISO"}, "OK — Scarlett Johansson · 87d tenure"),
            _trace("14:02:11.891", "warm_path_bridge", "graph.internal_overlap", {"lead": "scarlett_johansson", "org": "fabrikam"}, "OK — Alex Rivera VP Eng · score 0.95"),
            _trace("14:02:12.104", "draft_generation", "llm.compose_outreach", {"voice": "ae_forwardable", "variants": 2}, "OK — intro_request + direct_technical"),
            _trace("14:02:12.331", "slack_ready", "webhook.preview", {"channel": "#ae-west-signals"}, "READY — briefing payload staged"),
        ],
    },
    "lucario_systems": {
        "id": "lucario_systems",
        "name": "Lucario Systems",
        "industry": "Identity & Access",
        "size": "1,150 employees · Series C",
        "badges": ["⚡ Board Pressure", "IAM RFP Open"],
        "target_lead": {
            "name": "Keanu Reeves",
            "title": "VP of Security",
            "tenure": "14 months in seat",
            "previous_role": "Director, Identity Platform at Neonetix",
            "focus_areas": ["Workforce IAM", "Privileged access", "Passwordless rollout"],
        },
        "warm_path": {
            "internal_contact": "Priya Shah",
            "internal_title": "Principal PM, Entra",
            "relationship_overlap": "Priya sat on the same Cloud Identity SIG as Keanu for two years and reviewed Lucario's passwordless whitepaper. She can validate Fabrikam Entra as a peer, not a vendor.",
            "score_label": "HIGH",
            "score": 0.82,
        },
        "outreach": {
            "intro_request": """Priya — Lucario just opened an IAM RFP (board-driven). Keanu Reeves is VP Security.

You two shared the Cloud Identity SIG and you reviewed their passwordless paper. Relationship score 0.82.

Could you ping Keanu with a peer note on Entra Conditional Access + PIM vs. their current stack? Draft:

---
Keanu — saw the IAM RFP land. If you're comparing privileged access models, happy to walk through how we bound Entra PIM to production break-glass at similar scale. No AE on the first call if you prefer.

Priya Shah
Principal PM, Entra · Fabrikam
---""",
            "direct_technical": """Keanu — noting Lucario's IAM RFP and the board's 90-day identity risk ask.

Fabrikam Entra + PIM can map to the three controls in your RFP appendix (just-in-time admin, workload identities, passwordless). I can send a control-by-control matrix against your current IdP without a sales deck.

If a 25-min architecture working session is useful, I'll keep it engineer-only.
— Fabrikam Commercial AE""",
        },
        "mcp_trace": [
            _trace("14:05:03.011", "rfp_watch", "signals.procurement", {"account_id": "lucario_systems"}, "OK — IAM RFP detected (board packet)"),
            _trace("14:05:03.220", "exec_resolve", "graph.get_executive", {"role": "VP Security"}, "OK — Keanu Reeves · 14mo tenure"),
            _trace("14:05:03.441", "warm_path_bridge", "graph.internal_overlap", {"lead": "keanu_reeves"}, "OK — Priya Shah Principal PM · score 0.82"),
            _trace("14:05:03.702", "control_map", "product.map_rfp", {"sku": "entra_pim"}, "OK — 11/14 controls covered"),
            _trace("14:05:03.918", "draft_generation", "llm.compose_outreach", {"voice": "peer_pm"}, "OK — intro + technical variants"),
        ],
    },
    "garchomp_defense": {
        "id": "garchomp_defense",
        "name": "Garchomp Defense",
        "industry": "Aerospace & Defense",
        "size": "8,600 employees · Public",
        "badges": ["🛡️ CMMC Deadline", "OT/IT Convergence"],
        "target_lead": {
            "name": "Cillian Murphy",
            "title": "CISO",
            "tenure": "2.4 years in seat",
            "previous_role": "Head of Cyber, North Atlantic Systems",
            "focus_areas": ["CMMC L2 evidence", "OT segmentation", "National-cloud landing zone"],
        },
        "warm_path": {
            "internal_contact": "Marcus Cole",
            "internal_title": "Director, Public Sector Engineering",
            "relationship_overlap": "Marcus and Cillian served on the same CMMC working group. Marcus can speak evidence packages, not product slogans.",
            "score_label": "HIGH",
            "score": 0.78,
        },
        "outreach": {
            "intro_request": """Marcus — Garchomp's CMMC L2 date moved up a quarter. Cillian Murphy is still CISO.

You two sat on the CMMC WG together (score 0.78). Could you offer a 30-min evidence-mapping session?

---
Cillian — heard the L2 date compressed. We just closed a similar OT/IT evidence pack for a peer prime. Happy to share the control-to-artifact map if it saves your team a cycle.

Marcus Cole
Director, Public Sector Engineering · Fabrikam
---""",
            "direct_technical": """Cillian — flagging the pulled-forward CMMC L2 milestone against Garchomp's OT/IT program.

Fabrikam national-cloud landing zone + Defender for IoT can produce the evidence artifacts your assessor listed (network diagrams, privileged session logs, SBOM attestation). I can send a redacted sample pack from a peer prime.

Technical review only — no commercial motion until you want it.
— Fabrikam Commercial AE, Public Sector""",
        },
        "mcp_trace": [
            _trace("14:08:44.100", "compliance_watch", "signals.regulatory", {"framework": "CMMC_L2"}, "OK — deadline pulled forward 1Q"),
            _trace("14:08:44.322", "lead_enrichment", "graph.get_executive", {"account_id": "garchomp_defense"}, "OK — Cillian Murphy CISO"),
            _trace("14:08:44.551", "warm_path_bridge", "graph.internal_overlap", {"lead": "cillian_murphy"}, "OK — Marcus Cole · score 0.78"),
            _trace("14:08:44.803", "evidence_map", "compliance.control_pack", {"level": 2}, "OK — 17 artifacts mapped"),
            _trace("14:08:45.044", "draft_generation", "llm.compose_outreach", {"voice": "public_sector"}, "OK — drafts staged"),
        ],
    },
    "umbreon_finance": {
        "id": "umbreon_finance",
        "name": "Umbreon Finance",
        "industry": "Capital Markets",
        "size": "3,200 employees · Public",
        "badges": ["📈 SOC2 Bridge", "Insider Threat Spike"],
        "target_lead": {
            "name": "Zendaya Coleman",
            "title": "Head of Cyber Risk",
            "tenure": "11 months in seat",
            "previous_role": "VP, Operational Risk at Nightshade Capital",
            "focus_areas": ["Insider risk", "Data loss prevention", "Trading-floor segmentation"],
        },
        "warm_path": {
            "internal_contact": "Jordan Hale",
            "internal_title": "CISO Advisory, FSI",
            "relationship_overlap": "Jordan advised Zendaya's prior firm through a SOC2 bridge audit. Trust is already established on evidence quality.",
            "score_label": "MEDIUM-HIGH",
            "score": 0.71,
        },
        "outreach": {
            "intro_request": """Jordan — Umbreon showed an insider-threat alert volume spike (+41% MoM). Zendaya Coleman owns cyber risk.

You ran her prior SOC2 bridge. Score 0.71. Open to a quiet intro on Purview + insider risk?

---
Zendaya — saw the alert volume move. If you want a second set of eyes on how we bound Purview DLP to trading-floor identities without killing desk latency, I can connect you.

Jordan Hale
CISO Advisory, FSI · Fabrikam
---""",
            "direct_technical": """Zendaya — Umbreon's insider-risk telemetry jumped 41% MoM while the SOC2 bridge is still open.

Fabrikam Purview insider risk + DLP can tag privileged research data against trader identities with sub-10ms policy evaluation. I can share a latency bench from a peer desk.

Keeping this technical unless you want coverage pulled in.
— Fabrikam Commercial AE, FSI""",
        },
        "mcp_trace": [
            _trace("14:11:19.500", "telemetry_spike", "signals.security_ops", {"kpi": "insider_alerts"}, "OK — +41% MoM at Umbreon Finance"),
            _trace("14:11:19.714", "lead_enrichment", "graph.get_executive", {"role": "Head of Cyber Risk"}, "OK — Zendaya Coleman"),
            _trace("14:11:19.966", "warm_path_bridge", "graph.internal_overlap", {"lead": "zendaya_coleman"}, "OK — Jordan Hale · score 0.71"),
            _trace("14:11:20.188", "draft_generation", "llm.compose_outreach", {"voice": "fsi_quiet"}, "OK — drafts staged"),
        ],
    },
    "sylveon_health": {
        "id": "sylveon_health",
        "name": "Sylveon Health",
        "industry": "Health Tech",
        "size": "890 employees · Series B",
        "badges": ["🏥 HIPAA Expansion", "New CTO Hire"],
        "target_lead": {
            "name": "Oscar Isaac",
            "title": "CTO",
            "tenure": "41 days in seat",
            "previous_role": "SVP Engineering, ClinicMesh",
            "focus_areas": ["PHI data plane", "Zero-trust clinical apps", "Multi-cloud EHR connectors"],
        },
        "warm_path": {
            "internal_contact": "Nina Park",
            "internal_title": "Partner Engineering, Healthcare",
            "relationship_overlap": "Nina and Oscar shipped ClinicMesh's FHIR gateway together. She can reopen that engineering thread in one message.",
            "score_label": "VERY HIGH",
            "score": 0.91,
        },
        "outreach": {
            "intro_request": """Nina — Oscar Isaac is 41 days into the CTO seat at Sylveon. They're expanding HIPAA scope to a new PHI data plane.

You two shipped ClinicMesh's FHIR gateway (score 0.91). Perfect warm path.

---
Oscar — congrats on Sylveon. If the PHI data plane is still greenfield, the pattern we used on ClinicMesh (confidential compute + Purview labels) might save you a design cycle. Happy to reconnect.

Nina Park
Partner Engineering, Healthcare · Fabrikam
---""",
            "direct_technical": """Oscar — congratulations on the CTO role.

Sylveon's HIPAA expansion implies a new PHI data plane across two clouds. Fabrikam confidential compute + Purview sensitivity labels is the same skeleton we used on ClinicMesh's FHIR gateway.

I can send a 1-pager on tenant isolation and break-glass for clinical apps — engineer to engineer.
— Fabrikam Commercial AE, Healthcare""",
        },
        "mcp_trace": [
            _trace("14:14:02.010", "hire_watch", "signals.org_change", {"role": "CTO"}, "OK — Oscar Isaac · 41d tenure"),
            _trace("14:14:02.240", "scope_change", "signals.compliance", {"framework": "HIPAA"}, "OK — PHI data plane expansion"),
            _trace("14:14:02.481", "warm_path_bridge", "graph.internal_overlap", {"lead": "oscar_isaac"}, "OK — Nina Park · score 0.91"),
            _trace("14:14:02.703", "draft_generation", "llm.compose_outreach", {"voice": "partner_eng"}, "OK — drafts staged"),
        ],
    },
}


def account_summary(account: dict) -> dict:
    lead = account["target_lead"]
    return {
        "id": account["id"],
        "name": account["name"],
        "industry": account["industry"],
        "size": account["size"],
        "badges": account["badges"],
        "target_lead": {"name": lead["name"], "title": lead["title"]},
    }


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/accounts")
async def list_accounts():
    return [account_summary(account) for account in ACCOUNTS.values()]


@app.get("/api/accounts/{account_id}")
async def get_account(account_id: str):
    account = ACCOUNTS.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.post("/api/slack/push/{account_id}")
async def push_slack(account_id: str):
    account = ACCOUNTS.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {
        "ok": True,
        "channel": "#ae-west-signals",
        "pushed_at": datetime.now(timezone.utc).isoformat(),
        "message": f"Pushed {account['name']} signal briefing to Slack!",
    }
