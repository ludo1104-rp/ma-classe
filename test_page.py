"""Test de bout en bout de « Mes applis » (Playwright, sans interface).
Usage : python3 test_page.py [chemin/index.html]
Vérifie : aucune erreur JS, liens uniques et en ligne, nouvel onglet,
« Dernière ouverte » gardée après rechargement, aide, réglages, QR code."""
import sys, pathlib, urllib.request
from playwright.sync_api import sync_playwright

page_html = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).with_name('index.html')).resolve()
url = page_html.as_uri()
fautes = []
def ok(cond, msg):
    print(('OK   ' if cond else 'ERR  ') + msg)
    if not cond: fautes.append(msg)

with sync_playwright() as p:
    nav = p.chromium.launch()
    ctx = nav.new_context(viewport={'width': 820, 'height': 1180})
    page = ctx.new_page()
    erreurs = []
    page.on('pageerror', lambda e: erreurs.append(str(e)))
    page.goto(url); page.wait_for_timeout(400)

    data = page.evaluate('window.__appli')
    liens = [data['suivi']['lien']] + [a['lien'] for a in data['applis']]
    ids = [a['id'] for a in data['applis']]
    ok(len(set(ids)) == len(ids), f'{len(ids)} applis, identifiants uniques')
    ok(len(set(liens)) == len(liens), 'liens uniques')
    ok(page.locator('a.tile').count() == len(ids), 'une tuile par appli')
    ok(page.locator('a.suivi').count() == 1, 'tuile Mon suivi présente')
    cibles = page.eval_on_selector_all('a[data-id]', 'l=>l.map(a=>a.target+"|"+a.rel)')
    ok(all(c == '_blank|noopener' for c in cibles), 'tous les liens ouvrent un nouvel onglet')
    ok(page.locator('meta[name=robots][content*=noindex]').count() == 1, 'page non référencée (noindex)')

    # Clic sur une appli : nouvel onglet + « Dernière ouverte »
    with ctx.expect_page() as nouvel:
        page.locator('a.tile[data-id=a3]').click()
    nouvel.value.close()
    ok(page.locator('a.tile[data-id=a3] .recent').count() == 1, 'badge « Dernière ouverte » après le clic')
    page.reload(); page.wait_for_timeout(300)
    ok(page.locator('.recent').count() == 1 and page.locator('a.tile[data-id=a3] .recent').count() == 1, 'badge gardé après rechargement')
    with ctx.expect_page() as nouvel:
        page.locator('a.tile[data-id=a1]').click()
    nouvel.value.close()
    ok(page.locator('.recent').count() == 1 and page.locator('a.tile[data-id=a1] .recent').count() == 1, 'un seul badge, déplacé')

    # Ancienne valeur inconnue : aucune erreur
    page.evaluate("localStorage.setItem('mes-applis-derniere','\"zz9\"')"); page.reload(); page.wait_for_timeout(300)
    ok(page.locator('.recent').count() == 0, 'identifiant supprimé ignoré sans erreur')

    # Aide, réglages, QR
    page.click('#helpBtn'); ok(page.locator('#helpModal.on').count() == 1, 'aide ouverte')
    for _ in range(3): page.click('#helpNext')
    ok(page.locator('#helpModal.on').count() == 0, 'aide refermée après 3 étapes')
    page.click('#reglBtn'); page.click('[data-sty=simple]')
    ok(page.evaluate("document.body.classList.contains('simple')"), 'style Simple')
    page.click('#reglClose'); page.reload(); page.wait_for_timeout(300)
    ok(page.evaluate("document.body.classList.contains('simple')"), 'style gardé après rechargement')
    page.click('#qrBtn'); ok(page.locator('#qrModal.on .qr-image svg').count() == 1, 'QR code affiché')
    ok(not erreurs, 'aucune erreur JavaScript ' + ('; '.join(erreurs) if erreurs else ''))
    nav.close()

# Les adresses répondent-elles ?
for l in liens:
    try:
        code = urllib.request.urlopen(urllib.request.Request(l, method='HEAD'), timeout=10).status
    except Exception as e:
        code = getattr(e, 'code', str(e))
    ok(code == 200, f'en ligne ({code}) : {l}')

print('\nRÉSULTAT :', 'tout est bon' if not fautes else f'{len(fautes)} problème(s)')
sys.exit(1 if fautes else 0)
