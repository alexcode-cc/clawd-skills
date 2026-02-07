#!/usr/bin/env python3
"""
ASCII table formatter for Telegram (max width, box drawing, smart column sizing)
Usage: ascii-table [--width 58] [--mobile] "Col1|Col2|Col3" "val1|val2|val3"
"""
import sys
import textwrap
import argparse

# Box-drawing character sets
UNICODE_CHARS = {
    'top_left': '┌', 'top_right': '┐', 'bottom_left': '└', 'bottom_right': '┘',
    'horizontal': '─', 'vertical': '│',
    'top_tee': '┬', 'bottom_tee': '┴', 'left_tee': '├', 'right_tee': '┤',
    'cross': '┼'
}

ASCII_CHARS = {
    'top_left': '+', 'top_right': '+', 'bottom_left': '+', 'bottom_right': '+',
    'horizontal': '-', 'vertical': '|',
    'top_tee': '+', 'bottom_tee': '+', 'left_tee': '+', 'right_tee': '+',
    'cross': '+'
}

def make_table(rows, max_width=58, mobile=False):
    """Generate ASCII box table with smart column widths and wrapping."""
    if not rows:
        return ""
    
    chars = ASCII_CHARS if mobile else UNICODE_CHARS
    
    # Parse all rows into columns
    parsed = [row.split('|') for row in rows]
    num_cols = max(len(r) for r in parsed)
    
    # Pad rows to same number of columns
    for r in parsed:
        while len(r) < num_cols:
            r.append('')
        # Strip whitespace
        for i in range(len(r)):
            r[i] = r[i].strip()
    
    # Calculate ideal width per column (longest content)
    ideal_widths = []
    for col in range(num_cols):
        max_len = max(len(r[col]) for r in parsed)
        ideal_widths.append(max_len)
    
    # Calculate available space
    # Borders: │ + (space + content + space + │) per col = 1 + 3*num_cols + num_cols
    border_chars = 1 + (3 * num_cols)
    available = max_width - border_chars
    
    total_ideal = sum(ideal_widths)
    
    if total_ideal <= available:
        # Everything fits! Use ideal widths exactly (no padding)
        col_widths = ideal_widths[:]
    else:
        # Need to compress. Distribute proportionally with min width
        min_width = 5
        col_widths = []
        for ideal in ideal_widths:
            # Proportional share
            share = max(min_width, int(available * ideal / total_ideal))
            col_widths.append(share)
        
        # Adjust to fit exactly
        while sum(col_widths) > available:
            # Shrink largest
            max_idx = col_widths.index(max(col_widths))
            col_widths[max_idx] -= 1
        while sum(col_widths) < available:
            # Grow smallest that's under its ideal
            for i, (w, ideal) in enumerate(zip(col_widths, ideal_widths)):
                if w < ideal and sum(col_widths) < available:
                    col_widths[i] += 1
            else:
                # Just add to last
                col_widths[-1] += 1
                break
    
    lines = []
    
    # Top border
    top = chars['top_left']
    for i, w in enumerate(col_widths):
        top += chars['horizontal'] * (w + 2)
        top += chars['top_tee'] if i < len(col_widths) - 1 else chars['top_right']
    lines.append(top)
    
    def add_row(cells, separator=False):
        # Wrap each cell
        wrapped_cols = []
        for i, cell in enumerate(cells):
            wrapped = textwrap.wrap(cell, width=col_widths[i]) or ['']
            wrapped_cols.append(wrapped)
        
        # Find max lines needed
        max_lines = max(len(w) for w in wrapped_cols)
        
        # Pad each column to max_lines
        for w in wrapped_cols:
            while len(w) < max_lines:
                w.append('')
        
        # Output each line
        for line_idx in range(max_lines):
            row_str = chars['vertical']
            for col_idx, w in enumerate(wrapped_cols):
                content = w[line_idx]
                row_str += f" {content:<{col_widths[col_idx]}} {chars['vertical']}"
            lines.append(row_str)
        
        # Separator
        if separator:
            sep = chars['left_tee']
            for i, w in enumerate(col_widths):
                sep += chars['horizontal'] * (w + 2)
                sep += chars['cross'] if i < len(col_widths) - 1 else chars['right_tee']
            lines.append(sep)
    
    # Add all rows
    for i, row in enumerate(parsed):
        is_last = (i == len(parsed) - 1)
        add_row(row, separator=(not is_last))
    
    # Bottom border
    bottom = chars['bottom_left']
    for i, w in enumerate(col_widths):
        bottom += chars['horizontal'] * (w + 2)
        bottom += chars['bottom_tee'] if i < len(col_widths) - 1 else chars['bottom_right']
    lines.append(bottom)
    
    return '\n'.join(lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ASCII table for Telegram')
    parser.add_argument('rows', nargs='+', help='Rows as "col1|col2|..."')
    parser.add_argument('--width', '-w', type=int, default=None, help='Max width (default: 58 desktop, 48 mobile)')
    parser.add_argument('--mobile', '-m', action='store_true', help='Use ASCII chars (mobile-friendly, 48 char default)')
    args = parser.parse_args()
    
    # Default width: 48 for mobile, 58 for desktop
    width = args.width if args.width else (48 if args.mobile else 58)
    
    print(make_table(args.rows, max_width=width, mobile=args.mobile))
