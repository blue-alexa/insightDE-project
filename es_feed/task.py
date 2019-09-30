def download_parse_insert(url):
    from downloader import download
    from parser import ThirteenFHRParser
    from es_loader import ESLoader

    id = url.split("/")[-1].split(".")[0]
    content = download(url)
    parser = ThirteenFHRParser()
    data = parser.parse(content, id)
    print(data)
    loader = ESLoader()
    index_name = "13f-hr"
    type_name = "form"
    loader.insert(index_name, type_name, id, data)


