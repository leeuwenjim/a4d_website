import json
from django.utils.safestring import mark_safe


def __render_header(header_data):
    return f'<h{header_data["level"]}>{header_data["text"]}</h{header_data["level"]}>'

def __render_paragraph(paragraph_data):
    return f'<p>{paragraph_data["text"]}</p>'

def __render_list(list_data):
    open_tag = '<ol>'
    close_tag = '</ol>'

    if list_data['style'] == 'unordered':
        open_tag = '<ul>'
        close_tag = '</ul>'

    content = open_tag
    for item in list_data['items']:
        content += f'<li>{item}</li>'
    content += close_tag

    return content

def __render_delimitter(delimiter_data):
    return '<div class="page_delimiter"></div>'

def __render_table(table_data):
    content = '<table class="page_table">'

    head = None
    body = table_data['content']

    if len(table_data['content']) > 0 and table_data['withHeadings']:
        head = table_data['content'][0]
        body = table_data['content'][1:]

    if head is not None:
        content += '<thead><tr>'
        for item in head:
            content += f'<th>{item}</th>'
        content += '</tr></thead>'

    content += '<tbody>'
    for row in body:
        content += '<tr>'
        for cell in row:
            content += f'<td>{cell}</td>'
        content += '</tr>'
    content += '</tbody>'

    content += '</table>'
    return content

def render_page_content(page_data: str):
    data_blocks = json.loads(page_data)

    render_functions = {
        'header': __render_header,
        'paragraph': __render_paragraph,
        'list': __render_list,
        'delimiter': __render_delimitter,
        'table': __render_table
    }

    rendered_data = ''

    for block in data_blocks:
        rendered_data += render_functions[block['type']](block['data'])

    return mark_safe(rendered_data)
