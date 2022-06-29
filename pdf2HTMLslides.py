import os
import re
import pypdfium2 as pdfium


PROJECT_CWD = os.getcwd()

def createDir(out_dir):
    full_path = os.path.join(PROJECT_CWD, out_dir, 'assets', PDF_NAME)
    os.makedirs(full_path, exist_ok=True)

def pdf2jpg(filename, out_dir):
    image_out = os.path.join(out_dir, 'assets', PDF_NAME)
    pdf = pdfium.PdfDocument(filename)

    os.chdir(image_out)
    page_indices = [i for i in range(len(pdf))]
    renderer = pdf.render_topil(
        page_indices=page_indices,
    )
    image_names = list()
    for image, index in zip(renderer, page_indices):
        name = ("%s-%s.jpg" % (PDF_NAME, index))
        image_names.append(name)
        image.save(name)
        image.close()
    pdf.close()
    os.chdir(PROJECT_CWD)

    return image_names


def bodyHTML(image_names):
    slidesBody = ""
    for image in image_names:
        slidesBody += ('''<section data-background-transition="slide" data-background="assets/%s/%s"></section>''' % (PDF_NAME, image))
    return slidesBody

def headHTML():
    head = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>reveal.js - Slide Backgrounds</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link rel="stylesheet" href="../dist/reveal.css">
    <link rel="stylesheet" href="../dist/theme/serif.css" id="theme">
    <style type="text/css" media="screen">.slides section.has-dark-background,.slides section.has-dark-background h2 {
	color: #fff;}.slides section.has-light-background,.slides section.has-light-background h2 {
	color: #222;}</style></head><body><div class="reveal"><div class="slides">'''
    return head

def footHTML():
    foot = '''</div></div><script src="../dist/reveal.js"></script><script>
			// Full list of configuration options:
			// https://revealjs.revealjs.com/config/
			Reveal.initialize({
				center: true,
				transition: 'linear',
				// transitionSpeed: 'slow',
				// backgroundTransition: 'slide'
			});</script></body></html>'''
    return foot


if __name__ == '__main__':
    filename = 'Untitled_Artwork.pdf'  # sys.argv[1]
    global PDF_NAME
    PDF_NAME = re.findall('(.+)\.[pP][dD][fF]', filename)[0]
    out_dir = 'output'
    createDir(out_dir)
    image_names = pdf2jpg(filename, out_dir)
    head = headHTML()
    body = bodyHTML(image_names)
    foot = footHTML()
    data = (head+body+foot)

    os.chdir(out_dir)
    with open(PDF_NAME + '.html', "w") as a_file:
        a_file.write(data)
    os.chdir(PROJECT_CWD)


