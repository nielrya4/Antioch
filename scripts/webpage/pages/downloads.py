from antioch import *
from antioch.macros import DownloadLink
page = Div(
    H3("Downloads"),
    Br(),
    DownloadLink(
        data="This is a downloaded file",
        filename="file.txt",
        text="Download Sample TXT file"
    )
)
