def full_url(base, *urls):
    if len(urls) == 1 and '://' in urls[0]:
        return urls[0]

    if not base.endswith('/'):
        base += '/'
    for url in urls:
        if url.startswith('/'):
            url = url[1:]
        base += url
        if not base.endswith('/'):
            base += '/'
    return base
