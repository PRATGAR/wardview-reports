MAX_PAGE_SIZE = 200


def window(page, size, default_size=50):
    size = size if size and 0 < size <= MAX_PAGE_SIZE else default_size
    page = page if page and page > 0 else 1
    return size, (page - 1) * size


def envelope(items, page, size, total=None):
    return {
        "items": items,
        "page": page,
        "size": size,
        "total": total if total is not None else len(items),
    }
