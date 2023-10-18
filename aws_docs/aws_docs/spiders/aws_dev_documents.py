import scrapy
import pathlib


class AwsDevDocumentsSpider(scrapy.Spider):
    name = "aws_dev_documents"
    allowed_domains = ["docs.aws.amazon.com"]
    start_urls = [
        "https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html",
        "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html",
    ]

    def parse(self, response):

        # -------------------------------------------------------
        # アイテムをエクスポートする
        # クロールしたItem(html)のリストをJSONLファイルで出力します。
        # scrapy crawl aws_dev_documents -o　aws_dev_documents.json
        # -oで出力するファイルを指定してます。
        resp = {
            'Title': response.xpath('//head/title/text()').get(),
            'URLs': response.url
        }
        yield resp

        # スクレイピングしたHTMLファイルをローカルディレクトリに出力する。
        self.save_html_file(response=response)

        # XPathで次にクロールするHTMLURLを抽出する
        next_page = response.xpath('//div[contains(@class, "next-link")]/@href').get()

        # -------------------------------------------------------
        # 新しいリクエストを発行する
        # 次にクロールするページを指定します
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    def save_html_file(self, response):
        # ./aws_dev_docs/ディレクトリ配下にHTMLファイルを保存します
        file_name = self.make_path_strings(response)
        with open(file_name, 'w') as f:
            f.write(response.text)

    @staticmethod
    def make_path_strings(response) -> str:
        # VectorDBに読み込ませるHTMLのURLをディレクトリ構成に変換します。
        # 例:
        # https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.htmlを
        # ./aws_dev_docs/docs.aws.amazon.com/kendra/latest/db/what-is-kendra.htmlに変換します。

        root_path = './aws_dev_docs'
        url = response.url

        path = url.replace('https:/', root_path)
        path_list = path.rsplit('/', 1)

        directory = path_list[0] + '/'
        file_name = path_list[1]

        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

        print(f'directory_path: {directory + file_name}')
        return directory + file_name
