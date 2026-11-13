"""Test de bout en bout de « Ma classe » (Playwright, sans interface).
Usage : python3 test_page.py [chemin/index.html]
Vérifie : accueil à 2 portes, écran Mes applis, retour, bouton Retour du
navigateur, liens en nouvel onglet et en ligne, QR code, aucune erreur JS."""
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
    page.goto(url); page.wait_for_timeout(500)

    vis = lambda s: page.locator(s).is_visible()
    ok(vis('#ecran-accueil') and not vis('#ecran-applis'), 'accueil affiché seul')
    ok(page.locator('.porte').count() == 2, 'deux portes : Mes applis et Mon suivi')
    ok(not vis('#retour'), 'pas de bouton Accueil sur l’accueil')
    ok(page.locator('meta[name=robots][content*=noindex]').count() == 1, 'page non référencée (noindex)')
    ok(page.evaluate("document.fonts.check('600 20px Figtree')"), 'police Figtree chargée')

    data = page.evaluate('window.__appli')
    ok([a['nom'] for a in data['applis']] == ['Halloween', 'Minecraft', 'Dictée flash', 'La Foire de Liège'], 'les 4 applis demandées, dans l’ordre')
    liens = [data['suivi']] + [l[1] for a in data['applis'] for l in a['liens']]
    ok(len(set(liens)) == len(liens), f'{len(liens)} liens, sans doublon')

    # Mon suivi : nouvel onglet vers la page du suivi
    with ctx.expect_page() as nouvel:
        page.click('[data-porte=suivi]')
    ok(nouvel.value.url.rstrip('/').endswith('suivi-eleves'), 'Mon suivi ouvre la page du suivi')
    nouvel.value.close()
    ok(vis('#ecran-accueil'), 'l’accueil reste affiché derrière')

    # Mes applis
    page.click('[data-porte=applis]'); page.wait_for_timeout(300)
    ok(vis('#ecran-applis') and not vis('#ecran-accueil'), 'écran Mes applis')
    ok(page.locator('#ecran-applis .card').count() == 4, '4 cartes')
    ok(vis('#retour'), 'bouton Accueil visible')
    cibles = page.eval_on_selector_all('#ecran-applis a.btn', 'l=>l.map(a=>a.target+"|"+a.rel)')
    ok(len(cibles) == 6 and all(c == '_blank|noopener' for c in cibles), '6 boutons, tous en nouvel onglet')
    with ctx.expect_page() as nouvel:
        page.locator('.card[data-id=foire] a.btn').click()
    nouvel.value.close()

    # Retour : bouton de la page, puis bouton Retour du navigateur
    page.click('#retour'); page.wait_for_timeout(300)
    ok(vis('#ecran-accueil') and not vis('#retour'), 'bouton Accueil ramène à l’accueil')
    page.click('[data-porte=applis]'); page.wait_for_timeout(200)
    page.go_back(); page.wait_for_timeout(300)
    ok(vis('#ecran-accueil'), 'bouton Retour du navigateur ramène à l’accueil')

    # Ouverture directe de #applis, puis Accueil
    page.goto(url + '#applis'); page.reload(); page.wait_for_timeout(300)
    ok(vis('#ecran-applis'), 'adresse #applis ouvre Mes applis')
    page.click('#retour'); page.wait_for_timeout(300)
    ok(vis('#ecran-accueil'), 'puis Accueil fonctionne')

    page.click('#qrBtn'); ok(page.locator('#qrModal.on .qr-image svg').count() == 1, 'QR code affiché')
    page.keyboard.press('Escape'); ok(page.locator('#qrModal.on').count() == 0, 'QR fermé avec Échap')
    ok(not erreurs, 'aucune erreur JavaScript ' + ('; '.join(erreurs) if erreurs else ''))
    nav.close()

for l in liens:
    try:
        code = urllib.request.urlopen(urllib.request.Request(l, method='HEAD'), timeout=10).status
    except Exception as e:
        code = getattr(e, 'code', str(e))
    ok(code == 200, f'en ligne ({code}) : {l}')

print('\nRÉSULTAT :', 'tout est bon' if not fautes else f'{len(fautes)} problème(s)')
sys.exit(1 if fautes else 0)
