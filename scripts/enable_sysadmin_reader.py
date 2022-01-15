#!/usr/bin/env python
import argparse
from typing import Dict, List

from rich import console
from rich.table import Table

from enablesysadminrssreader import get_rss, parse_rss, ENABLE_SYSADMIN_URL


def create_table(rss: List[Dict[str, str]]) -> Table:
    rss_table = Table(title=f"Enable Sysadmin RSS headlines for today ({len(rss)})")
    rss_table.add_column("Title", justify="right", no_wrap=False)
    rss_table.add_column("Link", justify="right", no_wrap=True)
    rss_table.add_column("Description", style="cyan", no_wrap=False)
    for article in rss:
        rss_table.add_row(
            article['title'],
            article['link'],
            article['description']
        )
    return rss_table


if __name__ == "__main__":
    CONSOLE = console.Console()
    PARSER = argparse.ArgumentParser(
        description="Script to display the top 10 RSS articles from Enable Sysadmin"
    )
    PARSER.add_argument(
        "--url",
        required=False,
        default=ENABLE_SYSADMIN_URL,
        action='store',
        help=f'Override the RSS url for Enable Sysadmin. Default: {ENABLE_SYSADMIN_URL}'
    )
    ARGS = PARSER.parse_args()
    raw_rss = get_rss(ARGS.url)
    parsed_rss = parse_rss(raw_rss)
    table = create_table(parsed_rss)
    CONSOLE.print(table)
