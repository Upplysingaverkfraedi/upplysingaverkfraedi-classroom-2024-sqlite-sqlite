import requests
import pandas as pd
import argparse
import re


def parse_arguments():
    parser = argparse.ArgumentParser(description='Vinna með úrslit af tímataka.net.')
    parser.add_argument('--url', help='Slóð að vefsíðu með úrslitum.')
    parser.add_argument('--output', required=True,
                        help='Slóð að útgangsskrá til að vista niðurstöðurnar (CSV format).')
    parser.add_argument('--debug', action='store_true',
                        help='Vistar html í skrá til að skoða.')
    return parser.parse_args()


def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Tókst ekki að sækja gögn af {url}")
        return None


def parse_html(html):
    """
    Regluleg segð til að vinna úr HTML gögnum og skrá niðurstöður keppenda.

    """

    # Finna thead (dálkaheiti)
    thead_pattern = re.compile(r'<thead>(.*?)<\/thead>', re.DOTALL)
    thead_content = thead_pattern.search(html)

    # r'<thead>(.*?)<\/thead>': Leitar að <thead> og </thead> tags í html skráinni, sem táknar hausinn (header) á töflunni
    # (.*?): Leitar að einhverju efni á milli thead.
    # <\/thead>: leitar að lokataginu fyrir headerinn. Notum \/ til að sleppa skástrikinu. 

    # Ef ekkert thead finnst, prentar villuboð og skilar tómum lista
    if not thead_content:
        print("Engir dálkahausar fundust í HTML skránni.")
        return []
    
    #Sækir innihald thead sem HTML kóða
    thead_html = thead_content.group(1)
    
    # Finna dálkaheiti með th tag
    th_pattern = re.compile(r'<th.*?>(.*?)<\/th>', re.DOTALL)
    #<th.*?>: Leitar að byrjunartaginu <th>, en .*? segir segðinni að leita framhjá öllum "skrítnum" orðum sem eru í taginu eins og t.d <th class="header">
    # Punkturinn . stendur fyrir hvaða staf sem er og *? merkir "núll eða fleiri" stök og hættir við fyrsta lokunartag. 

    # Hreinsar HTML tags frá dálkaheitum og skilar lista af dálkaheitum
    column_headers = [re.sub(r'<.*?>', '', th).strip() for th in th_pattern.findall(thead_html)]
    # r'<.*?>', '', th: Notað til að hreinsa út HTML tags. 
    # <.*?>: Leitar að hvaða html tagi sem er (eh sem byrjar á < og endar á >). 
    # re.sub(r'<.*?>', '', th): Skiptir út öllu HTMl taginu með tómum streng, basically fjarlægir þau en innihaldið í þeim verður eftir. 

    print(f"Dálkaheiti fundust: {column_headers}")

    # Finna tbody hluta (gögnin sjálf) með regex
    tbody_pattern = re.compile(r'<tbody>(.*?)<\/tbody>', re.DOTALL)
    tbody_content = tbody_pattern.search(html)

    # Ef ekkert tbody finnst, prentar villuboð og skilar tómum lista
    if not tbody_content:
        print("Engin gögn fundust í HTML skránni.")
        return []
    
    # Sækir tbody sem HTML kóða
    tbody_html = tbody_content.group(1)

    # Finna allar raðir keppenda (tr) með regex
    tr_pattern = re.compile(r'<tr>(.*?)<\/tr>', re.DOTALL)
    # Þetta virkar mjög svipað og thead segðin. 
    tr_matches = tr_pattern.findall(tbody_html)

    results = []

    # Finna td (gildi í hverjum reit) fyrir hverja röð (tr)
    td_pattern = re.compile(r'<td.*?>(.*?)<\/td>', re.DOTALL)

    # Vinnur úr hverri röð (tr) til að finna gögnin (td)
    for tr in tr_matches:
        td_values = td_pattern.findall(tr)
        if td_values:
            # Hreinsa óþarfa hvít bil og HTML tags frá td gögnum
            clean_values = [re.sub(r'<.*?>', '', td).strip() for td in td_values]
            # Ef td gildi eru fleiri en dálkaheiti, skerum td gildin niður svo þau passi við dálkaheiti
            clean_values = clean_values[:len(column_headers)]
            # Býr til orðabók (dictionary) með dálkaheitum og samsvarandi td gildum
            row = dict(zip(column_headers, clean_values))
            # Bætir röðinni við niðurstöðu listann
            results.append(row)

    return results


def skrifa_nidurstodur(data, output_file):
    """
    Skrifar niðurstöður í úttaksskrá.
    :param data:        (list) Listi af línum
    :param output_file: (str) Slóð að úttaksskrá
    :return:            None
    """
    if not data:
        print("Engar niðurstöður til að skrifa.")
        return

    df = pd.DataFrame(data)
    df.to_csv(output_file, sep=',', index=False)
    print(f"Niðurstöður vistaðar í '{output_file}'.")


def main():
    args = parse_arguments()

    if not args.output.endswith('.csv'):
        print(f"Inntaksskráin {args.output} þarf að vera csv skrá.")
        return

    if not re.match(r'https:\/\/(www\.)?timataka\.net\/.*urslit.*', args.url):
        print("Slóðin er ekki frá timataka.net eða sýnir ekki úrslit.")
        return

    html = fetch_html(args.url)
    if not html:
        raise Exception("Ekki tókst að sækja HTML gögn, athugið URL.")

    if args.debug:
        html_file = args.output.replace('.csv', '.html')
        with open(html_file, 'w') as file:
            file.write(html)
        print(f"HTML fyrir {args.url} vistað í {html_file}")

    results = parse_html(html)
    skrifa_nidurstodur(results, args.output)


if __name__ == "__main__":
    main()