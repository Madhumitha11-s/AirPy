import base64
from io import BytesIO
"""
Writes different formats of images to HTMLS
"""
def figures_to_html_app(figs, station_name):
    with open('HTMLS/' + str(station_name), 'a') as dashboard:
        dashboard.write("<html><head></head><body>" + "\n")
        for fig in figs:

            inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
            dashboard.write(inner_html)
        dashboard.write("</body></html>" + "\n")

def write_html_fig(fig, station_name):
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    html = '<img src=\'data:image/png;base64,{}\'>'.format(encoded)
    with open('HTMLS/' + str(station_name) + '.html', 'a') as f:
        f.write(html)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'