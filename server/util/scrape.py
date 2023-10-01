from unstructured.partition.auto import partition
from unstructured.partition.pdf import partition_pdf
import requests
import io
from bs4 import BeautifulSoup
from typing import Optional


def parse_url(url: [str], filename: Optional[str] = None):
    plaintext = ""
    if url:
        resp = requests.get(url)  # , stream=True)
        print(f"{resp.headers=}")

        if resp.status_code != 200:
            raise RuntimeError(
                f"error retrieving URL. {resp.status_code=} {resp.text=}"
            )

        content_type = resp.headers.get("Content-Type")

        body = io.BytesIO(resp.content)
        partitions = None
        if "pdf" in content_type:
            partitions = partition_pdf(file=body, strategy="hi_res")
        else:
            partitions = partition(url=url, content_type=content_type)

        plaintext = "\n".join(str(el) for el in partitions)
    else:
        # handle local file?
        pass

    return plaintext


def scrape_linkedin(url: str):
    resp = requests.get(url)

    if resp.status_code != 200:
        raise RuntimeError(f"error retrieving URL. {resp.status_code=} {resp.text=}")

    html_body = resp.text
    # get <main> element
    soup = partition(html_body)
    main_html = soup.find("main")
    plaintext = partition(main_html)
    return plaintext


if __name__ == "__main__":
    # print("Test PDF parser from URL")
    # result = parse_doc("https://writing.colostate.edu/guides/documents/resume/functionalsample.pdf")
    # assert "John W. Smith" in result
    # print("PDF Parser works")

    print("Test HTML parser for JD at URL")
    result = parse_url(
        "https://s3.amazonaws.com/nicbor.com/sample_job_description.html"
    )

    print("Test HTML parser from URL")
    result = parse_url("https://s3.amazonaws.com/nicbor.com/sample_resume.html")
    print(result)
    print("HTML parser works")
