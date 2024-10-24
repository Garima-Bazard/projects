import os
import pprint as pp
import argparse

link_text = """onclick="window.open(`%s`, '_blank');"
                    style="cursor: pointer;\""""

template = """<div class="hitbox">
    <div class="box">
        <h2 class="name">%s</h2>
        <img class="product" %s src="images/%s">
        <p class="desc" %s>%s</p>
        <div class="back"><img src="images/%s"></img></div>
    </div>
</div>"""

template_gif = """<div class="hitbox2">
					<img
						src="images/%s"
						style="
							display: block;
							margin-left: auto;
							margin-right: auto;
							height: 100%%;
						"
					/>
				</div>"""

html_final = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <link rel="icon" href="images/toad.gif" type="image/gif">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> T U G D U A L</title>
    <link rel="stylesheet" href="index.css">
    <script src="vanilla-tilt.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"
        integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
</head>

<body>
    <div>
        <div id="background">
            <p id="background-text">TUGDUAL</p>
			<p id="background-text2">EPFL, Masters 2nd year Computer Architecture</p>
        </div>
        <div id="container">
            %s
        </div>
    </div>
</body>
<script>
    $('.hitbox').hover(function () {

        $(this).stop().animate({
            height: Math.max($(this).find(".desc").height() + 30 + $(this).find(".product").height(), 200),
        });
    }, function () {
        $(this).stop().animate({
            height: "150px",
        })
    });
</script>
<script src="./index.js"></script>

</html>
            """


def transform_text(text_array) -> str:
    if "[" in text_array[0]:  # Contains link
        title = text_array[0].split('# [')[1].split('](')[0]
        # Get link and remove the last )
        link = text_array[0].split('](')[1][:-2]
        card_image = text_array[1][4:-1]
        card_text = text_array[2][:-1]
        back_image = text_array[-1][4:]
        return template % (title, (link_text % link), back_image, (link_text % link), card_text, card_image)
    else:
        title = text_array[0].split('# ')[1][:-1]
        card_image = text_array[1][4:-2]
        card_text = text_array[3][:-1]
        back_image = text_array[-1][4:-1]
        return template % (title, "", back_image, "", card_text, card_image)


def main(article_path):
    file_list = os.listdir(article_path)
    file_list.sort()
    file_list.reverse()
    list_of_articles = []
    for element in file_list:
        print(element)
        if element == "images" or element == ".DS_Store":
            pass
        elif element[-4:] == ".gif":
            list_of_articles.append(template_gif % (element))
            os.system(f"xcopy /Y /I {element} ./images/")
        else:
            with open(article_path + str(element)) as article_file:
                print(element)
                list_of_articles.append(
                    transform_text(article_file.readlines()))
    final_string = html_final % ("\n".join(list_of_articles))
    with open("./index.html", "w") as final_doc:
        final_doc.write(final_string)
        final_doc.close()

    os.system(f"robocopy {os.path.join(article_path, 'images')} ./images /e")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate HTML page from articles")
    parser.add_argument('article_path', type=str, help="Path to the directory containing the article files")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Pass the article path to the main function
    main(args.article_path)
