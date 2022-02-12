def full_url(base: str = None, *urls: List[str]) -> str:
    """Concat a bunch of urls.

    Parameters
    ----------
    base : str
        The optional base URL to use if no full url is given to urls.
    urls : List[str]
        The url snippets

    Returns
    -------
    str
        - The URL if only a single and valid one is given
        - The base and all urls snippets appended to it

    Raises
    ------
    ValueError
        The given url is invalid and no base was given.

    """
    if len(urls) == 1 and '://' in urls[0]:
        return urls[0]
    if not base: raise ValueError('The given url is invalid and no base was given.')
    if not base.endswith('/'):
        base += '/'
    for url in urls:
        if url.startswith('/'):
            url = url[1:]
        base += url
        if not base.endswith('/'):
            base += '/'
    return base
