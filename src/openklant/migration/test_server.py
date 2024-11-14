import json


from http.server import BaseHTTPRequestHandler, HTTPServer


class JSONServer(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        data = {
            "inpBsn": "024325818",
            "anpIdentificatie": "107",
            "inpANummer": "",
            "geslachtsnaam": "Wever",
            "voorvoegselGeslachtsnaam": "",
            "voorletters": "W",
            "voornamen": "Willy",
            "geslachtsaanduiding": "",
            "geboortedatum": "2010-06-02",
            "verblijfsadres": None,
            "subVerblijfBuitenland": None,
        }

        json_data = json.dumps(data)

        self.wfile.write(json_data.encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8010), JSONServer)
    server.serve_forever()
