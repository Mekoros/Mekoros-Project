import django
django.setup()
import argparse
from mekoros.settings import STATICFILES_DIRS
from mekoros.sitemap import MekorosSiteMapGenerator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_directory", help="directory to write output", default=STATICFILES_DIRS[0])
    args = parser.parse_args()

    MekorosSiteMapGenerator('org', args.output_directory).generate_sitemaps()
    MekorosSiteMapGenerator('org.il', args.output_directory).generate_sitemaps()

