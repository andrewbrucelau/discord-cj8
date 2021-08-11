from typing import Any, List, Optional


def make_table(rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False) -> str:
    """
    :param rows: 2D list containing objects that have a single-line representation (via `str`).
    All rows must be of the same length.
    :param labels: List containing the column labels. If present, the length must equal to that of each row.
    :param centered: If the items should be aligned to the center, else they are left aligned.
    :return: A table representing the rows passed in.
    """

    # Calculate column widths #
    max_columns = 0
    for row in rows:
        max_columns = max(max_columns, len(row))
    if labels:
        max_columns = max(max_columns, len(labels))

    column_widths: List[int] = [0] * max_columns

    def find_width(row: List[Any]):
        """Calculate width of text for a row and accumulate in column_widths."""
        for index, item in enumerate(row):
            column_widths[index] = max(column_widths[index], len(str(item)))

    for row in rows:
        find_width(row)

    if labels:
        find_width(labels)

    # Generate separator rows
    def render_row(left: str, sep: str, right: str, content: List[str]) -> str:
        """Return a string of a row."""
        guts = sep.join(content)
        return left + guts + right

    hline_content = ['─' * (width+2) for width in column_widths]
    top_line = render_row('┌', '┬', '┐', hline_content)
    mid_line = render_row('├', '┼', '┤', hline_content)
    bot_line = render_row('└', '┴', '┘', hline_content)

    # Generate label and row content
    def render_row_content(row_items: List[Any]) -> List[str]:
        """Return a list of padded row items."""
        result: List[str] = []
        for index, item in enumerate(row_items):
            total_padding = column_widths[index] - len(str(item))
            padding_left = total_padding // 2 if centered else 0
            padding_right = total_padding - padding_left
            rendered_item = (
                    ' '
                    + ' ' * padding_left
                    + str(item)
                    + ' ' * padding_right
                    + ' '
            )
            result.append(rendered_item)
        return result

    # Put together table
    table_rows: List[str] = [top_line]
    if labels:
        header_content = render_row_content(labels)
        header_line = render_row('│', '│', '│', header_content)
        table_rows.append(header_line)
        table_rows.append(mid_line)
    for row in rows:
        row_content = render_row_content(row)
        row_line = render_row('│', '│', '│', row_content)
        table_rows.append(row_line)
    table_rows.append(bot_line)

    result_table = '\n'.join(table_rows)

    return result_table
