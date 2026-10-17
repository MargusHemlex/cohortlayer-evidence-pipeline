# CohortLayeri avaliku näidise lähteülesanne

Versioon: 1.2 · 18. oktoober 2026

Nimeuuendus: kasutaja kinnitatud nimi on **CohortLayer Evidence Pipeline**, repo `cohortlayer-evidence-pipeline`. Muudatus puudutab nimesid ja viiteid; funktsionaalsed nõuded jäävad samaks.

## 1. Eesmärk ja positsioneerimine

Ehitame iseseisvalt käivitatava avaliku tarkvaranäidise, mis näitab geneetiliste tõendite päritolu, versioonimist, kahe sünteetilise kohordi eraldi tulemuste võrdlemist ja muutuste jälgimist. Sihtrühm on tehniline värbaja, CTO ja automatiseeritud koodihindaja. Näidis peab lubama väiteid koodi ja testidega kontrollida.

Näidis ei valideeri bioloogiliselt ravimi sihtmärki, ei tõenda põhjuslikkust ega sõltumatut teaduslikku replikatsiooni. See ei ühendu UK Biobanki, All of Usi ega teiste päriskohortidega. Päris allikast loetud tõend ja sünteetiline analüüs jäävad eraldi andmekihtideks; nende kokkulangevus ei ole uus teaduslik tõend.

Avaliku repo soovituslik nimi on `cohortlayer-evidence-pipeline`. Privaatse tootemootori jaoks reserveerime eraldi repo `cohortlayer-engine`. Mõlemad on praegu kavandatavad; see dokument ei kinnita olemasolevaid tootmisvõimekusi.

## 2. Esimese versiooni ulatus

1. Kolm kuni viis eelvalitud näidishüpoteesi, mitte vabavormiline teadusotsing.
2. Kaks lokaalset sünteetilist kohordiadapterit, nimedega `Cohort A` ja `Cohort B`.
3. Kohordipõhised sünteetilised mõju hinnangud koos määramatusega, eraldi tabelis; metaanalüüsi ega koondefekti ei arvutata.
4. Läbipaistev, versioonitud näitlik kooskõlareegel.
5. Kohordi väljundi kontroll, väikeste gruppide näidispoliitika ja veastsenaariumid.
6. Kaks muutumatut tõendiversiooni, deterministlik korduskäivitus ning muutuste raport.
7. Väike avalike teadusandmete väljavõte pärast kasutus- ja taasavaldamisõiguste kontrolli. Sünteetiline baasversioon peab töötama ka ilma selle lisamoodulita.
8. Ingliskeelsed README, koodinimed, CLI väljundid ja raportid. Käesolev lähteülesanne on eestikeelne.

Populatsiooni kirjeldus säilitatakse raportis; näidisreegel ei hinda päritolurühmade teaduslikku ülekantavust. Avaldatud hinnangute tehniline võrreldavus ei tähenda populatsioonide teaduslikku samaväärsust.

Versiooni 1 ei kuulu kasutajakontod, mitme kliendi teenus, maksed, LLM, mudeli treenimine, pilve juurutamine, päris kohordianalüüs, piiranguteta geenipäringud, üldine genoomiversioonide teisendamine ega tootmise automaatne seire. Uuendust näitab lokaalne käsuga käivitatav sündmus; ajastatud teenus jääb hilisemaks tööks.

## 3. Andmed ja allikate rollid

### 3.1 Sünteetiline baasversioon

Fikseeritud seemne ja selgesõnalise generaatoriversiooniga valmistatud andmed või fikseeritud koondstatistika-fixtuurid. Iga stsenaariumi eeldused on dokumenteeritud. Kahe sama generaatori väljundi võrdlus on tarkvaraloogika näide, mitte sõltumatu replikatsioon.

Versiooni 1 adapterid kasutavad fikseeritud sünteetilisi koondstatistika-fixtuure; individuaalsete genoomide generaator ei kuulu MVP-sse. Valikulises adapteri sisemises testis võib kasutada üksikrea sünteetilist materjali, kuid see ei ole baasversioon sisend ega väljund. Raportitesse ja tavapärastesse logidesse jõuavad ainult lubatud koondväljad. Baasversioon ei vaja internetti ega API võtit.

### 3.2 Avalike tõendite lisamoodul

| Allikas | Roll | Mida sellest ei järeldata |
|---|---|---|
| Open Targets | Geeni ja haiguse identifikaatorid, seose kontekst ning viited algtõendile | Skoori ei käsitleta kohordi efektihinnangu ega põhjuslikkuse tõendina |
| GWAS Catalog | Üksikute valitud uuringute seosed, uuringu-ID-d, olemasolul koondhinnangud ja metaandmed | Uuringut ei loeta teistest sõltumatuks ilma päritolu kontrollita |
| ClinVar | Variandi ja haigusseose tõlgendus, ülevaatuse staatus ja versioon | Kliiniline klassifikatsioon ei võrdu sihtmärgi valideerimise ega kohordi efektiga |

Open Targets võib sisaldada teiste nimetatud allikate tõendeid. Üht algtõendit ei loeta mitmeks sõltumatuks kinnituseks. Iga kirje säilitab algallika ja uuringu-/kirje-ID; identne allikakirje deduplikeeritakse. Võimalik valimite kattuvus märgitakse `known`, `possible` või `unknown`; pipeline ei väida kattuvuse täielikku lahendamist.

Enne konkreetse väljavõtte reposse lisamist dokumenteeritakse versioon, URL, allalaadimiskuupäev, litsents/tingimused, päritoluahel, omistamisnõuded ja taasavaldamise alus. Kontrollimata väljavõtte avaldamine ei ole lubatud. Kui taasavaldamine ei ole lubatud, kasutame tingimustega lubatud allalaadimistööriista või sünteetilist asendust. Baasversioon ja selle testid ei sõltu sellest võrgutoimingust.

Avalikud andmed on eraldi viitetõend; need ei määra varjatult sünteetilise stsenaariumi „õiget” tulemust. Reaalset tõendimuutust näitav lisamoodul vajab kaht tegelikku arhiveeritud versiooni. Väljamõeldud muutus märgitakse alati simulatsiooniks.

## 4. Kasutajavoog ja väljund

Kasutaja käivitab ühe ettevalmistatud hüpoteesi valitud versiooniga. Süsteem valideerib sisendi, käivitab adapterid eraldi, kontrollib väljundeid ja rakendab avaldamispoliitikat. Raport näitab kummagi kohordi tulemust, piiranguid ja kooskõla põhjendust. Eraldi jaotis näitab avalikku viitetõendit, kui lubatud väljavõte on lisatud.

Kasutaja käivitab sama hüpoteesi teise tõendiversiooniga ja saab eraldi jaotistes avaldamiskõlblike viitetõendikirjete ning sünteetiliste kohorditulemuste lisatud, eemaldatud ja muutunud väljade võrdluse. Klassifikaatori, hüpoteesile vastavuse ning lipu muutused näidatakse tuletatud järelduste jaotises sama avaldamispiiriga. Tegelik failimuutus ilma asjakohase sisumuutuseta ei tekita uut teaduslikku järeldust.

Väljundid on skeemivalideeritud JSON ja inimloetav Markdown-raport. Veebiliides on võimalik hilisem täiendus; CLI, raportid ja testid moodustavad versiooni 1.

## 5. Arhitektuur ja teostus

Soovituslik teostus on Python 3.12+, `pyproject.toml`, lukustatud sõltuvused, Pydantic/JSON Schema, pytest ja ruff. Python toetab hilisemat teadusarvutust; selles teostuses väldime tarbetuid andme- ja orkestreerimisraamistikke. Kohustuslik on üks dokumenteeritud konteinerita käivitustee. Docker ei ole eeltingimus.

Moodulid:

- `contracts`: hüpoteesi, viitetõendi, kohorditulemuse, manifesti ja raporti skeemid.
- `fixtures`: kolm kuni viis hüpoteesi ja nende stsenaariumid ning v1/v2 sünteetilised andmed.
- `adapters`: ühine adapterileping ja kaks sünteetilist teostust; repo ei sisalda päriskohordi ligipääse ega API võtmeid.
- `validation`: sisendi, väljundi ja võrreldavuse kontroll.
- `disclosure`: avaldamiseks lubatud koondväljundite moodustamine; raportid, diff ja kasutajale nähtavad vead kasutavad sama piiri.
- `comparison`: kohordipõhiste tulemuste näitlik kooskõlaklassifikaator.
- `provenance`: sisuräsid, versioonid, allikad ja muutumatud analüüsikirjed.
- `diff`: kahe versiooni lubatud semantiliste muutuste võrdlus.
- `reporting` ja `cli`: JSON/Markdown väljundid ning käivituskäsud.
- `tests`: ühik-, lepingu-, integratsiooni- ja korduvustestid.

Ühised JSON-lepingud võivad hiljem teenindada privaatset mootorit, kuid avalik repo ei impordi privaatset paketti ega vaja sellele ligipääsu.

## 6. Minimaalsed andmelepingud

### Hüpotees

`hypothesis_id`, `gene_id`, vajadusel `variant_id`, `trait_id`, oodatava mõju suund, analüüsiprotokolli versioon ja stsenaariumi-ID. Versioon 1 toetab ainult eelvalitud gene–trait ja variant–trait juhtumeid; ravimi annuse või modulatsiooni mõju ei modelleerita. Toetame üht dokumenteeritud genoomiversiooni (GRCh38) ning EFO fenotüübisõnastikku avalike kirjetega seostamiseks; väljamõeldud kõrvalfenotüüp jääb eraldi `SYNTHETIC:` nimeruumi. Kui variant/alleel ei sobitu, tagastatakse võrreldavuse probleem; vaikset teisendamist ei tehta.

### Tõendikirje

`evidence_id`, `source`, `source_record_id`, `study_id` olemasolul, `source_version`, `retrieved_at`, algallika URL, andmeliik (`public_reference` või `synthetic`), asjakohased identifikaatorid ja litsentsiviide. Puuduv uuringu-ID on `null` koos põhjusega. Sünteetilistel kirjetel on `retrieved_at=null` põhjusega `generated_fixture` ja eraldi fikseeritud `fixture_version`; päris allalaadimist ei teeselda. Allikaskoor, kliiniline klassifikatsioon ja statistiline efekt on eri tüüpi väljad.

### Kohorditulemus

- `cohort_id`, `hypothesis_id`, `analysis_version`, `dataset_version`, `data_kind=synthetic`.
- `execution_status`: `succeeded`, `failed` või `timeout`.
- `disclosure_status`: `released`, `suppressed` või `not_applicable`. `not_applicable` kehtib tõrke või aegumise korral, kui hinnatavat statistikat ei tekkinud; edukal statistilisel tulemusel on staatus `released` või `suppressed`.
- Efektitüüp, hinnang ja kohustuslik 95% usaldusvahemik igal edukal avaldatud efektitulemusel; standardviga võib olla lisaväli. Populatsiooni kirjeldus, olemasolul valimi ja kandjate arv. Ainult standardveaga tulemus on `invalid_output`; pipeline ei tuleta sellest usaldusvahemikku.
- Puuduv väärtus on `null` koos põhjusekoodiga, mitte 0. Ebaõnnestunud või peidetud tulemus ei sisalda avaldamata statistikat.
- Mõju suund määratletakse fenotüübi ja efektimõõdiku suhtes; näiteks väiksem biomarker ei tähenda automaatselt väiksemat haigusriski.
- Variantide korral säilivad efektialleel ja referentsalleel; sünteetilise geenikontrasti korral säilib kontrasti-ID ning võrreldavate rühmade järjekord. Fenotüübi kodeering ja mõõtühik on kohustuslikud. Vastupidise orientatsiooni, erineva ühiku või kodeeringuga paari versioon 1 ei normaliseeri, vaid märgib võrreldamatuks.
- Statistilised väärtused peavad olema lõplikud arvud, standardviga mittenegatiivne, intervalli alumine ots ülemisest väiksem või võrdne ning hinnang intervalli sees. Suhtemõõdikud ja nende intervallid on positiivsed; loendid mittenegatiivsed täisarvud ning kandjate arv ei ületa valimi suurust. Vigane statistika ei jõua klassifikaatorisse.

### Võrdlusraport

`run_status`: `complete`, `partial` või `failed`; `comparison_status`: `concordant`, `conflicting`, `inconclusive` või `not_evaluable`; masinloetavad põhjusekoodid; kohorditulemused; avalik viitetõend eraldi; manifesti ID ja piirangud.

Kooskõlareegel on teostuses ette määratud ja testitav: võrreldava mõõdiku kaks avaldatud hinnangut, mille 95% intervallid jäävad nullmõju samale poolele, annavad `concordant`; vastaspooltele jäävad intervallid annavad `conflicting`; nullmõju hõlmav intervall annab `inconclusive`. Puuduv, peidetud või võrreldamatu paar annab `not_evaluable`. Nullmõju on beetal 0 ja suhtemõõdikul 1. Heterogeenseid fenotüüpe või mõõdikuid ei võrrelda. See on näitlik reegel, mitte valideeritud teadusprotokoll.

Üks õnnestunud kohort ja üks tõrge annab `partial` ning `not_evaluable`. Osalise jooksu õnnestunud kohordi tulemus läbib sama avaldamiskontrolli ja selle lubatud väljad kuvatakse raportis. Täielikult käivitatud, kuid peidetud või ebaselge analüüs võib olla `complete`; see ei tähenda toetavat teadustulemust.

Lõplik staatus määratakse pärast skeemi- ja semantilist kontrolli. Vigane adapteri väljund teisendatakse `failed` tulemuseks koos kontrollitud põhjusekoodiga `invalid_output`; toorvastust ei avaldata. Adapteri aegumise piir on versioonitud konfiguratsioonis (teostuses vaikimisi 5 sekundit); stsenaariumitest süstib deterministliku timeout-tulemuse, mitte ei sõltu võrgu viivitusest või kellaajast.

| Adapterite kontrollitud tulemus | `run_status` | `comparison_status` |
|---|---|---|
| Mõlemad `failed`/`timeout` | `failed` | `not_evaluable` |
| Täpselt üks `succeeded` | `partial` | `not_evaluable` |
| Mõlemad `succeeded`, vähemalt üks peidetud või paar võrreldamatu | `complete` | `not_evaluable` |
| Mõlemad `succeeded`, avaldatud ja võrreldavad | `complete` | Intervallireegli järgi `concordant`, `conflicting` või `inconclusive` |

Kõigepealt kontrollitakse käivitust, avaldamisstaatust ja võrreldavust. Võrreldava paari puhul piisab ühe intervalli nullmõju hõlmamisest, et anda `inconclusive`; alles seejärel kontrollitakse samasuunalist või vastassuunalist kooskõla. Intervalli nullmõjuga võrdne otspunkt kuulub `inconclusive` alla. `concordant` tähendab kohortide omavahelist kooskõla; see võib olla hüpoteesi oodatavale suunale vastupidine. Raport näitab eraldi `direction_vs_hypothesis`: `matches`, `opposes`, `mixed` või `not_assessable`; hinnang antakse ainult nullmõjust eristatavate, avaldatud ja võrreldavate tulemuste korral. Mõlemad oodatud suunas → `matches`, mõlemad vastassuunas → `opposes`, vastassuunalised omavahel → `mixed`, muudel juhtudel `not_assessable`.

Fenotüübilipu reegel `pipeline-flag-v1` kasutab ainult eraldi sünteetilist kõrvalfenotüüpi `SYNTHETIC:ADVERSE_EVENT` ja mõõdikut šansside suhe (OR). `triggered` kehtib, kui kontrollitud ja avaldatud 95% intervalli alumine piir on rangelt suurem kui 1; muul hinnataval juhul on tulemus `not_triggered`. Puuduva, peidetud, vigase või ebaõnnestunud sisendi puhul on tulemus `not_assessable`. Mõlemad kohordid saavad eraldi lipu, neid ei koondata. Testid katavad kõik kolm tulemust ja piiri 1. See on väljamõeldud fenotüübi tehniline lipureegel, mitte kliinilise ohutuse tõend.

### Manifest

Sisendi räsi, andmete ja reeglite versioonid/räsid (kohorditulemuse `analysis_version` ja `dataset_version` peavad neile täpselt vastama), avaldamispoliitika versioon ja konfiguratsiooni räsi, generaatori seeme/versioon (fikseeritud koondfixtuuridel `null` põhjusega `fixed_aggregate_fixture`; fixtuuriversioon on alati olemas), koodi versioon, skeemiversioon ja kasutatud allikate identifikaatorid. Muutuvad töötlusajad ja kohalikud failiteed on eraldi operatiivmetaandmed ega mõjuta kanoonilist tulemusräsi. Sama sisend, versioonid ja kood annavad sama kanoonilise JSON-i ning sama räsi. Manifestid salvestatakse sisuräsi järgi. Sama kanoonilise sisuga manifesti kordus on idempotentne: olemasolev fail tagastatakse muutmata. Sama ID all erinev sisu põhjustab tervikluskontrolli vea (rikutud fail või räsikollisioon); uut versiooni salvestatakse uue räsi alla. Ülekirjutamise lippu ei ole. Kanooniline JSON kasutab RFC 8785 serialiseerimist ja SHA-256 räsi; NaN ja lõpmatus on keelatud ning ebastabiilse järjekorraga kirjekogud sorditakse enne serialiseerimist stabiilse ID järgi. Keskkond ja sõltuvused on lukustatud; korduvustest ei sõltu kohalikust ajatsoonist.

Raporti andmepäritolu on `synthetic` või `mixed`; segaraportis märgistatakse iga tõendikihi päritolu. Avalikku faktikirjet ei nimetata sünteetiliseks ja sünteetilist tulemust ei esitata päris mõõtmisena. Märgistus säilib igas iseseisvalt eksporditavas väljundis.

## 7. Avaldamispoliitika ja piirangud

Pipeline kasutab avalikult dokumenteeritud, versioonitud konfiguratsioonis väikese grupi lävendit `k=10`: alla 10 kandja või juhtumi korral peidetakse seotud statistika. Puuduva loendiga sünteetiline tulemus peidetakse põhjusega `disclosure_input_missing`; puuduvat arvu ei oletata. See on näidispoliitika, mitte ühegi kohordi pärispoliitika ega formaalne privaatsusgarantii. Piiratud loendiga seotud hinnangud ja tuletatavad väljad eemaldatakse koos loendiga. Vigadesse, logidesse, raportisse ega diff-väljundisse ei kopeerita adapteri toorvastust.

Diff töötab ainult avaldamiskõlblike kujutistega. Kui ühe versiooni tulemus on peidetud, ei väljastata peidetud arve, efekte, täpseid deltasid ega tagasijäreldust hõlbustavaid põhjendusi. Olekumuutus võib anda ainult üldise teate piiratud võrreldavusest. Testid sisaldavad lävendi ületamist versioonide vahel. Ka siis ei väida me, et korduvate päringute või välise info põhine tuletamine on täielikult välistatud.

## 8. Kohustuslikud stsenaariumid

1. Sama suunaga, nullmõjust eristatavad sünteetilised hinnangud → `concordant`.
2. Vastassuunalised, nullmõjust eristatavad hinnangud → `conflicting`.
3. Nullmõju hõlmav intervall vähemalt ühes kohordis → `inconclusive`; pelgalt intervalli laius ei muuda klassi.
4. Väike grupp → piiratud väljad peidetud, paar `not_evaluable`.
5. Kohort B ebaõnnestub/aegub → `partial`, mitte „tõend puudub” ega „replikatsioon õnnestus”.
6. Vale skeem, erinev alleel/build/fenotüüp või efektimõõdik → ohutu tagasilükkamine/võrreldamatus.
7. v1 → v2: lisatud, eemaldatud või muutunud lubatud kirjed → täpne diff ja uus sisuräsi.
8. Sama versiooni korduskäivitus → sama kanooniline tulemus.
9. Sama algtõend kahes sünteetilises allikakirjes → kattuvus märgitud, sõltumatut kinnitust ei lisandu. Baasversioon kasutab selleks fiktiivseid allika-ID-sid ja sünteetiliseks märgitud kirjeid; tegelikke avalikke väljavõtteid see test ei vaja. Kõik kümme stsenaariumi peavad olema testitavad ainult sünteetiliste fixtuuridega.
10. Fiktiivne fenotüübilipp → täpne näidis-lipureegli selgitus; „lipp ei käivitunud” ei tähenda „ohutu”. See on eraldi näitlik lipp, mitte kliiniline ohutushinnang.

Kolm kuni viis hüpoteesi võivad olla mitme stsenaariumi sisendiks; kümme eraldi bioloogilist juhtumit ei ole vajalikud.

## 9. Avalik ja privaatne osa

| Avalik `cohortlayer-evidence-pipeline` | Privaatne `cohortlayer-engine` |
|---|---|
| Avalikud JSON-skeemid ja adapteriliides | Päriskohortide adapterid, päringud ja töötluskonfiguratsioon |
| Sünteetilised andmed/generaator ja A/B adapterid | Ligipääsud, võtmed, kontod ja keskkonnaseadistus |
| Lihtsustatud avalik kooskõlareegel, mille loogika on täielikult loetav | Tootmise kaitstav statistiline metoodika, skoorimine ja harmoniseerimise erilahendused |
| Näitlik väljundivalvur ning selle teadaolevad piirangud | Kohordispetsiifilised konfidentsiaalsed kontrollid ja operatiivprotsessid |
| Versioonimine, päritolumanifest, diff ja raportigeneraator | Klientide hüpoteesid, lepingud, tulemused ja päringuajalugu |
| Kontrollitud õigustega avalikud väljavõtted ja omistused | Piiratud ligipääsuga või taasavaldamisõiguseta andmed |
| Testid, näidisraportid, CI, arhitektuuriotsused ja piirangud | Tootmise taristu, seire, auditikirjed ja juurutuskonfiguratsioon |

Privaatne piir ei tähenda, et kõik tulevased komponendid juba olemas oleksid. Avalik näidis kirjeldab asendatud osi selgelt. Avalikus repos ei ole privaatseid submoduleid, sõltuvusi ega privaatsetest failidest genereeritud bundle'e. Väljavõtted, testifixtuurid ja commit-ajalugu kuuluvad samasse avaldamiskontrolli.

## 10. Vastuvõtukriteeriumid

- AC01: README üks käivitusrada loob puhtas toetatud keskkonnas baasversioon ilma API võtme ja runtime-võrguta; sõltuvuste esmainstalli vajadus on dokumenteeritud.
- AC02: vähemalt kolm eelvalitud hüpoteesi; kõik kohustuslikud stsenaariumid on automaattestides kaetud.
- AC03: sisendid ja kõik eksporditavad JSON-id valideeruvad suletud skeemide vastu; ootamatud väljad ei jõua raportisse.
- AC04: kohordi mõõdikuid ei ühendata koondefektiks; vale mõõdiku/alleeli/build/trait kombinatsioon ei anna kooskõlaväidet.
- AC05: tõrge, määramatus ja peitmine on eraldi masinloetavad seisundid. Puuduvad arvud ei muutu nullideks. Testid katavad kõik staatuste tabeli harud, efekti orientatsiooni ja hüpoteesile vastupidise kooskõla ning lipureegli kolm tulemust.
- AC06: iga eksporditav raport säilitab andmekihtide päritolu ja sünteetiliste tulemuste märgistuse.
- AC07: sama versiooni kordusjooks annab sama kanoonilise JSON-i ja räsi; failisüsteemi asukoht ja kellaaeg seda ei muuda.
- AC08: v1/v2 muutused on seletatavad kirjete ja versioonide kaudu; väljund ei avalda peidetud väärtusi ega nende deltasid.
- AC09: väljundipiiri testid kontrollivad ka logisid, vigu, raporteid ja diff'i; ebaõnnestumise korral avaldatakse ainult kontrollitud veakood.
- AC10: avalikud snapshot'id lisatakse alles pärast konkreetsete versioonide kasutusõiguste dokumenteerimist. Selle kontrolli puudumisel väljastatakse ainult sünteetiline baasversioon.
- AC11: CI käivitab vormingu/lindi, skeemi-, ühik-, integratsiooni- ja korduvustestid ning saladuste kontrolli. CI ei vaja päriskohordi ega tasulise teenuse võtit.
- AC12: README sisaldab eesmärki, sinu tegelikku panust, arhitektuuri, käivitusnäidet, vähemalt üht näidisraportit, allikate päritolu, avaliku/privaatse osa piiri ning teaduslikke piiranguid.
- AC13: avalik repo ei sisalda privaatse mootori sõltuvust, kliendimaterjali, saladusi ega kasutusõiguseta andmeid; repo koodilitsents ja andmete litsentsid on eristatavad.

## 11. Tööde järjekord ja valmimine

1. Skeemid, staatuste tähendus, kolm kuni viis sünteetilist hüpoteesi ja avalik/privaatne piir.
2. Adapterid, väljundivalvur ja võrreldavuse kontroll koos testidega.
3. Võrdlusraport, manifest ja deterministlik käivitus.
4. Teine tõendiversioon ja privaatsuspiiriga diff.
5. Avalike väljavõtete õiguste kontroll ning lubatud lisamoodul; sünteetilise baasversioon valmimist see ei peata.
6. README, näidisväljundid ja CI; nõuetele vastavuse kontroll enne avaldamist.

Valmisolek tähendab AC01–AC13 läbimist ja piirangute täpset dokumenteerimist. Käesoleva ülesande tulemuseks on lähteülesanne, mitte repo loomine ega avaldamine. Avaliku näidise ehitamine ja GitHubi avaldamine on järgmised eraldi tööd.

## 12. Algallikad

- CohortLayeri toote kirjeldus: https://cohortlayer.com/
- Open Targets andmeallikad: https://platform-docs.opentargets.org/gentropy/data-sources
- Open Targets tõendid: https://platform-docs.opentargets.org/evidence
- Open Targets allalaadimised: https://platform.opentargets.org/downloads/data
- GWAS Catalogi koondstatistika: https://www.ebi.ac.uk/gwas/docs/summary-statistics/
- ClinVari andmete kasutamine: https://www.ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/

Allikaloend ei asenda konkreetse väljavõtte õiguste kontrolli. Ülevaatajate hinnangud on spetsifikatsiooni kvaliteedikontroll, mitte teaduslik või juriidiline sertifikaat.
