def format_description(description):
    """
    Formats a job description into HTML.

    This function takes a job description string, splits it into lines,
    and formats each line as either a list item or a paragraph, based on
    whether it starts with an asterisk (*).

    Args:
        description (str): The job description to format.

    Returns:
        str: The formatted job description as an HTML string.
    """
    lines = description.split('\n')
    formatted_lines = ['<ul>'] + ['<li>' + line[1:].strip() + '</li>' if line.startswith('*') else '<p>' + line + '</p>' for line in lines]
    formatted_lines.append('</ul>')
    return ''.join(formatted_lines)
