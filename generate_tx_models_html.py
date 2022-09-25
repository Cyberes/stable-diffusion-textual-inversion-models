import argparse
import datetime
import os
import shutil
import sys
from urllib import request as ulreq

from bs4 import BeautifulSoup
import requests
from huggingface_hub import HfApi
from PIL import ImageFile


def getsizes(uri):
    # https://stackoverflow.com/a/37709319
    # get file size *and* image size (None if not known)
    file = ulreq.urlopen(uri)
    size = file.headers.get("content-length")
    if size:
        size = int(size)
    p = ImageFile.Parser()
    while True:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return (size, None)


parser = argparse.ArgumentParser()
parser.add_argument('out_file', nargs='?', help='file to save to', default='stable-diffusion-textual-inversion-models.html')
args = parser.parse_args()

print('Will save to file:', args.out_file)

# Get list of models under the sd-concepts-library organization
api = HfApi()
models_list = []
for model in api.list_models(author="sd-concepts-library"):
    models_list.append(model.modelId.replace('sd-concepts-library/', ''))
models_list.sort()

dt = datetime.datetime.now()
tz = dt.astimezone().tzname()

html_struct = f"""
<!DOCTYPE html>
<html lang="en">

<head>
  <title>Stable Diffusion Texual Inversion Models</title>
  <meta charset="utf-8">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
  <meta http-equiv="Pragma" content="no-cache" />
  <meta http-equiv="Expires" content="0" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">

  <link rel="apple-touch-icon" sizes="180x180" href="/stable-diffusion-textual-inversion-models/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/stable-diffusion-textual-inversion-models/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/stable-diffusion-textual-inversion-models/favicon-16x16.png">
  <link rel="manifest" href="/stable-diffusion-textual-inversion-models/site.webmanifest">
  <link rel="mask-icon" href="/stable-diffusion-textual-inversion-models/safari-pinned-tab.svg" color="#ee9321">
  <link rel="shortcut icon" href="favicon.ico">
  <meta name="msapplication-TileColor" content="#ee9321">
  <meta name="msapplication-config" content="/stable-diffusion-textual-inversion-models/browserconfig.xml">
  <meta name="theme-color" content="#ee9321">

  <!-- Matomo -->
  <script>
    var _paq = window._paq = window._paq || [];
    _paq.push(['trackPageView']);
    _paq.push(['enableLinkTracking']);
    (function() {{
        var u = "https://mato.evulid.cc/";
        _paq.push(['setTrackerUrl', u + 'matomo.php']);
        _paq.push(['setSiteId', '1']);
        var d = document,
          g = d.createElement('script'),
          s = d.getElementsByTagName('script')[0];
        g.async = true;
        g.src = u + 'matomo.js';
        s.parentNode.insertBefore(g, s);
      }})();
  </script>
  <!-- End Matomo Code -->
</head>

<body>
  <style>
    .thumbnail {{
        max-width: 185px;
        display: block;
        padding-top: 5px;
        padding-bottom: 5px;
      }}

    .model-title {{
        margin-top: 100px;
      }}
  </style>
  <div class="container" style="margin-bottom: 180px;">
    <div class="jumbotron text-center" style="margin-top: 45px;margin-right: 45px;margin-bottom: 0px;margin-left: 45px;">
      <h1>Stable Diffusion Texual Inversion Models</h1>
    </div>
    <center>
      <p style="margin-bottom: 45px;font-size: 8pt;">
        <i>Page updates automatically daily. Last updated <a class="btn-link" style="cursor: pointer;text-decoration: none;" data-toggle="tooltip" data-placement="bottom" title="{dt.strftime(f"%m-%d-%Y %H:%M:%S {tz}")}">{datetime.datetime.now().strftime("%A %B %d, %Y")}</a>.</i>
      </p>
    </center>

    <p>
      Generated from <a href="https://huggingface.co/sd-concepts-library">huggingface.co/sd-concepts-library</a>
    </p>

    <p>
      Models are downloaded straight from the HuggingFace repositories. There are currently {len(models_list)} textual inversion models in sd-concepts-library. The images displayed are the inputs, not the outputs.
    </p>

    <p>
      Want to quickly test concepts? Try the <a href="https://huggingface.co/spaces/sd-concepts-library/stable-diffusion-conceptualizer">Stable Diffusion Conceptualizer</a> on HuggingFace.
    </p>

    <p>
      <a href="https://github.com/Cyberes/stable-diffusion-textual-inversion-models/actions/workflows/generate_static_html.yml"><img src="https://github.com/Cyberes/stable-diffusion-textual-inversion-models/actions/workflows/generate_static_html.yml/badge.svg"></a>
    </p>
    <br>
    <hr>
    <script>
    const downloadAs = (url, name) => {{
      axios.get(url, {{
        headers: {{
          "Content-Type": "application/octet-stream"
        }},
        responseType: "blob"
      }})
        .then(response => {{
          const a = document.createElement("a");
          const url = window.URL.createObjectURL(response.data);
          a.href = url;
          a.download = name;
          a.click();
        }})
        .catch(err => {{
          console.log("error", err);
        }});
      _paq.push(['trackLink', url, 'download']);
    }};
    </script>
    <noscript><p><img src="https://mato.evulid.cc/matomo.php?idsite=1&rec=1&url=https://cyberes.github.io/stable-diffusion-textual-inversion-models" style="border:0;" alt="" /></p></noscript>
"""
 
i = 1
for model_name in models_list:
    # For testing
    # if i == 4:
    #     break

    print(f'{i}/{len(models_list)} -> {model_name}')

    # Images can be in a few different formats, figure out which one it's in
    restricted = False
    try:
        files = api.list_repo_files(
            repo_id=f'sd-concepts-library/{model_name}')
        concept_images = [i for i in files if i.startswith('concept_images/')]
    # sometimes an author will require you to share your contact info to gain access.
    except requests.exceptions.HTTPError:
        restricted = True

    if restricted:
        html_struct = html_struct + f"""
<h3 class="model-title">{model_name}</h3>
<p>
  {model_name} is restricted and you must share your contact information to view this repository.
  <a type="button" class="btn btn-link" href="https://huggingface.co/sd-concepts-library/{model_name}/">View Repository</a>
</p>
        """
    else:
        html_struct = html_struct + f"""
<h3 class="model-title">{model_name}</h3>
<p>
  <button type="button" class="btn btn-primary" onclick="downloadAs('https://huggingface.co/sd-concepts-library/{model_name}/resolve/main/learned_embeds.bin', '{model_name}.pt')">Download {model_name}.pt</button>
  <a type="button" class="btn btn-link" href="https://huggingface.co/sd-concepts-library/{model_name}/">View Repository</a>
</p>
<div class="row">
        """

        # Some repos don't have 3 images
        img_count = 3
        if len(concept_images) < 3:
            img_count = len(concept_images)

        for x in range(img_count):
            html_struct = html_struct + f"""
<div class="col-sm">
  <img class="thumbnail mx-auto lazy-load img-fluid" data-src="https://huggingface.co/sd-concepts-library/{model_name}/resolve/main/{concept_images[x]}">
</div>
            """
        html_struct = html_struct + '</div>'
    i = i + 1

html_struct = html_struct + """
  </div>
  <script>
    document.addEventListener("DOMContentLoaded", function() {
      let lazyloadImages;
      if ("IntersectionObserver" in window) {
        lazyloadImages = document.querySelectorAll(".lazy-load");
        let imageObserver = new IntersectionObserver(function(entries, observer) {
          entries.forEach(function(entry) {
            if (entry.isIntersecting) {
              let image = entry.target;
              image.src = image.dataset.src;
              image.classList.remove("lazy-load");
              imageObserver.unobserve(image);
            }
          });
        });
        lazyloadImages.forEach(function(image) {
          imageObserver.observe(image);
        });
      } else {
        let lazyloadThrottleTimeout;
        lazyloadImages = document.querySelectorAll(".lazy-load");

        function lazyload() {
          if (lazyloadThrottleTimeout) {
            clearTimeout(lazyloadThrottleTimeout);
          }
          lazyloadThrottleTimeout = setTimeout(function() {
            let scrollTop = window.pageYOffset;
            lazyloadImages.forEach(function(img) {
              if (img.offsetTop < (window.innerHeight + scrollTop)) {
                img.src = img.dataset.src;
                img.classList.remove('lazy-load');
              }
            });
            if (lazyloadImages.length == 0) {
              document.removeEventListener("scroll", lazyload);
              window.removeEventListener("resize", lazyload);
              window.removeEventListener("orientationChange", lazyload);
            }
          }, 20);
        }
        document.addEventListener("scroll", lazyload);
        window.addEventListener("resize", lazyload);
        window.addEventListener("orientationChange", lazyload);
      }
    })

    $(function() {
      $('[data-toggle="tooltip"]').tooltip({
        placement: "bottom"
      })
    })
  </script>
</body>
"""

# Load the HTML into bs4 so we can format it
soup = BeautifulSoup(html_struct, "html.parser")

f = open(args.out_file, 'w', encoding='utf-8')
f.write(str(soup.prettify()))
f.close()
