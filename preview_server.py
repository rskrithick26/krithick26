import http.server
import socketserver
import os
import json
import urllib.parse
import urllib.request
import mimetypes

PORT = 8080
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "artifacts", "drugscope", "dist", "public"))

class SPAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Handle API routes
        if path == "/api/healthz":
            self.send_json({"status": "ok"})
            return

        if path == "/api/dashboard/summary":
            self.send_json({
                "totalCompounds": 14,
                "totalAnalyses": 9,
                "savedCount": 2,
                "recentAnalyses": [
                    {
                        "id": 1,
                        "cid": 2519,
                        "compoundName": "Caffeine",
                        "status": "nominal",
                        "analyzedAt": "2026-09-17T12:00:00.000Z"
                    },
                    {
                        "id": 2,
                        "cid": 2244,
                        "compoundName": "Aspirin",
                        "status": "nominal",
                        "analyzedAt": "2026-09-17T11:30:00.000Z"
                    }
                ],
                "admetOverview": [
                    {"label": "Low risk", "count": 12, "tone": "accent"},
                    {"label": "Moderate", "count": 4, "tone": "accent"}
                ],
                "toxicityOverview": [
                    {"label": "Low risk", "count": 15, "tone": "accent"},
                    {"label": "Moderate", "count": 2, "tone": "accent"}
                ]
            })
            return

        if path == "/api/saved-compounds":
            self.send_json([
                {
                    "cid": 2519,
                    "name": "Caffeine",
                    "formula": "C8H10N4O2",
                    "savedAt": "2026-09-17T10:00:00.000Z"
                },
                {
                    "cid": 2244,
                    "name": "Aspirin",
                    "formula": "C9H8O4",
                    "savedAt": "2026-09-17T10:15:00.000Z"
                }
            ])
            return

        if path == "/api/analyses":
            self.send_json([
                {
                    "id": 1,
                    "cid": 2519,
                    "compoundName": "Caffeine",
                    "status": "nominal",
                    "analyzedAt": "2026-09-17T12:00:00.000Z"
                }
            ])
            return

        if path.startswith("/api/compounds/lookup"):
            query_params = urllib.parse.parse_qs(parsed.query)
            q = query_params.get("query", ["caffeine"])[0].lower()
            if "aspirin" in q or q == "2244":
                self.send_json(self.get_aspirin())
            else:
                self.send_json(self.get_caffeine())
            return

        if path.startswith("/api/compounds/search"):
            query_params = urllib.parse.parse_qs(parsed.query)
            q = query_params.get("query", [""])[0]
            self.send_json({
                "results": [
                    {
                        "cid": 2519,
                        "name": "Caffeine",
                        "formula": "C8H10N4O2",
                        "molecularWeight": 194.19
                    },
                    {
                        "cid": 2244,
                        "name": "Aspirin",
                        "formula": "C9H8O4",
                        "molecularWeight": 180.16
                    }
                ],
                "total": 2,
                "page": 1,
                "pageSize": 20
            })
            return

        if path.startswith("/api/compounds/"):
            cid_str = path.split("/")[-1]
            if cid_str == "2244":
                self.send_json(self.get_aspirin())
            else:
                self.send_json(self.get_caffeine())
            return

        # Check if requested static file exists
        req_file = os.path.normpath(os.path.join(BASE_DIR, path.lstrip("/")))
        if os.path.isfile(req_file):
            return super().do_GET()

        # SPA fallback to index.html
        index_path = os.path.join(BASE_DIR, "index.html")
        if os.path.isfile(index_path):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            with open(index_path, "rb") as f:
                content = f.read()
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        self.send_error(404, "File not found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path == "/api/saved-compounds":
            self.send_json({"success": True})
            return
        if path == "/api/analyses":
            self.send_json({"id": 3, "cid": 2519, "compoundName": "Caffeine", "status": "nominal", "analyzedAt": "2026-09-17T12:00:00.000Z"})
            return
        self.send_json({"success": True})

    def do_DELETE(self):
        self.send_json({"success": True})

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        self.end_headers()

    def get_caffeine(self):
        return {
            "cid": 2519,
            "name": "Caffeine",
            "formula": "C8H10N4O2",
            "molecularWeight": 194.19,
            "iupacName": "1,3,7-trimethylpurine-2,6-dione",
            "smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
            "canonicalSmiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
            "inchi": "InChI=1S/C8H10N4O2/c1-10-4-9-6-5(10)7(13)12(3)8(14)11(6)2/h4H,1-3H3",
            "inchikey": "RYYVLZVUVIJVGH-UHFFFAOYSA-N",
            "imageUrl": "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2519/PNG",
            "properties": {
                "molecularWeight": 194.19,
                "logP": -0.07,
                "tpsa": 61.8,
                "hBondDonors": 0,
                "hBondAcceptors": 3,
                "rotatableBonds": 0,
                "complexity": 293
            },
            "admet": [
                {"endpoint": "HIA", "status": "high", "label": "Human Intestinal Absorption", "explanation": "Well absorbed across human intestinal barrier."},
                {"endpoint": "BBB", "status": "high", "label": "Blood-Brain Barrier", "explanation": "Readily permeates the blood-brain barrier."},
                {"endpoint": "CYP1A2", "status": "moderate", "label": "CYP1A2 Substrate", "explanation": "Major metabolic pathway mediated by CYP1A2."}
            ],
            "toxicity": [
                {"endpoint": "hERG", "status": "low", "label": "hERG Inhibition", "explanation": "Low risk of hERG channel blockade at physiological concentrations."},
                {"endpoint": "Ames", "status": "low", "label": "Ames Mutagenicity", "explanation": "Non-mutagenic in Ames test assay."}
            ],
            "drugLikeness": {
                "lipinski": "Passes Lipinski Rule of 5",
                "violations": 0,
                "summary": "MW < 500, LogP < 5, HBD < 5, HBA < 10. Suitable candidate."
            },
            "source": "PubChem"
        }

    def get_aspirin(self):
        return {
            "cid": 2244,
            "name": "Aspirin",
            "formula": "C9H8O4",
            "molecularWeight": 180.16,
            "iupacName": "2-acetyloxybenzoic acid",
            "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
            "canonicalSmiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
            "inchi": "InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)",
            "inchikey": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
            "imageUrl": "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/PNG",
            "properties": {
                "molecularWeight": 180.16,
                "logP": 1.19,
                "tpsa": 63.6,
                "hBondDonors": 1,
                "hBondAcceptors": 3,
                "rotatableBonds": 2,
                "complexity": 212
            },
            "admet": [
                {"endpoint": "HIA", "status": "high", "label": "Human Intestinal Absorption", "explanation": "Rapidly absorbed from stomach and small intestine."},
                {"endpoint": "BBB", "status": "moderate", "label": "Blood-Brain Barrier", "explanation": "Moderate central nervous system penetration."},
                {"endpoint": "PPB", "status": "moderate", "label": "Plasma Protein Binding", "explanation": "Moderate binding to serum albumin."}
            ],
            "toxicity": [
                {"endpoint": "hERG", "status": "low", "label": "hERG Inhibition", "explanation": "Negligible cardiac toxicity risk."},
                {"endpoint": "Hepatotoxicity", "status": "low", "label": "Liver Injury Risk", "explanation": "Low risk at therapeutic doses."}
            ],
            "drugLikeness": {
                "lipinski": "Passes Lipinski Rule of 5",
                "violations": 0,
                "summary": "MW < 500, LogP < 5, HBD < 5, HBA < 10. Meets all criteria."
            },
            "source": "PubChem"
        }

if __name__ == "__main__":
    print(f"Serving DrugScope at http://localhost:{PORT}")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), SPAHandler) as httpd:
        httpd.serve_forever()
