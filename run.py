from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
PORT = 8080

client = genai.Client()


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        prompt = (
            f"Generate the HTML for the {self.path} page of a website. "
            "Take as much creative liberty as you like. "
            "The website can be about any topic and have any functionality. "
            "The design can look good or horrendous. Aim for something unique. "
            "The HTML should be valid and complete, including the doctype, head, and body tags. "
            "Any CSS or JavaScript should be included inline in the HTML. "
            "Do not include any external resources. "
            "There can be links to other pages on the same website. "
            "Respond only with the content of the page in HTML format."
            "Do not use a code block.")
        response = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)))

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        for chunk in response:
            if chunk.text:
                print(chunk.text, end="")
                self.wfile.write(bytes(chunk.text, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer(("", PORT), MyServer)
    print(f"Running on http://localhost:{PORT}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
