
"Helps in initiating the HTML for each analysis"
def start_html(station_name):


    with open('HTMLS/' + str(station_name)+'.html', 'w') as dashboard:
        dashboard.write("<html><head></head><body>" + "\n")


        dashboard.write(
        '''
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        ul {
          list-style-type: none;
          margin: 0;
          padding: 0;
          overflow: hidden;
          background-color: #333;
        }

        li {
          float: left;
        }

        li a {
          display: block;
          color: white;
          text-align: center;
          padding: 14px 16px;
          text-decoration: none;
        }

        li a:hover {
          background-color: #111;
        }
        </style>
        </head>
        <body>

        <ul>
          <li><a class="active" href="#home">'''  + str(station_name))

        dashboard.write(
        '''
        </a></li>

        </ul>

        </body>
        </html>


        '''
        )

    # print("created ", station_name+'.html')
