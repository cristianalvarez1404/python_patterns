from htmlbuilder import HTMLPage, HTMLBuilder

def main() -> None:
  builder = HTMLBuilder()
  
  page = (builder.add_title("My Web Page")
          .add_heading("Welcome to my Web Page")
          .add_paragraph("This is a simple HTML page.")
          .add_button("Visit codes",onclick="http://www.google.com")
          .build()
          )

  file_path = "page.html"
  with open(file_path,"w") as f:
    f.write(page.render())


if __name__ == "__main__":
  main()