#!/usr/bin/env python3
"""Check topic rows, printed page references and the PDF's named destinations.

This checks navigation integrity; deciding whether an entry teaches the named
concept still requires editorial reading of its destination.
"""
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]


def groups(text):
    """Read consecutive brace groups, including nested TeX in label titles."""
    result = []
    cursor = 0
    while cursor < len(text):
        if text[cursor].isspace():
            cursor += 1
            continue
        if text[cursor] != '{':
            break
        start = cursor + 1
        depth = 1
        cursor += 1
        while cursor < len(text) and depth:
            if text[cursor] in '{}':
                # TeX literal \{ and \} do not change grouping depth.
                slashes = 0
                previous = cursor - 1
                while previous >= 0 and text[previous] == '\\':
                    slashes += 1
                    previous -= 1
                if slashes % 2 == 0:
                    depth += 1 if text[cursor] == '{' else -1
            cursor += 1
        if depth:
            raise ValueError('Unbalanced TeX label group')
        result.append(text[start:cursor - 1])
    return result


def normalized(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text)).replace('−', '-')


def audit():
    pdf = ROOT / 'build/main.pdf'
    aux = ROOT / 'build/main.aux'
    source = ROOT / 'chapters/quick-reference.tex'
    if pdf.stat().st_mtime < max(aux.stat().st_mtime, source.stat().st_mtime):
        raise RuntimeError('Finish the current build before auditing navigation.')
    document = fitz.open(pdf)
    destinations = document.resolve_names()
    labels, errors = {}, []
    for line in aux.read_text().splitlines():
        if not line.startswith('\\newlabel{'):
            continue
        key, value = groups(line[len('\\newlabel'):])[:2]
        fields = groups(value)
        if key in labels:
            errors.append(f'Duplicate label: {key}')
        if len(fields) >= 4:
            labels[key] = fields

    # Repeated long-table headers identify every page of the two topic tables.
    index_pages = [i for i, page in enumerate(document)
                   if '要查的概念' in normalized(page.get_text())]
    index_links = [link for i in index_pages for link in document[i].get_links()]
    rows = []
    for line in source.read_text().splitlines():
        if '\\pageref{' not in line:
            continue
        targets = re.findall(r'\\hyperref\[([^]]+)\]', line)
        pages = re.findall(r'\\pageref\{([^}]+)\}', line)
        if targets != pages:
            errors.append(f'Topic/page target mismatch: {line.split("&")[0].strip()}')
        entries = []
        for key in targets:
            if key not in labels:
                errors.append(f'Missing topic label: {key}')
                continue
            number, printed, title, anchor = labels[key][:4]
            destination = destinations.get(anchor)
            if not destination or not 0 <= destination['page'] < len(document):
                errors.append(f'Invalid topic destination: {key}')
                continue
            page_index = destination['page']
            if document[page_index].get_label() != printed:
                errors.append(f'Printed page disagrees with destination: {key}')
            hits = [link for link in index_links if link.get('nameddest') == anchor
                    and link.get('page') == page_index]
            if len(hits) < 2:
                errors.append(f'Topic text/page links not both present in PDF: {key}')
            entries.append(dict(label=key, section=number, title_tex=title,
                                printed_page=printed, pdf_page=page_index + 1,
                                destination=anchor, matching_pdf_link_annotations=len(hits)))
        rows.append(dict(topic_tex=line.split('&')[0].strip(), entries=entries))

    bookmarks = document.get_toc(False)
    missing_titles = []
    for level, title, one_based_page, detail in bookmarks:
        anchor = detail.get('nameddest')
        destination = destinations.get(anchor, {})
        if destination.get('page') != one_based_page - 1:
            errors.append(f'Bookmark page disagrees with named destination: {title}')
        if not 1 <= one_based_page <= len(document):
            errors.append(f'Bookmark outside document: {title}')
            continue
        if normalized(title) not in normalized(document[one_based_page - 1].get_text()):
            missing_titles.append(dict(title=title, pdf_page=one_based_page))
    if missing_titles:
        errors.append('Some bookmark titles were not found on their destination pages')
    if not rows or not index_pages or not bookmarks:
        errors.append('Navigation data missing')

    return dict(status='PASS' if not errors else 'FAIL',
                method='Compare each topic-row link with its page-reference label, '
                       'resolve PDF named destinations and printed page labels; '
                       'check bookmark destinations and visible title text. '
                       'Concept-to-entry relevance is reviewed manually.',
                pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
                pages=len(document), topic_rows=len(rows),
                topic_targets=sum(len(row['entries']) for row in rows),
                topic_table_pdf_pages=[i + 1 for i in index_pages],
                bookmarks=len(bookmarks), labels=len(labels),
                bookmark_titles_not_found=missing_titles, errors=errors, rows=rows)


if __name__ == '__main__':
    result = audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result['status'] != 'PASS':
        raise SystemExit(1)
