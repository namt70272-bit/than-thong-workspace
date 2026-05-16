import json
data = json.load(open(r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\_audit\trivy-fs.json'))
print(f'Results: {len(data.get("Results",[]))} results')
results = data.get("Results",[])
for r in results:
    target = r.get("Target","?")
    vulns = len(r.get("Vulnerabilities",[]))
    secrets = len(r.get("Secrets",[]))
    print(f'  Target: {target} - Vulns: {vulns}, Secrets: {secrets}')
